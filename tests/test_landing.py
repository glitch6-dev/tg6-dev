from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(name):
    return (ROOT / name).read_text(encoding="utf-8")


def test_index_exists():
    assert (ROOT / "index.html").exists(), "index.html must exist"


def test_title_has_brand():
    html = read("index.html")
    assert "TG6-Dev" in html, "page title/brand must say TG6-Dev"
    assert "AI Training" in html, "page brand must say AI Training"


def test_hero_promise_present():
    html = read("index.html").lower()
    # The core promise: go from a browser chat to shipping with Claude Code
    assert "ship" in html
    assert "claude code" in html
    assert "chat" in html


def test_claude_code_named_on_landing():
    html = read("index.html").lower()
    assert "claude code" in html, "the ladder must name Claude Code"


def test_services_catalog_present():
    html = read("index.html")
    # curated digital-services catalogue; AI Training is one card among many
    assert "Custom Software" in html
    assert "Security &amp; Pentest" in html
    assert 'href="ai-training.html#pricing"' in html  # AI Training is one service
    assert 'href="contact.html' in html               # CTAs route to the form


def test_no_free_tier_language():
    html = read("index.html").lower()
    assert "free lesson" not in html
    assert "free course" not in html
