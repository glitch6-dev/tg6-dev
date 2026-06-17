from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(name):
    return (ROOT / name).read_text(encoding="utf-8")


def test_index_exists():
    assert (ROOT / "index.html").exists(), "index.html must exist"


def test_title_has_brand():
    html = read("index.html")
    assert "Zero to Shipping" in html, "page title/brand must say Zero to Shipping"


def test_hero_promise_present():
    html = read("index.html")
    # The core promise: ship a real, deployed project using AI
    assert "ship" in html.lower()
    assert "deployed" in html.lower() or "real project" in html.lower()


def test_no_free_tier_language():
    html = read("index.html").lower()
    assert "free lesson" not in html
    assert "free course" not in html
