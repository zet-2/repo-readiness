"""Command-line interface for Repo Readiness."""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from repo_readiness.github import GitHubError, fetch_repository


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="repo-readiness",
        description="Show a compact metadata summary for a public GitHub repository.",
    )
    parser.add_argument("repository", help="GitHub repository in owner/name format")
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


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        repository = fetch_repository(args.repository)
    except (GitHubError, ValueError) as exc:
        build_parser().error(str(exc))
    print(format_summary(repository))
    return 0
