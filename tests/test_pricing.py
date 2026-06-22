import re
from pathlib import Path

# Pricing tiers live on the dedicated AI Training catalogue page; index.html is
# now the digital-services storefront.
ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "ai-training.html").read_text(encoding="utf-8")


def test_all_three_prices_present():
    assert "$49" in HTML
    assert "$499" in HTML
    assert "$2,999" in HTML


def test_all_three_tier_names():
    assert "Build It" in HTML
    assert "Ship It" in HTML
    assert "Get Launched" in HTML


def test_exactly_three_tier_cards():
    assert len(re.findall(r'data-tier="', HTML)) == 3


def test_tiers_are_data_tagged():
    for n in ("1", "2", "3"):
        assert f'data-tier="{n}"' in HTML


def test_tier2_value_props_present():
    # The $499 jump is justified by support/access
    low = HTML.lower()
    assert "discord" in low
    assert "coaching" in low or "feedback" in low


def test_tier3_is_one_on_one_limited():
    low = HTML.lower()
    assert "1-on-1" in low or "1:1" in low or "one-on-one" in low
    assert "limited" in low or "seats" in low
