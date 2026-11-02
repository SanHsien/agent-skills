"""Regression contracts for corrected upstream documentation examples."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_error_boundary_declares_children_props():
    text = (ROOT / "skills/shipping-and-launch/SKILL.md").read_text(encoding="utf-8")
    assert "extends React.Component<React.PropsWithChildren>" in text


def test_large_text_contrast_uses_css_pixel_equivalent():
    text = (ROOT / "references/accessibility-checklist.md").read_text(encoding="utf-8")
    assert "18pt / 24 CSS px" in text
    assert "14pt / about 18.67 CSS px when bold" in text
    assert "Do not round a failing contrast ratio up" in text


def test_resize_measurements_wait_for_fonts_and_observers():
    text = (ROOT / "skills/browser-testing-with-devtools/SKILL.md").read_text(encoding="utf-8")
    assert "measure layout only after fonts and resize observers have settled" in text
