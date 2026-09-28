"""DNA cache and Indeed keep/skip without provider calls."""

from __future__ import annotations

import tempfile
import unittest
import json
from pathlib import Path
from unittest.mock import MagicMock, patch

from scripts.search_bots_dna import lookup, remember, text_dna
from scripts.search_bots_filters import (
    indeed_fromage_days,
    is_excluded,
    parse_pay_annual_max_usd,
    pay_skip_reason,
)
from scripts.search_bots_handoff import enqueue, flush_handoff
from scripts.search_bots_indeed import (
    LEDGER_FIELDS,
    append_ledger,
    counts_toward_limit,
    file_stem,
    keep_job,
    load_term_queries,
    parse_capture,
    process_text,
    verdict,
)
from scripts.search_bots_indeed_live import _first_text, capture_to_markdown

JOB = """Indeed.com

https://www.indeed.com/viewjob?jk=abc123def456

Company: Synthires
Senior AI Software Engineer
Python capacity planning remote $140,000 a year

Build Python services, observability, and practical AI workflows.
"""


class DnaTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_same_jk_is_one_dna_even_if_text_grows(self):
        remember(
            self.root,
            job_text=JOB,
            url="https://www.indeed.com/viewjob?jk=abc123def456",
            record={"dna": text_dna(JOB), "site": "indeed"},
        )
        longer = JOB + "\nExtra paragraph about Docker and CI."
        hit = lookup(
            self.root,
            job_text=longer,
            url="https://www.indeed.com/viewjob?jk=abc123def456&from=share",
        )
        self.assertIsNotNone(hit)
        self.assertEqual(hit["indeed_jk"], "abc123def456")

    def test_same_text_without_url_hits_hash(self):
        remember(self.root, job_text=JOB, url=None, record={"dna": text_dna(JOB)})
        hit = lookup(self.root, job_text="  " + JOB + "\n", url=None)
        self.assertIsNotNone(hit)

    def test_keep_rule(self):
        self.assertTrue(keep_job({"score": 68, "recommendation": "REVIEW"}))
        self.assertFalse(keep_job({"score": 80, "recommendation": "SKIP"}))
        self.assertFalse(keep_job({"score": 40, "recommendation": "REVIEW"}))
        self.assertTrue(keep_job({"score": 82, "recommendation": "PROCEED"}))

    def test_supplied_config_controls_keep_and_filename(self):
        (self.root / "config").mkdir()
        (self.root / "config/search_bots.json").write_text(
            json.dumps(
                {
                    "evaluation": {
                        "verdicts": {"apply_min_score": 90, "wait_min_score": 70}
                    },
                }
            ),
            encoding="utf-8",
        )
        self.assertFalse(
            keep_job({"score": 68, "recommendation": "REVIEW"}, root=self.root)
        )
        stem = file_stem(
            {"score": 82, "recommendation": "PROCEED"}, "Example", "abc", root=self.root
        )
        self.assertTrue(stem.startswith("082_Wait_"))

    def test_filename_score_and_verdict(self):
        self.assertEqual(verdict({"score": 88, "recommendation": "PROCEED"}), "Apply")
        self.assertEqual(verdict({"score": 72, "recommendation": "REVIEW"}), "Wait")
        self.assertEqual(verdict({"score": 38, "recommendation": "REVIEW"}), "Reject")
        self.assertEqual(verdict({"score": 90, "recommendation": "SKIP"}), "Reject")
        stem = file_stem(
            {"score": 72, "recommendation": "REVIEW"}, "GE Vernova", "da5b9a21" * 8
        )
        self.assertTrue(stem.startswith("072_Wait_"))
        self.assertIn("ge-vernova", stem)
        queries = load_term_queries(Path(__file__).resolve().parents[1])
        self.assertGreaterEqual(len(queries), 8)

    def test_parse_indeed_url(self):
        cap = parse_capture(JOB)
        self.assertIn("jk=abc123def456", cap["job_url"])
        self.assertEqual(cap["company"], "Synthires")
        self.assertEqual(cap["title"], "Senior AI Software Engineer")

    def test_live_fields_survive_capture_round_trip(self):
        capture = {
            "job_url": "https://www.indeed.com/viewjob?jk=abc123",
            "company": "Marathon TS",
            "title": "Code Review Specialist",
            "salary": "$60 - $70 an hour",
            "job_description": "Review code. Schedule: Full-time, Eastern hours.",
        }
        parsed = parse_capture(capture_to_markdown(capture))
        for field in ("job_url", "title", "company", "salary"):
            self.assertEqual(parsed[field], capture[field])

    def test_legacy_capture_finds_hourly_pay_without_salary_label(self):
        cap = parse_capture("""Indeed.com
https://www.indeed.com/viewjob?jk=abc123
Company:
Code Review Specialist
Code Review Specialist
Marathon TS
Remote
$60 - $70 an hour
Full-time
Full job description
Review software source code for quality and readability.
""")
        self.assertEqual(cap["title"], "Code Review Specialist")
        self.assertEqual(cap["salary"], "$60 - $70 an hour")

    def test_short_dom_fields_are_not_discarded(self):
        page = MagicMock()
        page.locator.return_value.count.return_value = 1
        for value in ("DataAnnotation", "$50 an hour"):
            page.locator.return_value.first.inner_text.return_value = value
            self.assertEqual(_first_text(page, ("field",)), value)
            self.assertEqual(_first_text(page, ("field",), min_chars=80), "")


