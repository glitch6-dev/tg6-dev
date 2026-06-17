from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APPLY = ROOT / "apply.html"

FIELDS = ["name", "email", "background", "goal", "project", "timeline", "why"]


def test_apply_exists():
    assert APPLY.exists()


def test_form_present():
    html = APPLY.read_text(encoding="utf-8")
    assert 'id="applyForm"' in html


def test_all_named_fields_present():
    html = APPLY.read_text(encoding="utf-8")
    for f in FIELDS:
        assert f'name="{f}"' in html, f"missing field {f}"


def test_honeypot_present():
    html = APPLY.read_text(encoding="utf-8")
    assert 'name="company_url"' in html


def test_endpoint_placeholder_and_nocors():
    html = APPLY.read_text(encoding="utf-8")
    assert "PASTE_APPS_SCRIPT_URL" in html
    assert 'mode: "no-cors"' in html


def test_no_price_or_checkout_on_apply():
    html = APPLY.read_text(encoding="utf-8").lower()
    assert "$2,999" not in html  # application page sells the call, not the price
    assert "data-checkout" not in html
