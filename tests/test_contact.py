import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_contact_page_exists():
    assert (ROOT / "contact.html").exists()


def test_contact_form_and_honeypot():
    html = (ROOT / "contact.html").read_text(encoding="utf-8")
    assert 'id="contactForm"' in html
    assert 'name="company_url"' in html  # spam honeypot


def test_contact_endpoint_is_live():
    html = (ROOT / "contact.html").read_text(encoding="utf-8")
    m = re.search(r'ENDPOINT\s*=\s*"([^"]+)"', html)
    assert m, "no ENDPOINT constant"
    assert m.group(1).startswith("https://script.google.com/macros/s/")
    assert m.group(1).endswith("/exec")


def test_contact_no_stale_domain():
    html = (ROOT / "contact.html").read_text(encoding="utf-8")
    assert "glitch6-dev.github.io" not in html


def test_contact_backend_present_and_clean():
    gs = (ROOT / "apps-script" / "contact" / "Code.gs").read_text(encoding="utf-8")
    assert "Leads" in gs
    for col in ["Name", "Email", "Business", "Service", "Budget", "Message"]:
        assert col in gs, f"missing header {col}"
    assert "function doPost" in gs and "function doGet" in gs
    assert "dvelupr@proton.me" in gs
    assert "gmail.com" not in gs
    assert "spreadsheets/d/" not in gs  # no private Sheet id committed