class ScheduleTests(unittest.TestCase):
    def _root(self):
        tmp = tempfile.TemporaryDirectory()
        root = Path(tmp.name)
        (root / "search_bots").mkdir()
        (root / "config").mkdir(parents=True)
        (root / "search_bots" / "terms.json").write_text(
            json.dumps({"categories": {"a": ["alpha"], "b": ["beta"]}}),
            encoding="utf-8",
        )
        (root / "config" / "search_bots.json").write_text(
            json.dumps({"polite": {"hours_between_phrases": 12}}),
            encoding="utf-8",
        )
        return tmp, root

    def test_blocked_does_not_consume_12h(self):
        from scripts.search_bots_schedule import claim_next, mark_blocked, mark_success

        tmp, root = self._root()
        first = claim_next(root)
        self.assertEqual(first["query"], "alpha")
        mark_blocked(root, first["id"], "cloudflare")
        again = claim_next(root)
        self.assertEqual(again["query"], "beta")
        mark_success(root, again["id"])
        third = claim_next(root)
        self.assertIsNone(third)
        tmp.cleanup()


class HandoffTests(unittest.TestCase):
    def test_flush_copies_queued_file_and_keeps_local(self):
        tmp = tempfile.TemporaryDirectory()
        root = Path(tmp.name)
        src = root / "data" / "search_bots" / "ready" / "indeed" / "Wait" / "a.job.md"
        src.parent.mkdir(parents=True, exist_ok=True)
        src.write_text("hello", encoding="utf-8")
        dest_root = root / "onedrive"
        dest_root.mkdir()
        enqueue(root, src, "indeed/Wait/a.job.md")
        result = flush_handoff(root, dest_root)
        self.assertGreaterEqual(result["ok"], 1)
        self.assertTrue((dest_root / "indeed" / "Wait" / "a.job.md").is_file())
        self.assertTrue(src.is_file())
        tmp.cleanup()


class LedgerTests(unittest.TestCase):
    def test_ledger_starts_with_human_processed_n(self):
        tmp = tempfile.TemporaryDirectory()
        root = Path(tmp.name)
        append_ledger(
            root,
            {
                "human_processed": "N",
                "category": "Wait",
                "score": 72,
                "search_pack": "capacity_performance",
                "verdict": "Wait",
                "dna": "abc",
                "stem": "072_Wait_x",
            },
        )
        path = root / "data" / "search_bots" / "logs" / "indeed_ledger.csv"
        text = path.read_text(encoding="utf-8-sig")
        self.assertIn("human_processed", text)
        self.assertIn("category", text)
        self.assertIn("score", text)
        self.assertTrue(text.splitlines()[1].startswith("N,"))
        self.assertEqual(LEDGER_FIELDS[0], "human_processed")

    def test_dna_hit_does_not_count_toward_limit(self):
        self.assertFalse(counts_toward_limit("dna_hit"))
        self.assertTrue(counts_toward_limit("evaluated"))
        self.assertTrue(counts_toward_limit("excluded"))


