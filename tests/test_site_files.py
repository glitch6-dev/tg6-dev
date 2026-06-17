from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_standard_files_exist():
    for f in ["robots.txt", "sitemap.xml", "favicon.svg", "README.md"]:
        assert (ROOT / f).exists(), f"missing {f}"


def test_index_links_favicon():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    assert "favicon.svg" in html


def test_readme_has_golive_checklist():
    rm = (ROOT / "README.md").read_text(encoding="utf-8").lower()
    assert "stripe" in rm
    assert "apps script" in rm or "endpoint" in rm
    assert "domain" in rm
