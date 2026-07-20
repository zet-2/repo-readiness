"""Repository readiness checks."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReadinessCheck:
    """The result of one repository hygiene check."""

    key: str
    label: str
    passed: bool
    advice: str


def evaluate(repository: dict[str, object]) -> list[ReadinessCheck]:
    """Evaluate lightweight hygiene signals exposed by repository metadata."""
    return [
        ReadinessCheck(
            key="description",
            label="Repository has a description",
            passed=bool(repository.get("description")),
            advice="Add a concise description in repository settings.",
        ),
        ReadinessCheck(
            key="license",
            label="Repository declares a license",
            passed=bool(repository.get("license")),
            advice="Add a LICENSE file recognized by GitHub.",
        ),
        ReadinessCheck(
            key="topics",
            label="Repository has discovery topics",
            passed=bool(repository.get("topics")),
            advice="Add a few specific repository topics.",
        ),
        ReadinessCheck(
            key="homepage",
            label="Repository links to a homepage",
            passed=bool(repository.get("homepage")),
            advice="Add a demo, documentation, or project homepage URL.",
        ),
        ReadinessCheck(
            key="issues",
            label="Issue tracking is enabled",
            passed=bool(repository.get("has_issues")),
            advice="Enable issues or document the preferred support channel.",
        ),
        ReadinessCheck(
            key="active",
            label="Repository is active",
            passed=not bool(repository.get("archived")),
            advice="Unarchive the repository only if it is actively maintained.",
        ),
    ]


def score(checks: list[ReadinessCheck]) -> int:
    """Return the percentage of readiness checks that pass."""
    if not checks:
        return 0
    passed = sum(check.passed for check in checks)
    return round(passed / len(checks) * 100)


def format_checks(checks: list[ReadinessCheck]) -> str:
    """Format readiness results for a terminal."""
    lines = [f"Readiness score: {score(checks)}/100"]
    for check in checks:
        marker = "x" if check.passed else " "
        lines.append(f"  [{marker}] {check.label}")
        if not check.passed:
            lines.append(f"      {check.advice}")
    return "\n".join(lines)