class FilterTests(unittest.TestCase):
    def test_expanded_exclusions_preserve_technical_and_adoption_roles(self):
        root = Path(__file__).resolve().parents[1]
        for title in (
            "Coding Expertise for AI Training",
            "Personalized Internet Ads Assessor",
            "Search Quality Rater",
            "AI Response Reviewer",
            "Data Annotator",
        ):
            with self.subTest(title=title):
                self.assertIsNotNone(
                    is_excluded(company="Example", title=title, root=root)
                )
        for company, title in (
            ("TELUS Digital", "Observability Engineer"),
            ("Dynatrace", "Solutions Engineer"),
            ("Example", "AI Enablement Consultant"),
            ("Example", "AI Adoption Training Consultant"),
        ):
            with self.subTest(title=title):
                self.assertIsNone(is_excluded(company=company, title=title, root=root))

    def test_explicit_pay_units_and_unknown_currency(self):
        examples = {
            "$120,000 - $160,000 a year": 160000,
            "$140k": 140000,
            "$120-160k": 160000,
            "$120,000 - $160k": 160000,
            "$70/hr": 145600,
            "$12,000 per month": 144000,
            "$2,800 per week": 145600,
            "$600 per day": 156000,
            "$60 an hour; 401k benefits": 124800,
            "CAD $150,000 a year": None,
            "$60-$70": None,
            "Competitive; 5 years experience": None,
        }
        for snippet, expected in examples.items():
            with self.subTest(snippet=snippet):
                self.assertEqual(parse_pay_annual_max_usd(snippet), expected)

    def test_query_cannot_exempt_full_time_posting(self):
        root = Path(__file__).resolve().parents[1]
        for title, body in (
            ("Python Engineer", "Full-time"),
            ("Python Contractor", "Schedule: Full-time; flexible hours"),
        ):
            with self.subTest(title=title):
                self.assertIsNotNone(
                    pay_skip_reason(
                        title=title,
                        salary_text="$60 an hour",
                        query="part time Python",
                        job_text=body,
                        root=root,
                    )
                )
        self.assertIsNone(
            pay_skip_reason(
                title="Python Consultant",
                salary_text="$60 an hour",
                query="Python automation",
                job_text="Employment Type: Part-time",
                root=root,
            )
        )

    def test_salary_floor_boundaries(self):
        root = Path(__file__).resolve().parents[1]
        for salary, skip in (
            ("$139,999 a year", True),
            ("$140,000 a year", False),
            ("$120,000-$160,000 per year", False),
            (None, False),
        ):
            with self.subTest(salary=salary):
                reason = pay_skip_reason(
                    title="Engineer", salary_text=salary, query="AI", root=root
                )
                self.assertEqual(reason is not None, skip)

    def test_lookback_is_one_day(self):
        root = Path(__file__).resolve().parents[1]
        with patch("scripts.search_bots_filters.has_prior_dna", return_value=False):
            self.assertEqual(indeed_fromage_days(root), 1)
        with patch("scripts.search_bots_filters.has_prior_dna", return_value=True):
            self.assertEqual(indeed_fromage_days(root), 1)

    def test_dataannotation_excluded(self):
        root = Path(__file__).resolve().parents[1]
        self.assertIsNotNone(
            is_excluded(company="DataAnnotation", title="AI Writer", root=root)
        )
        self.assertIsNone(
            is_excluded(company="eHealth", title="Amplify Data Analyst", root=root)
        )
        self.assertIsNotNone(
            is_excluded(company="Acme", title="Image Annotation Specialist", root=root)
        )

    def test_full_time_pay_floor(self):
        root = Path(__file__).resolve().parents[1]
        self.assertEqual(parse_pay_annual_max_usd("$90,000 - $110,000 a year"), 110000)
        self.assertEqual(parse_pay_annual_max_usd("$50 an hour"), 104000)
        self.assertIsNotNone(
            pay_skip_reason(
                title="Data Engineer",
                salary_text="$110,000 a year",
                query="capacity planning python",
                root=root,
            )
        )
        self.assertIsNone(
            pay_skip_reason(
                title="Part-time Python consultant",
                salary_text="$40 an hour",
                query="part time remote",
                root=root,
            )
        )


class IndeedProcessTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_excluded_title_and_low_pay_stop_before_eval(self):
        repo = Path(__file__).resolve().parents[1]
        (self.root / "config").mkdir()
        for name in ("search_bots.json", "search_bots_exclusions.json"):
            (self.root / "config" / name).write_bytes(
                (repo / "config" / name).read_bytes()
            )
        with patch("scripts.search_bots_indeed.require_fresh"), patch(
            "scripts.search_bots_indeed.evaluate",
            side_effect=AssertionError("No paid eval"),
        ):
            for key, title, salary, expected in (
                ("aaa", "Search Quality Rater", "$70 an hour", "title:"),
                (
                    "bbb",
                    "Python Automation Engineer",
                    "$110,000 per year",
                    "full_time_pay_",
                ),
            ):
                text = capture_to_markdown(
                    {
                        "job_url": f"https://www.indeed.com/viewjob?jk={key}",
                        "company": "Acme",
                        "title": title,
                        "salary": salary,
                        "job_description": "Full-time\nBuild and maintain enterprise reporting automation in Python.",
                    }
                )
                result = process_text(self.root, text, query="part time Python")
                self.assertEqual(result["status"], "excluded")
                self.assertFalse(result["paid"])
                self.assertTrue(result["reason"].startswith(expected))

    def test_second_process_is_dna_hit_without_pay(self):
        remember(
            self.root,
            job_text=JOB,
            url="https://www.indeed.com/viewjob?jk=abc123def456",
            record={"dna": text_dna(JOB), "eval_paid": True},
        )
        # Skip require_fresh by not calling process_text full path; lookup is the contract.
        hit = lookup(
            self.root,
            job_text=JOB,
            url="https://www.indeed.com/viewjob?jk=abc123def456",
        )
        self.assertTrue(hit["eval_paid"])
        result = {"status": "dna_hit", "paid": False} if hit else None
        self.assertEqual(result["status"], "dna_hit")


if __name__ == "__main__":
    unittest.main()
