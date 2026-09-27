"""Contract tests for the dependency freshness check.

The check is only useful if a red line means "someone has to look". Two things
can make that false: a false alarm that fires every month until people stop
reading the report, and a silencing move that hides a real gap. These tests pin
both edges -- the declared-precision comparison, and the two documented exits
(hold and deferral) with the deferral expiring by itself -- across both
declaration sources this repo actually has: PyPI dev dependencies and pinned
GitHub Actions.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import check_dependency_freshness as checker  # noqa: E402


def test_comparison_uses_the_precision_the_declaration_states() -> None:
    # `>=7` says nothing about the minor, so 7.4.0 must not be a monthly alarm.
    assert not checker.is_newer_version("7.4.0", "7")
    assert checker.is_newer_version("8.0.0", "7")
    assert checker.is_newer_version("7.4.0", "7.3")
    assert not checker.is_newer_version("7.3.2", "7.3")


def test_prerelease_suffix_does_not_count_as_newer() -> None:
    assert not checker.is_newer_version("7.0.0rc1", "7.0.0")


def test_leading_v_is_stripped_for_github_action_tags() -> None:
    assert checker.is_newer_version("v7.1.0", "7.0.1")
    assert not checker.is_newer_version("v7.0.1", "7.0.1")


def test_hold_marker_is_read_off_the_declaring_line() -> None:
    packages = checker.parse_requirements(
        "pytest>=8.3  # freshness-hold: pinned for a documented reason\n"
        "ruff>=0.16\n",
        "requirements-dev.txt",
    )

    holds = {package["name"]: package["hold"] for package in packages}
    assert holds["ruff"] == ""
    assert holds["pytest"].startswith("pinned for a documented reason")


def test_workflow_actions_are_parsed_with_their_declared_version() -> None:
    text = (
        "jobs:\n"
        "  test:\n"
        "    steps:\n"
        "      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1\n"
        "      - uses: actions/setup-node@820762786026740c76f36085b0efc47a31fe5020 # v7.0.0\n"
    )

    packages = checker.parse_workflow_actions(text, "ci.yml")

    by_name = {p["name"]: p for p in packages}
    assert by_name["actions/checkout"]["minimum"] == "7.0.1"
    assert by_name["actions/checkout"]["source"] == "ci.yml"
    assert by_name["actions/checkout"]["hold"] == ""


def test_workflow_action_hold_marker_is_read_off_the_uses_line() -> None:
    text = (
        "      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1"
        " # freshness-hold: pinned for a documented reason\n"
    )

    packages = checker.parse_workflow_actions(text, "ci.yml")

    assert packages[0]["hold"] == "pinned for a documented reason"
    assert packages[0]["minimum"] == ""


def test_real_workflows_declare_at_least_one_pinned_action() -> None:
    actions = checker.load_workflow_actions()

    assert len(actions) >= 3
    assert all(a["minimum"] or a["hold"] for a in actions)


def test_a_held_floor_is_reported_but_does_not_ask_for_work() -> None:
    packages = checker.parse_requirements(
        "pytest>=8.3  # freshness-hold: CI still tests an older Python\n",
        "requirements-dev.txt",
    )

    rows = checker.collect_status(packages, lambda _name: "9.1.0", deferrals={})

    assert rows[0]["outdated"] is True
    assert checker.needs_review(rows[0]) is False
    assert "HELD: CI still tests an older Python" in checker.render_markdown(rows)


def test_a_live_deferral_covers_the_row_and_says_what_it_was_reviewed_against() -> None:
    packages = checker.parse_requirements("pytest>=8.3\n", "requirements-dev.txt")

    rows = checker.collect_status(
        packages,
        lambda _name: "9.1.0",
        deferrals={"pytest": ("9.1", "reviewed 2026-08; wait for the 9.x line to settle")},
    )

    assert checker.needs_review(rows[0]) is False
    assert "DEFERRED at 9.1.0" in checker.render_markdown(rows)


def test_a_deferral_expires_once_the_upstream_source_moves_past_the_reviewed_release() -> None:
    """This is the whole point of `deferredLatest`: it cannot become a mute button."""
    packages = checker.parse_requirements("pytest>=8.3\n", "requirements-dev.txt")

    rows = checker.collect_status(
        packages, lambda _name: "10.0.0", deferrals={"pytest": ("9.1", "not this month")}
    )

    assert checker.needs_review(rows[0]) is True
    assert "REVIEW UPDATE" in checker.render_markdown(rows)


def test_deferral_without_a_reviewed_release_is_ignored(tmp_path: Path) -> None:
    path = tmp_path / "dependency-deferrals.json"
    path.write_text(
        json.dumps(
            {
                "deferrals": {
                    "kept": {"deferredLatest": "9.1", "reason": "reviewed, not now"},
                    "no-release": {"reason": "reviewed, not now"},
                    "no-reason": {"deferredLatest": "9.1"},
                }
            }
        ),
        encoding="utf-8",
    )

    assert checker.load_deferrals(path) == {"kept": ("9.1", "reviewed, not now")}


def test_missing_deferrals_file_is_not_an_error(tmp_path: Path) -> None:
    assert checker.load_deferrals(tmp_path / "nope.json") == {}


def test_report_names_both_exits_so_the_next_person_does_not_invent_a_third() -> None:
    report = checker.render_markdown([], [])

    assert "freshness-hold:" in report
    assert "dependency-deferrals.json" in report
    assert "mute button" in report


def test_report_has_a_section_for_each_declaration_source() -> None:
    report = checker.render_markdown([], [])

    assert "Python dev dependencies" in report
    assert "GitHub Actions" in report


def test_subdirectory_actions_are_tracked_and_resolved_to_their_repository() -> None:
    """`github/codeql-action/init` is an action; its releases live on the repo."""
    text = (
        "      - uses: github/codeql-action/init@f205ea1c3313d32999d8d6a48b4f6530d4437b38"
        " # v4.37.4\n"
    )

    packages = checker.parse_workflow_actions(text, "codeql.yml")

    assert packages[0]["name"] == "github/codeql-action/init"
    assert packages[0]["minimum"] == "4.37.4"
    assert checker.action_repository(packages[0]["name"]) == "github/codeql-action"
    assert checker.action_repository("actions/checkout") == "actions/checkout"


def test_codeql_pins_are_in_the_real_report() -> None:
    """Regression guard: the owner/repo-only pattern skipped every CodeQL pin."""
    names = {action["name"] for action in checker.load_workflow_actions()}

    assert any(name.startswith("github/codeql-action/") for name in names)


def test_an_uncomparable_latest_is_a_failed_check_not_an_ok() -> None:
    """`codeql-bundle-v2.26.4` shares no numbering with the pinned `v4.37.4`."""
    packages = checker.parse_workflow_actions(
        "      - uses: github/codeql-action/init@f205ea1c # v4.37.4\n", "codeql.yml"
    )

    rows = checker.collect_status(
        packages, lambda _name: "codeql-bundle-v2.26.4", deferrals={}
    )

    assert rows[0]["check_failed"] is True
    assert "CHECK FAILED" in checker.render_markdown([], rows)


def test_a_token_is_sent_when_the_environment_has_one(monkeypatch) -> None:
    """Anonymous api.github.com is 60/hour and hosted runners share it."""
    seen: dict[str, str] = {}

    class _Response:
        def __enter__(self):
            return self

        def __exit__(self, *_exc) -> None:
            return None

        def read(self) -> bytes:
            return b'{"tag_name": "v7.0.1"}'

    def fake_urlopen(request, timeout=None):  # noqa: ARG001
        seen.update(request.headers)
        return _Response()

    monkeypatch.setattr(checker.urllib.request, "urlopen", fake_urlopen)

    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    monkeypatch.delenv("GH_TOKEN", raising=False)
    assert checker.fetch_github_release("actions/checkout") == "7.0.1"
    assert not any(key.lower() == "authorization" for key in seen)

    seen.clear()
    monkeypatch.setenv("GITHUB_TOKEN", "secret-token")
    checker.fetch_github_release("actions/checkout")
    authorization = next(value for key, value in seen.items() if key.lower() == "authorization")
    assert authorization == "Bearer secret-token"
