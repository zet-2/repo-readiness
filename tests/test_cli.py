import argparse
import unittest

from repo_readiness.checks import evaluate, format_checks, score
from repo_readiness.cli import build_json_report, format_summary, main, percentage
from repo_readiness.github import parse_repository


class ParseRepositoryTests(unittest.TestCase):
    def test_parses_owner_and_name(self) -> None:
        self.assertEqual(parse_repository("octocat/Hello-World"), ("octocat", "Hello-World"))

    def test_rejects_incomplete_slug(self) -> None:
        with self.assertRaisesRegex(ValueError, "owner/name"):
            parse_repository("octocat")


class FormatSummaryTests(unittest.TestCase):
    def test_formats_core_metadata(self) -> None:
        repository = {
            "full_name": "octocat/Hello-World",
            "description": "A greeting",
            "archived": False,
            "default_branch": "main",
            "stargazers_count": 10,
            "forks_count": 2,
            "open_issues_count": 1,
        }

        summary = format_summary(repository)

        self.assertIn("octocat/Hello-World", summary)
        self.assertIn("state: active", summary)
        self.assertIn("stars: 10", summary)


class ReadinessCheckTests(unittest.TestCase):
    def test_scores_repository_hygiene(self) -> None:
        repository = {
            "description": "A greeting",
            "default_branch": "main",
            "stargazers_count": 10,
            "forks_count": 2,
            "open_issues_count": 1,
            "license": {"spdx_id": "MIT"},
            "topics": ["example"],
            "homepage": "",
            "has_issues": True,
            "archived": False,
        }

        checks = evaluate(repository)

        self.assertEqual(score(checks), 83)
        self.assertIn("[ ] Repository links to a homepage", format_checks(checks))
        self.assertIn("Add a demo", format_checks(checks))

    def test_empty_check_list_has_zero_score(self) -> None:
        self.assertEqual(score([]), 0)


class AutomationOutputTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = {
            "full_name": "octocat/Hello-World",
            "html_url": "https://github.com/octocat/Hello-World",
            "description": "A greeting",
            "default_branch": "main",
            "stargazers_count": 10,
            "forks_count": 2,
            "open_issues_count": 1,
            "license": {"spdx_id": "MIT"},
            "topics": ["example"],
            "homepage": "",
            "has_issues": True,
            "archived": False,
        }

    def test_builds_json_report(self) -> None:
        report = build_json_report(self.repository, evaluate(self.repository))

        self.assertEqual(report["repository"], "octocat/Hello-World")
        self.assertEqual(report["score"], 83)
        self.assertEqual(len(report["checks"]), 6)

    def test_fail_under_returns_nonzero(self) -> None:
        from unittest.mock import patch

        with patch("repo_readiness.cli.fetch_repository", return_value=self.repository):
            with patch("builtins.print"):
                self.assertEqual(
                    main(["octocat/Hello-World", "--fail-under", "90"]),
                    1,
                )

    def test_percentage_rejects_out_of_range_value(self) -> None:
        with self.assertRaisesRegex(argparse.ArgumentTypeError, "0 to 100"):
            percentage("101")


if __name__ == "__main__":
    unittest.main()
