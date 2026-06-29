from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_recurring_costs_exists():
    assert (ROOT / "recurring-costs.html").exists()


def test_recurring_costs_clean_and_linked():
    html = (ROOT / "recurring-costs.html").read_text(encoding="utf-8")
    assert "glitch6-dev.github.io" not in html
    assert 'href="contact.html"' in html
    index = (ROOT / "index.html").read_text(encoding="utf-8")
    assert "recurring-costs.html" in index  # footer-linked from home
