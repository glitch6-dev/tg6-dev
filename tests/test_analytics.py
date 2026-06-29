from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# recurring-costs.html is added in a later task; it is asserted there.
PAGES = ["index.html", "ai-training.html", "apply.html",
         "privacy.html", "terms.html", "404.html", "contact.html"]


def test_ga4_on_all_pages():
    for p in PAGES:
        html = (ROOT / p).read_text(encoding="utf-8")
        assert "G-BJK86RFN9N" in html, f"GA4 missing on {p}"
