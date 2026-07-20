"""Command-line interface for Repo Readiness."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from dataclasses import asdict
from typing import Any

from repo_readiness.checks import ReadinessCheck, evaluate, format_checks, score
from repo_readiness.github import GitHubError, fetch_repository


def percentage(value: str) -> int:
    """Parse a percentage accepted by ``--fail-under``."""
    try:
        result = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be an integer from 0 to 100") from exc
    if not 0 <= result <= 100:
        raise argparse.ArgumentTypeError("must be an integer from 0 to 100")
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="repo-readiness",
        description="Show a compact metadata summary for a public GitHub repository.",
    )
    parser.add_argument("repository", help="GitHub repository in owner/name format")
    parser.add_argument(
        "--json",
        action="store_true",
        help="emit structured JSON for automation",
    )
    parser.add_argument(
        "--fail-under",
        type=percentage,
        metavar="SCORE",
        help="exit with status 1 when readiness is below SCORE",
    )
    return parser


def format_summary(repository: dict[str, object]) -> str:
    description = repository.get("description") or "(no description)"
    state = "archived" if repository.get("archived") else "active"
    lines = [
        str(repository["full_name"]),
        f"  {description}",
        f"  state: {state}",
        f"  default branch: {repository['default_branch']}",
        f"  stars: {repository['stargazers_count']}",
        f"  forks: {repository['forks_count']}",
        f"  open issues: {repository['open_issues_count']}",
    ]
    return "\n".join(lines)


def build_json_report(
    repository: dict[str, Any],
    checks: list[ReadinessCheck],
) -> dict[str, object]:
    """Build the stable, machine-readable report shape."""
    return {
        "repository": repository["full_name"],
        "url": repository["html_url"],
        "score": score(checks),
        "checks": [asdict(check) for check in checks],
    }


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        repository = fetch_repository(args.repository)
    except (GitHubError, ValueError) as exc:
        build_parser().error(str(exc))
    checks = evaluate(repository)
    readiness_score = score(checks)

    if args.json:
        print(json.dumps(build_json_report(repository, checks), indent=2, sort_keys=True))
    else:
        print(format_summary(repository))
        print()
        print(format_checks(checks))

    if args.fail_under is not None and readiness_score < args.fail_under:
        return 1
    return 0
