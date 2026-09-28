"""Offline contract tests: synthetic model IDs/keys, temporary config, mocked HTTP."""

from __future__ import annotations

import importlib
import io
import json
import shutil
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import httpx
from openai import OpenAI

from scripts.model_profile import main
from src.ai.llm_client import JSON_ONLY, LLMClient, LLMError, PROVIDERS
from src.ai.model_profiles import CONFIG_DIR, ProfileError, load_profiles, select_profile

MESSAGES = [{"role": "user", "content": "Assess this synthetic test job."}]
SCHEMA = {
    "type": "object",
    "properties": {"fit": {"type": "boolean"}},
    "required": ["fit"],
    "additionalProperties": False,
}
TEST_KEY = "synthetic-test-key-not-a-credential"


def target(
    provider: str = "openrouter", model: str = "test-model", **kwargs: Any
) -> dict[str, Any]:
    return {"provider": provider, "model": model, "supports_json_schema": True, **kwargs}


def completion(
    content: Any = "  hello  ", finish: str = "stop", refusal: str | None = None
) -> dict[str, Any]:
    return {
        "id": "test-completion",
        "object": "chat.completion",
        "created": 0,
        "model": "test-model",
        "choices": [
            {
                "index": 0,
                "finish_reason": finish,
                "message": {"role": "assistant", "content": content, "refusal": refusal},
            }
        ],
    }


class ProfileTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.config_dir = Path(self.temp.name)
        self.example = self.config_dir / "model_profiles.example.json"
        self.local = self.config_dir / "model_profiles.local.json"
        shutil.copyfile(CONFIG_DIR / self.example.name, self.example)
        # MockTransport should handle everything. A real socket is always a test failure.
        self.network_guard = patch(
            "socket.socket.connect", side_effect=AssertionError("Network prohibited")
        )
        self.network_guard.start()
        self.addCleanup(self.network_guard.stop)

    def overlay(self, data: dict[str, Any]) -> None:
        self.local.write_text(json.dumps(data), encoding="utf-8")

    def configure(self, **fields: Any) -> None:
        self.overlay({"profiles": {"economy": {"primary": target(), **fields}}})

    def client(self, responses: list[httpx.Response | Exception] | None = None) -> LLMClient:
        self.requests: list[httpx.Request] = []
        self.factory_options: list[dict[str, Any]] = []
        pending = list(responses or [httpx.Response(200, json=completion('{"fit":true}'))])

        def handler(request: httpx.Request) -> httpx.Response:
            self.requests.append(request)
            if not pending:
                raise AssertionError("Unexpected extra request")
            result = pending.pop(0)
            if isinstance(result, Exception):
                raise result
            return result

        def factory(**kwargs: Any) -> OpenAI:
            self.factory_options.append(kwargs)
            return OpenAI(
                http_client=httpx.Client(transport=httpx.MockTransport(handler)), **kwargs
            )

        return LLMClient(
            config_dir=self.config_dir,
            environ={entry[1]: TEST_KEY for entry in PROVIDERS.values()},
            client_factory=factory,
        )

    def test_examples_load_without_local_file_or_keys(self) -> None:
        config = load_profiles(self.config_dir)
        self.assertEqual(config.active_profile, "economy")
        self.assertEqual(set(config.profiles), {"economy", "quality", "discussion"})
        self.assertIsNone(config.profiles["economy"].primary.model)
        self.assertEqual(config.profiles["economy"].structured_output, "required")
        self.assertFalse(config.profiles["discussion"].allow_artifacts)
        self.assertFalse(self.local.exists())

    def test_overlay_merges_targets_and_replaces_fallback_list(self) -> None:
        self.configure(primary={"model": "test-primary"}, fallbacks=[target("xai", "test-backup")])
        profile = load_profiles(self.config_dir).profiles["economy"]
        self.assertEqual(profile.primary.provider, "openrouter")
        self.assertEqual(profile.primary.model, "test-primary")
        self.assertEqual(profile.fallbacks[0].provider, "xai")
        self.assertEqual(profile.temperature, 0.1)

    def test_use_preserves_local_models_and_example_bytes(self) -> None:
        self.configure(fallbacks=[target("xai", "test-backup")])
        original = self.example.read_bytes()
        overrides = json.loads(self.local.read_text())["profiles"]
        select_profile("discussion", self.config_dir)
        local = json.loads(self.local.read_text())
        self.assertEqual(local["active_profile"], "discussion")
        self.assertEqual(local["profiles"], overrides)
        self.assertEqual(self.example.read_bytes(), original)
        self.assertEqual(list(self.config_dir.glob(".model_profiles-*.tmp")), [])

    def test_use_creates_minimal_selection_file(self) -> None:
        select_profile("economy", self.config_dir)
        self.assertEqual(json.loads(self.local.read_text()), {"active_profile": "economy"})

    def test_unknown_profile_is_clear_and_does_not_write(self) -> None:
        with self.assertRaisesRegex(ProfileError, "Profile is absent"):
            select_profile("absent", self.config_dir)
        self.assertFalse(self.local.exists())

    def test_invalid_local_json_never_echoes_input(self) -> None:
        self.local.write_text('{"api_key": "' + TEST_KEY, encoding="utf-8")
        with self.assertRaises(ProfileError) as failure:
            load_profiles(self.config_dir)
        self.assertNotIn(TEST_KEY, str(failure.exception))

    def test_bad_config_and_credentials_are_rejected(self) -> None:
        for fields in [
            {"api_key": TEST_KEY},
            {"primary": {"provider": "unknown"}},
            {"primary": {"model": "sk-test-secret"}},
            {"max_output_tokens": 0},
            {"max_output_tokens": True},
            {"temperature": 3.0},
            {"structured_output": "json"},
            {"primary": {"supports_json_schema": "yes"}},
            {"primary": {"token_parameter": "unknown"}},
        ]:
            with self.subTest(fields=fields):
                self.configure(**fields)
                with self.assertRaises(ProfileError) as failure:
                    load_profiles(self.config_dir)
                self.assertNotIn(TEST_KEY, str(failure.exception))

    def test_absent_active_profile_is_rejected(self) -> None:
        self.overlay({"active_profile": "absent"})
        with self.assertRaisesRegex(ProfileError, "Active profile is absent"):
            load_profiles(self.config_dir)

    def test_cli_list_show_use_and_error_are_offline(self) -> None:
        self.configure(description=TEST_KEY)
        for command in [["list"], ["show"], ["use", "quality"], ["show"]]:
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                status = main(["--config-dir", str(self.config_dir), *command])
            self.assertEqual(status, 0)
            self.assertNotIn(TEST_KEY, stdout.getvalue())
        stderr = io.StringIO()
        with redirect_stderr(stderr):
            status = main(["--config-dir", str(self.config_dir), "use", "absent"])
        self.assertEqual(status, 2)
        self.assertIn("Profile is absent", stderr.getvalue())

    def test_unconfigured_model_blocks_before_factory(self) -> None:
        client = self.client()
        with self.assertRaisesRegex(ProfileError, "Set actual model IDs"):
            client.chat(MESSAGES, json_schema=SCHEMA)
        self.assertEqual(self.factory_options, [])

    def test_all_provider_endpoints_headers_and_token_parameters(self) -> None:
        for provider, (url, _) in PROVIDERS.items():
            with self.subTest(provider=provider):
                self.configure(primary=target(provider))
                client = self.client()
                self.assertEqual(client.chat(MESSAGES, json_schema=SCHEMA), '{"fit":true}')
                request = self.requests[0]
                self.assertEqual(str(request.url), url + "/chat/completions")
                self.assertEqual(request.headers["authorization"], "Bearer " + TEST_KEY)
                body = json.loads(request.content)
                token_key = "max_completion_tokens" if provider == "openai" else "max_tokens"
                self.assertEqual(body[token_key], 1500)
                self.assertEqual(body["temperature"], 0.1)
                self.assertEqual(self.factory_options[0]["max_retries"], 0)
                self.assertEqual(self.factory_options[0]["timeout"], 45.0)
                if provider == "openrouter":
                    self.assertNotIn("response_format", body)
                    self.assertNotIn("provider", body)
                    self.assertEqual(body["messages"][-1]["content"], JSON_ONLY)
                else:
                    self.assertTrue(body["response_format"]["json_schema"]["strict"])
                    self.assertEqual(body["response_format"]["json_schema"]["schema"], SCHEMA)
                    self.assertNotIn("provider", body)

    def test_primary_failure_uses_fallback_capabilities(self) -> None:
        self.configure(fallbacks=[target("openai", "test-backup", supports_temperature=False)])
        client = self.client(
            [
                httpx.Response(429, json={"error": {"message": TEST_KEY}}),
                httpx.Response(200, json=completion('{"fit":true}')),
            ]
        )
        self.assertEqual(client.chat(MESSAGES, json_schema=SCHEMA), '{"fit":true}')
        first, second = [json.loads(request.content) for request in self.requests]
        self.assertEqual(first["model"], "test-model")
        self.assertEqual(second["model"], "test-backup")
        self.assertEqual(second["max_completion_tokens"], 1500)
        self.assertNotIn("temperature", second)
        self.assertNotIn("response_format", first)
        self.assertTrue(second["response_format"]["json_schema"]["strict"])
        self.assertNotIn("provider", second)

    def test_missing_keys_skip_without_requests_and_never_echo_keys(self) -> None:
        self.configure(fallbacks=[target("xai", "test-backup")])
        client = self.client()
        client._environ = {"XAI_API_KEY": TEST_KEY}
        self.assertEqual(client.chat(MESSAGES, json_schema=SCHEMA), '{"fit":true}')
        self.assertEqual(self.requests[0].url.host, "api.x.ai")
        client = self.client()
        client._environ = {}
        with self.assertRaisesRegex(LLMError, "OPENROUTER_API_KEY missing"):
            client.chat(MESSAGES, json_schema=SCHEMA)
        self.assertEqual(self.requests, [])

    def test_strict_output_never_silently_degrades(self) -> None:
        self.configure(primary=target(supports_json_schema=False))
        client = self.client()
        with self.assertRaisesRegex(ProfileError, "requires json_schema"):
            client.chat(MESSAGES)
        with self.assertRaisesRegex(ProfileError, "No configured target supports"):
            client.chat(MESSAGES, json_schema=SCHEMA)
        self.assertEqual(self.requests, [])

    def test_unsupported_primary_is_skipped_for_capable_fallback(self) -> None:
        self.configure(
            primary=target(supports_json_schema=False), fallbacks=[target("xai", "test-backup")]
        )
        client = self.client()
        self.assertEqual(client.chat(MESSAGES, json_schema=SCHEMA), '{"fit":true}')
        self.assertEqual(len(self.requests), 1)
        self.assertEqual(self.requests[0].url.host, "api.x.ai")

    def test_request_preview_no_keys_or_client_and_deduplicates(self) -> None:
        self.configure(fallbacks=[target(), target("xai", "test-backup")])
        client = self.client()
        plans = client.build_requests(MESSAGES, json_schema=SCHEMA)
        self.assertEqual([p.model for p in plans], ["test-model", "test-backup"])
        self.assertEqual(self.factory_options, [])
        self.assertNotIn(TEST_KEY, repr(plans))

    def test_token_parameter_override_and_null_temperature(self) -> None:
        self.configure(primary=target(token_parameter="max_completion_tokens"), temperature=None)
        client = self.client()
        params = client.build_requests(MESSAGES, json_schema=SCHEMA)[0].parameters
        self.assertEqual(params["max_completion_tokens"], 1500)
        self.assertNotIn("max_tokens", params)
        self.assertNotIn("temperature", params)

    def test_discussion_text_and_artifact_policy(self) -> None:
        self.overlay(
            {"active_profile": "discussion", "profiles": {"discussion": {"primary": target()}}}
        )
        client = self.client([httpx.Response(200, json=completion())])
        self.assertFalse(client.profile.allow_artifacts)
        self.assertEqual(client.chat(MESSAGES), "hello")
        self.assertNotIn("response_format", json.loads(self.requests[0].content))
        with self.assertRaisesRegex(ProfileError, "disabled"):
            client.build_requests(MESSAGES, json_schema=SCHEMA)

    def test_auth_and_billing_errors_stop_without_leaking_response(self) -> None:
        self.configure(fallbacks=[target("xai", "test-backup")])
        for status in [401, 402, 403]:
            with self.subTest(status=status):
                client = self.client(
                    [httpx.Response(status, json={"error": {"message": TEST_KEY}})]
                )
                with self.assertRaises(LLMError) as failure:
                    client.chat(MESSAGES, json_schema=SCHEMA)
                self.assertIn(str(status), str(failure.exception))
                self.assertNotIn(TEST_KEY, str(failure.exception))
                self.assertEqual(len(self.requests), 1)

    def test_refusal_does_not_trigger_fallback(self) -> None:
        self.configure(fallbacks=[target("xai", "test-backup")])
        client = self.client([httpx.Response(200, json=completion(None, refusal=TEST_KEY))])
        with self.assertRaisesRegex(LLMError, "declined") as failure:
            client.chat(MESSAGES, json_schema=SCHEMA)
        self.assertNotIn(TEST_KEY, str(failure.exception))
        self.assertEqual(len(self.requests), 1)

    def test_invalid_empty_truncated_and_schema_mismatched_output_fall_back(self) -> None:
        self.configure(fallbacks=[target("xai", "test-backup")])
        for bad in [
            completion(""),
            completion('{"fit":true}', "length"),
            completion("not JSON"),
            completion('{"fit":"wrong-type"}'),
            {"choices": []},
            {"error": {"message": TEST_KEY}},
        ]:
            with self.subTest(bad=bad):
                client = self.client(
                    [
                        httpx.Response(200, json=bad),
                        httpx.Response(200, json=completion('{"fit":true}')),
                    ]
                )
                self.assertEqual(client.chat(MESSAGES, json_schema=SCHEMA), '{"fit":true}')
                self.assertEqual(len(self.requests), 2)

    def test_connection_failure_is_bounded_and_sanitized(self) -> None:
        self.configure(fallbacks=[target("xai", "test-backup")])
        client = self.client(
            [
                httpx.ConnectError(TEST_KEY),
                httpx.Response(503, json={"error": {"message": TEST_KEY}}),
            ]
        )
        with self.assertRaises(LLMError) as failure:
            client.chat(MESSAGES, json_schema=SCHEMA)
        self.assertIn("connection", str(failure.exception))
        self.assertIn("HTTP 503", str(failure.exception))
        self.assertNotIn(TEST_KEY, str(failure.exception))
        self.assertEqual(len(self.requests), 2)

    def test_unexpected_sdk_error_is_sanitized(self) -> None:
        self.configure()
        client = self.client()
        client._client_factory = MagicMock(side_effect=ValueError(TEST_KEY))
        with self.assertRaisesRegex(LLMError, "check local SDK") as failure:
            client.chat(MESSAGES, json_schema=SCHEMA)
        self.assertNotIn(TEST_KEY, str(failure.exception))

    def test_nonfinite_numbers_are_not_accepted_as_structured_json(self) -> None:
        self.configure()
        for content in ['{"value":NaN}', '{"value":Infinity}', '{"value":1e999}']:
            with self.subTest(content=content):
                client = self.client([httpx.Response(200, json=completion(content))])
                with self.assertRaisesRegex(LLMError, "invalid response"):
                    client.chat(MESSAGES, json_schema={"type": "object"})

    def test_failed_atomic_selection_preserves_local_file(self) -> None:
        self.configure()
        original = self.local.read_bytes()
        with patch("src.ai.model_profiles.os.replace", side_effect=OSError(TEST_KEY)):
            with self.assertRaises(ProfileError) as failure:
                select_profile("quality", self.config_dir)
        self.assertEqual(self.local.read_bytes(), original)
        self.assertNotIn(TEST_KEY, str(failure.exception))
        self.assertEqual(list(self.config_dir.glob(".model_profiles-*.tmp")), [])

    def test_invalid_messages_and_external_schema_references_are_local_errors(self) -> None:
        self.configure()
        client = self.client()
        for messages in [[], [{"role": "invalid", "content": "text"}], [{"role": "user"}]]:
            with self.assertRaises(ProfileError):
                client.build_requests(messages, json_schema=SCHEMA)
        for schema in [{"type": "invalid"}, {"$ref": "https://example.invalid/schema"}]:
            with self.assertRaises(ProfileError):
                client.build_requests(MESSAGES, json_schema=schema)
        self.assertEqual(self.factory_options, [])

    def test_existing_grok_api_remains_callable_with_mocked_sdk(self) -> None:
        with patch("dotenv.load_dotenv"):
            legacy = importlib.import_module("src.ai.grok_client")
        response = MagicMock()
        response.choices[0].message.content = "  legacy response  "
        with patch.dict("os.environ", {"XAI_API_KEY": TEST_KEY}), patch.object(
            legacy, "OpenAI"
        ) as sdk:
            sdk.return_value.chat.completions.create.return_value = response
            client = legacy.GrokClient(model="test-legacy-model")
            self.assertEqual(client.chat(MESSAGES), "legacy response")
            self.assertEqual(client.query("test prompt"), "legacy response")
            self.assertEqual(
                client.generate_tailored_summary("test job", "test profile"), "legacy response"
            )
            self.assertEqual(sdk.call_args.kwargs["base_url"], PROVIDERS["xai"][0])


if __name__ == "__main__":
    unittest.main()
