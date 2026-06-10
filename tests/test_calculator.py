import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.calculator.effective_rate import calculate_card
from src.models.profile import UserProfile, resolve_profile


def test_epos_effective_rate_at_1m():
    profile = resolve_profile(
        UserProfile(annual_spend=1_000_000, epos_million_achieved=True)
    )
    result = calculate_card("epos-platinum", profile)
    assert result.effective_annual_fee == 20_000
    assert result.effective_rate > 0.02


def test_rakuten_with_market_spend():
    profile = resolve_profile(
        UserProfile(
            mode="detail",
            annual_spend=1_000_000,
            rakuten_annual_spend=300_000,
            ecosystems=["rakuten"],
        )
    )
    result = calculate_card("rakuten-premium", profile)
    assert result.effective_rate > 0.008


def test_paypay_card_no_fee():
    profile = resolve_profile(UserProfile(annual_spend=500_000, ecosystems=["paypay"]))
    result = calculate_card("paypay-card", profile)
    assert result.effective_annual_fee == 0
