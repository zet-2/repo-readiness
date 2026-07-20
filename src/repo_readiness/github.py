"""Small GitHub REST API client built on the Python standard library."""

from __future__ import annotations

import json
import os
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class GitHubError(RuntimeError):
    """Raised when repository metadata cannot be fetched."""


def parse_repository(value: str) -> tuple[str, str]:
    """Return the owner and repository components of an ``owner/repo`` slug."""
    parts = value.strip().strip("/").split("/")
    if len(parts) != 2 or not all(parts):
        raise ValueError("repository must use the owner/name format")
    return parts[0], parts[1]


def fetch_repository(value: str, timeout: float = 10.0) -> dict[str, Any]:
    """Fetch public metadata for a GitHub repository."""
    owner, name = parse_repository(value)
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "repo-readiness/0.1",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = Request(
        f"https://api.github.com/repos/{owner}/{name}",
        headers=headers,
    )

    try:
        with urlopen(request, timeout=timeout) as response:
            return json.load(response)
    except HTTPError as exc:
        if exc.code == 404:
            raise GitHubError(f"repository not found: {owner}/{name}") from exc
        raise GitHubError(f"GitHub returned HTTP {exc.code}") from exc
    except URLError as exc:
        raise GitHubError(f"could not reach GitHub: {exc.reason}") from exc
