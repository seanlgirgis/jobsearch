"""Offline runtime-profile tests using isolated copies of source evidence."""

from __future__ import annotations

import io
import json
import shutil
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

import yaml

from scripts.build_runtime_profile import (
    FOUNDATIONS,
    PROFILE_PATH,
    REPORT_PATH,
    REQUIRED,
    ROOT,
    RuntimeProfileError,
    build_profile,
    canonical,
    main,
    validate_runtime_profile,
)


class RuntimeProfileTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for relative in REQUIRED.values():
            destination = self.root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, destination)
        self.director = self.root / "director"
        self.director.mkdir()
        # Synthetic private biography must never appear in generated context.
        (self.director / "SEAN.md").write_text(
            "| Name | Sean Example | confirmed |\n"
            "| Lives | Murphy, TX, USA | confirmed |\n"
            "| Employer | LTIMindtree (LTM) | confirmed |\n"
            "| Private note | synthetic-private-detail | private |\n",
            encoding="utf-8",
        )
        (self.director / "SEAN_NOW.md").write_text(
            "Private context: synthetic-current-note", encoding="utf-8"
        )
        self.network_guard = patch(
            "socket.socket.connect", side_effect=AssertionError("Network prohibited")
        )
        self.network_guard.start()
        self.addCleanup(self.network_guard.stop)

    def build(self) -> tuple[dict, str]:
        return build_profile(self.root, self.director)

    def cli(self, *options: str) -> tuple[int, str, str]:
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            code = main(["--root", str(self.root), "--director-dir", str(self.director), *options])
        return code, stdout.getvalue(), stderr.getvalue()

    def test_deterministic_compact_profile_and_readonly_sources(self) -> None:
        before = {relative: (self.root / relative).read_bytes() for relative in REQUIRED.values()}
        first, first_report = self.build()
        second, second_report = self.build()
        self.assertEqual(canonical(first), canonical(second))
        self.assertEqual(first_report, second_report)
        self.assertLess(len(canonical(first)), 12000)
        self.assertEqual(len(first["bullet_bank"]), 13)
        for relative, original in before.items():
            self.assertEqual((self.root / relative).read_bytes(), original)

    def test_identity_whitelist_uses_director_and_omits_private_context(self) -> None:
        profile, report = self.build()
        self.assertEqual(profile["identity"]["name"], "Sean Example")
        self.assertEqual(profile["identity"]["location"], "Murphy, TX, USA")
        self.assertEqual(set(profile["identity"]), {"name", "location", "email", "phone"})
        for excluded in [
            "synthetic-private-detail",
            "synthetic-current-note",
            "https://",
            "linkedin.com",
            "bofa",
        ]:
            self.assertNotIn(excluded, canonical(profile).decode().casefold())
        self.assertNotIn("synthetic-private-detail", report)
        self.assertIn("director_identity", report)

    def test_missing_optional_director_uses_only_master_identity(self) -> None:
        profile, report = build_profile(self.root, self.root / "absent")
        master = yaml.safe_load((self.root / REQUIRED["career"]).read_text(encoding="utf-8"))
        self.assertEqual(profile["identity"]["name"], master["personal"]["name"])
        self.assertEqual(profile["identity"]["location"], master["personal"]["location"])
        self.assertIn("optional source absent", report)

    def test_every_required_source_missing_fails_clearly(self) -> None:
        for relative in REQUIRED.values():
            with self.subTest(source=relative):
                path = self.root / relative
                saved = path.read_bytes()
                path.unlink()
                with self.assertRaisesRegex(RuntimeProfileError, "Required source missing"):
                    self.build()
                path.write_bytes(saved)
        self.assertFalse((self.root / PROFILE_PATH).exists())

    def test_unconfirmed_current_title_dates_metrics_and_research(self) -> None:
        profile, _ = self.build()
        current = next(item for item in profile["evidence"] if item["kind"] == "current")
        self.assertEqual(current["employer"], "LTIMindtree")
        for key in ("official_title", "start_date", "end_date"):
            self.assertIsNone(current[key])
        current_text = " ".join(
            bullet["text"] for bullet in profile["bullet_bank"] if bullet["evidence"] == "current"
        )
        self.assertNotRegex(current_text, r"\d")
        self.assertIn("research/investigation, not production", current_text)
        self.assertNotIn("CAPTAIN", current_text)
        self.assertIn("CAPTAIN", profile["public_safety"]["research"])

    def test_supported_skill_tiers_and_foundational_caps(self) -> None:
        profile, _ = self.build()
        self.assertIn("Python", profile["skill_tiers"]["professional_evidence"]["Expert"])
        self.assertIn("C++", profile["skill_tiers"]["historical_evidence"]["Expert"])
        self.assertEqual(profile["skill_tiers"]["foundational_only"], FOUNDATIONS)
        self.assertNotIn('"years"', canonical(profile).decode())
        path = self.root / REQUIRED["skills"]
        rows = yaml.safe_load(path.read_text(encoding="utf-8"))
        next(row for row in rows if row["name"] == "Databricks").update(
            proficiency="Expert", years=20
        )
        path.write_text(yaml.safe_dump(rows), encoding="utf-8")
        rebuilt, _ = self.build()
        self.assertEqual(rebuilt["skill_tiers"], profile["skill_tiers"])

    def test_selected_skill_changes_flow_from_source_without_copying_notes(self) -> None:
        path = self.root / REQUIRED["skills"]
        rows = yaml.safe_load(path.read_text(encoding="utf-8"))
        next(row for row in rows if row["name"] == "Python").update(
            proficiency="Advanced", notes="synthetic-private-skill-note"
        )
        path.write_text(yaml.safe_dump(rows), encoding="utf-8")
        profile, _ = self.build()
        self.assertIn("Python", profile["skill_tiers"]["professional_evidence"]["Advanced"])
        self.assertNotIn("synthetic-private-skill-note", canonical(profile).decode())

    def test_changed_selected_source_stops_stale_bullets(self) -> None:
        path = self.root / REQUIRED["career"]
        source = yaml.safe_load(path.read_text(encoding="utf-8"))
        source["experience"][0]["highlights"][0] = "Unconfirmed new scale: 99,000 endpoints"
        path.write_text(yaml.safe_dump(source), encoding="utf-8")
        with self.assertRaisesRegex(RuntimeProfileError, "Selected source evidence changed"):
            self.build()

    def test_current_source_change_requires_review_but_newlines_are_portable(self) -> None:
        path = self.root / REQUIRED["current_work"]
        original = path.read_text(encoding="utf-8")
        path.write_bytes(original.replace("\n", "\r\n").encode("utf-8"))
        self.build()
        path.write_text(original + "\nsynthetic-private-new-work\n", encoding="utf-8")
        with self.assertRaisesRegex(
            RuntimeProfileError, "Current-work evidence changed"
        ) as failure:
            self.build()
        self.assertNotIn("synthetic-private-new-work", str(failure.exception))

    def test_positioning_cannot_upgrade_career_evidence(self) -> None:
        baseline, _ = self.build()
        path = self.root / REQUIRED["positioning"]
        path.write_text(
            path.read_text(encoding="utf-8")
            + "\nInvented expert production model-training career: 100 years.\n",
            encoding="utf-8",
        )
        profile, _ = self.build()
        self.assertEqual(profile, baseline)

    def test_client_variants_are_blocked_without_echoing_them(self) -> None:
        baseline, _ = self.build()
        for client in [
            "Bank of America",
            "BofA",
            "B.O.F.A.",
            "BOA",
            "Ｂａｎｋ ｏｆ Ａｍｅｒｉｃａ",
            "Bank\u200bof\u200bAmerica",
        ]:
            with self.subTest(client=client):
                profile = deepcopy(baseline)
                profile["identity"]["name"] = client
                with self.assertRaisesRegex(
                    RuntimeProfileError, "Prohibited client wording"
                ) as failure:
                    validate_runtime_profile(profile)
                self.assertNotIn(client, str(failure.exception))

    def test_urls_paths_credentials_and_private_fields_are_blocked(self) -> None:
        baseline, _ = self.build()
        for value in [
            "https://example.invalid",
            "internal.local",
            "D:\\private\\data",
            "sk-syntheticsecret0000",
            "xai-syntheticsecret0000",
        ]:
            profile = deepcopy(baseline)
            profile["identity"]["location"] = value
            with self.assertRaisesRegex(
                RuntimeProfileError, "Prohibited URL, file path or credential"
            ):
                validate_runtime_profile(profile)
        profile = deepcopy(baseline)
        profile["identity"]["age"] = 99
        with self.assertRaisesRegex(RuntimeProfileError, "Only public"):
            validate_runtime_profile(profile)

    def test_safety_rules_foundation_aliases_and_research_cannot_be_removed(self) -> None:
        baseline, _ = self.build()
        profile = deepcopy(baseline)
        profile["public_safety"].pop("research")
        with self.assertRaisesRegex(RuntimeProfileError, "public-safety"):
            validate_runtime_profile(profile)
        for alias in ["DLT", "Azure", "Databricks"]:
            profile = deepcopy(baseline)
            profile["skill_tiers"]["professional_evidence"]["Expert"].append(alias)
            with self.assertRaisesRegex(RuntimeProfileError, "must not be promoted"):
                validate_runtime_profile(profile)
        profile = deepcopy(baseline)
        next(b for b in profile["bullet_bank"] if b["id"] == "current_research")[
            "text"
        ] = "Built a production chatbot."
        with self.assertRaisesRegex(RuntimeProfileError, "explicitly qualified"):
            validate_runtime_profile(profile)

    def test_builder_and_check_preserve_sources_and_detect_tampering(self) -> None:
        self.assertEqual(self.cli()[0], 0)
        original = (self.root / PROFILE_PATH).read_bytes()
        report = (self.root / REPORT_PATH).read_bytes()
        self.assertEqual(self.cli("--check")[0], 0)
        self.assertEqual(self.cli()[0], 0)
        self.assertEqual((self.root / PROFILE_PATH).read_bytes(), original)
        self.assertEqual((self.root / REPORT_PATH).read_bytes(), report)
        profile = json.loads(original)
        profile["identity"]["name"] = "Another Name"
        (self.root / PROFILE_PATH).write_bytes(canonical(profile) + b"\n")
        code, _, error = self.cli("--check")
        self.assertEqual(code, 2)
        self.assertIn("stale or altered", error)

    def test_failed_validation_does_not_replace_existing_derived_files(self) -> None:
        self.assertEqual(self.cli()[0], 0)
        output, report = self.root / PROFILE_PATH, self.root / REPORT_PATH
        before = (output.read_bytes(), report.read_bytes())
        path = self.director / "SEAN.md"
        path.write_text("| Name | BofA | confirmed |\n", encoding="utf-8")
        code, _, error = self.cli()
        self.assertEqual(code, 2)
        self.assertIn("Prohibited client wording", error)
        self.assertEqual((output.read_bytes(), report.read_bytes()), before)

    def test_check_missing_artifacts_is_readonly(self) -> None:
        code, _, error = self.cli("--check")
        self.assertEqual(code, 2)
        self.assertIn("Derived profile or report is missing", error)
        self.assertFalse((self.root / PROFILE_PATH).exists())


if __name__ == "__main__":
    unittest.main()
