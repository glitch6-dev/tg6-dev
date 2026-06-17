from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GS = ROOT / "apps-script" / "Code.gs"


def test_codegs_exists():
    assert GS.exists()


def test_applications_tab_and_headers():
    src = GS.read_text(encoding="utf-8")
    assert "Applications" in src
    for col in ["Name", "Email", "Background", "Goal", "Project", "Timeline", "Why"]:
        assert col in src, f"missing header {col}"


def test_honeypot_drop():
    src = GS.read_text(encoding="utf-8")
    assert "company_url" in src


def test_has_doget_and_dopost():
    src = GS.read_text(encoding="utf-8")
    assert "function doPost" in src
    assert "function doGet" in src


def test_no_hardcoded_sheet_id_or_gmail():
    src = GS.read_text(encoding="utf-8")
    # NOTIFY_EMAIL must be the public proton address, not a private gmail
    assert "dvelupr@proton.me" in src
    assert "gmail.com" not in src
    assert "spreadsheets/d/" not in src  # no private Sheet URL/ID committed
