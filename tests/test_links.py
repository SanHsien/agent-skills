from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import check_links  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def test_maintainer_markdown_links_resolve() -> None:
    failures = 0
    for path in check_links.iter_documents():
        problems = check_links.check_document(path)
        failures += len(problems)
        for problem in problems:
            print(f"{path}: {problem}")
    assert failures == 0


def test_iter_documents_covers_root_and_docs_but_not_product_dirs() -> None:
    documents = check_links.iter_documents()
    names = {path.name for path in documents}

    assert "README.md" in names
    assert "FORK.md" in names
    assert "DEVELOPMENT.md" in names

    scanned_dirs = {path.parent.name for path in documents}
    assert "skills" not in scanned_dirs
    assert "commands" not in scanned_dirs
    assert "agents" not in scanned_dirs
    assert "references" not in scanned_dirs
    assert "evals" not in scanned_dirs
    assert "scripts" not in scanned_dirs


def test_check_links_rejects_path_outside_repo(tmp_path: Path) -> None:
    doc = tmp_path / "note.md"
    doc.write_text("[here](.)\n", encoding="utf-8")
    problems = check_links.check_document(doc)
    assert any("逃出" in item for item in problems)


def test_check_links_reports_a_missing_target(tmp_path: Path, monkeypatch: object) -> None:
    # ROOT is patched to tmp_path so the target resolves *inside* the fake
    # root and hits the "missing" branch rather than the "escapes the repo"
    # branch exercised by test_check_links_rejects_path_outside_repo above.
    monkeypatch.setattr(check_links, "ROOT", tmp_path)
    doc = tmp_path / "note.md"
    doc.write_text("[gone](./does-not-exist.md)\n", encoding="utf-8")
    problems = check_links.check_document(doc)
    assert any("找不到" in item for item in problems)


def test_check_links_ignores_external_and_anchor_links(tmp_path: Path) -> None:
    doc = tmp_path / "note.md"
    doc.write_text(
        "[web](https://example.com) [mail](mailto:a@example.com) [anchor](#section)\n",
        encoding="utf-8",
    )
    problems = check_links.check_document(doc)
    assert problems == []


def test_bilingual_readmes_cross_link_each_other() -> None:
    zh = (ROOT / "README.md").read_text(encoding="utf-8")
    en = (ROOT / "README.en.md").read_text(encoding="utf-8")

    assert "README.en.md" in zh
    assert "README.md" in en


def test_link_title_is_not_part_of_the_path(tmp_path: Path) -> None:
    # `[text](path "title")` is standard Markdown; the title is not a filename.
    doc = ROOT / "docs" / "_title_probe.md"
    doc.write_text('[a](../FORK.md "title") [b](<../FORK.md>)\n', encoding="utf-8")
    try:
        assert check_links.check_document(doc) == []
    finally:
        doc.unlink()


def test_links_inside_code_are_examples_not_links() -> None:
    doc = ROOT / "docs" / "_code_probe.md"
    doc.write_text(
        "```md\n[x](does-not-exist.md)\n```\n\nInline `[y](also-missing.md)` too.\n",
        encoding="utf-8",
    )
    try:
        assert check_links.check_document(doc) == []
    finally:
        doc.unlink()


def test_missing_link_outside_code_is_still_reported() -> None:
    doc = ROOT / "docs" / "_real_probe.md"
    doc.write_text("```\n[x](a.md)\n```\n[z](missing-real.md)\n", encoding="utf-8")
    try:
        problems = check_links.check_document(doc)
    finally:
        doc.unlink()
    assert len(problems) == 1 and "missing-real.md" in problems[0]
