# Pipeline model profiles

For current job execution, use [PIPELINE_OPERATOR.md](../docs/PIPELINE_OPERATOR.md).
This file documents the reusable profile/client setup from Prompt 01. The new
canonical runner defaults to the `economy` and `quality` profiles, while allowing
explicit named analysis and generation profiles per run. Changing the active
selection does not switch its stage defaults. Its request-plan limit and cache
limitations are described in [PIPELINE_ARCHITECTURE.md](../docs/PIPELINE_ARCHITECTURE.md).

Prompt 01 foundation: opt-in chat through OpenRouter, xAI or OpenAI. Existing
`GrokClient` and pipeline callers are unchanged. Switching a profile affects new
`LLMClient` instances only; it does not yet reroute the old pipeline scripts.

## Local setup and switching

The example config is safe to track in Git. No model IDs have been selected on
Sean's behalf: `null` is a deliberate setup placeholder and cannot trigger a call.
Keep keys in the root `.env`, using `OPENROUTER_API_KEY`, `XAI_API_KEY`, or
`OPENAI_API_KEY`. The client also honors an existing environment variable for
automation; `.env` does not override it. Keys are never stored in profile JSON.

From the repository's PowerShell terminal:

```powershell
. .\env_setter.ps1
python scripts\model_profile.py list
python scripts\model_profile.py show
python scripts\model_profile.py use economy
```

`use` creates/updates the gitignored `config/model_profiles.local.json` and
preserves any model overrides. It can select a profile before its model IDs are
filled in, but reports that setup is still needed. All three CLI commands are
offline and do not read `.env` or initialize a provider client. An absent profile
returns exit code 2 without writing a file.

After selection, edit the local JSON to supply exact model IDs from your provider
account. A safe local-overlay shape is shown below. Replace `null` before calling
the client; the placeholder is not an actual model ID.

The gitignored local overlay is the place to set Sean's economy model
(`deepseek/deepseek-v4-flash-0731` on OpenRouter). Quality may remain `null`
until a supervised generate step. Keys stay in `.env` as `OPENROUTER_API_KEY`.

```json
{
  "active_profile": "economy",
  "profiles": {
    "economy": {
      "primary": {
        "provider": "openrouter",
        "model": null,
        "supports_json_schema": true,
        "supports_temperature": true
      },
      "fallbacks": []
    }
  }
}
```

Local object fields merge over the example; lists replace the entire example
list. Other profiles keep their example defaults. New locally named profiles
may be supplied too. Unknown fields, malformed provider names, invalid budgets,
and credential fields are rejected without echoing the file contents.

The wrapper accepts any configured profile name, so you can use names meaningful
to you, such as `economy_deepseek` and `quality_claude`:

```powershell
.\job-runner.ps1 .\intake\new_job.md -Mode triage -AnalysisProfile economy_deepseek
.\job-runner.ps1 .\intake\new_job.md -Mode generate -AnalysisProfile economy_deepseek -GenerationProfile quality_claude
```

The analysis profile needs structured-schema support. The generation profile
also needs `allow_artifacts: true`; both canonical profiles must have no
fallbacks. `model_profile.py use` selects an existing profile but does not create
one—add a new named profile to the local overlay first.

Each fallback is another target object with the same fields as `primary`. Supply
its own `provider`, `model`, and capability flags; fallbacks may cross providers.
The client never guesses a model ID, price, availability, or capability. Configure
those flags for the exact chosen model. Disable `supports_temperature` for models
that reject temperature. `token_parameter` optionally overrides the token field:
OpenAI defaults to `max_completion_tokens`; xAI/OpenRouter default to `max_tokens`.

## Profile intent

| Profile | Intended work | Output cap | JSON policy | Artifact policy |
| --- | --- | --- | --- | --- |
| economy | Tier 1 fit analysis with a low-cost model | 1,500 tokens | Schema required, strict | Disabled |
| quality | Accepted-job resume and cover package with a stronger model | 4,500 tokens | Optional strict schema | Allowed |
| discussion | Interactive job/career discussion | 2,000 tokens | Text | Disabled |

`allow_artifacts` is enforced by the canonical runner for its selected generation stage; this
client itself only returns text and never generates files under any profile. Output
caps are per attempt, not dollar limits. Reasoning tokens can consume a provider's
completion budget. Fallback attempts can add cost, so keep the list short.

## Uniform chat interface

