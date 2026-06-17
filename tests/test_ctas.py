import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "index.html").read_text(encoding="utf-8")


def _tier_block(n):
    # Grab the <article ... data-tier="n"> ... </article> chunk
    m = re.search(rf'data-tier="{n}".*?</article>', HTML, re.DOTALL)
    assert m, f"tier {n} block not found"
    return m.group(0)


def test_tier3_cta_links_to_apply():
    block = _tier_block("3")
    assert 'href="apply.html"' in block


def test_tier3_has_no_checkout():
    block = _tier_block("3")
    assert "data-checkout" not in block, "Tier 3 must be application-based, not checkout"


def test_tier1_and_2_have_checkout_hooks():
    assert 'data-checkout="1"' in _tier_block("1")
    assert 'data-checkout="2"' in _tier_block("2")


def test_stripe_placeholders_present():
    assert "TIER1_CHECKOUT_URL" in HTML
    assert "TIER2_CHECKOUT_URL" in HTML
    assert "PASTE_STRIPE_LINK" in HTML
