import unittest

from repo_readiness.checks import evaluate, format_checks, score
from repo_readiness.cli import format_summary
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


if __name__ == "__main__":
    unittest.main()