```python
from src.ai.llm_client import LLMClient

schema = {
    "type": "object",
    "properties": {"fit": {"type": "boolean"}},
    "required": ["fit"],
    "additionalProperties": False,
}
client = LLMClient("economy")  # Omit the name to use the active profile.
messages = [{"role": "user", "content": "Assess the supplied job against the supplied profile."}]

# Offline preview: constructs requests without reading keys or making API calls.
plans = client.build_requests(messages, json_schema=schema)

# Paid only when explicitly run with configured models and credentials:
# result = client.chat(messages, json_schema=schema, schema_name="job_fit")
```

`chat()` always returns a stripped string; schema output is validated JSON text
that the caller can parse with `json.loads`. The new interface supports
non-streaming text messages and intentionally omits tools, audio, Responses API
features, and arbitrary SDK parameter passthrough in this step.

For schema requests, known unsupported targets are skipped, and every attempted
target receives the same strict schema. OpenRouter requests also require endpoint
parameter support. There is no silent downgrade to plain text or JSON-object mode.
Schemas are checked locally, external schema references are rejected, and output
is checked for valid JSON and schema compliance. Refusal/content-filter responses
stop immediately. Empty, incomplete or invalid output can use a configured fallback.

The client makes at most one SDK request per eligible unique provider/model pair,
with SDK retries disabled and a 45-second request timeout. The list is bounded to
one primary plus five fallbacks. Missing credentials skip that target. HTTP
400/404/408/409/422/429/500/502/503/504 and connection/timeout failures can fall back;
other HTTP errors, including authentication/access/billing failures, stop.
Bad requests can fail on every target, so check the schema and capability settings
before expanding a fallback list. Errors report only provider names, fixed key
variable names, status codes, and safe categories; raw SDK errors, provider bodies,
and credentials are not included.

## Validation and compatibility

The focused suite uses synthetic model IDs and keys in temporary configs, mocked
HTTP, and a socket guard. It tests the real installed SDK's request construction
without contacting providers. It also exercises the original Grok interface using
a mocked SDK. No dependency installation or full pipeline migration was performed.

Commands run from `D:\Workarea\jobsearch` (activate the environment in each shell):

```powershell
. .\env_setter.ps1
python -c "import importlib.metadata as m; print({n:m.version(n) for n in ['httpx','openai','jsonschema','python-dotenv']})"
python -m black --line-length 100 src\ai\model_profiles.py src\ai\llm_client.py scripts\model_profile.py tests\test_model_profiles.py
python -m unittest discover -s tests -p test_model_profiles.py -v
python -m ruff check src\ai\model_profiles.py src\ai\llm_client.py scripts\model_profile.py tests\test_model_profiles.py
python scripts\model_profile.py list
python scripts\model_profile.py show
```

Profile `use` is exercised by the tests in temporary directories; no local model
selection or real model IDs were created for Sean. The Grok source hash before
and after this work is
`54DB713AC7F521B743766FAE06C091813E6FBB6EE4434DED8100ED44D7FED50D`.
Legacy model defaults, return values, and `query()` behavior remain unchanged.
The new client does not read legacy `LLM_PROVIDER` or heavy/light model variables.
Live account access, model availability and provider acceptance remain untested
because this task explicitly prohibits paid calls.

For OpenRouter reasoning models, a profile may set `reasoning_effort` to one of
`none`, `minimal`, `low`, `medium`, `high`, `xhigh`, or `max`. Use `none` for
strictly structured resume/cover selection when a model's hidden reasoning would
otherwise consume the completion budget; use `low` when limited reasoning is
useful. The runner requests that reasoning be excluded from returned text while
OpenRouter still reports its usage.

Final validation: **27 tests passed**, Ruff passed, and Black reported all four
Python files unchanged after formatting. The local config ignore rule was verified
with `git check-ignore -v config/model_profiles.local.json`. Only read-only Git
inspection was used (`git status --short -- .env.example .gitignore config src/ai
scripts/model_profile.py tests/test_model_profiles.py`); nothing was staged or committed.
Grok compatibility was also checked using
`Get-FileHash -LiteralPath 'src\ai\grok_client.py' -Algorithm SHA256 | Format-List Hash`.

## API references

Request construction follows the official [OpenAI Chat Completions API](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create)
and [structured-output guide](https://developers.openai.com/api/docs/guides/structured-outputs).
OpenRouter's endpoint capability requirement is documented in its
[structured-output guide](https://openrouter.ai/docs/guides/features/structured-outputs).
xAI documents its [OpenAI-compatible chat interface](https://docs.x.ai/developers/rest-api-reference/inference/chat)
and [structured outputs](https://docs.x.ai/developers/model-capabilities/text/structured-outputs).
