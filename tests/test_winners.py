import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.calculator.effective_rate import calculate_all
from src.models.profile import UserProfile, resolve_profile
from src.ui.winners import get_axis_winners


def test_effective_rate_winner():
    profile = resolve_profile(UserProfile(annual_spend=1_000_000, epos_million_achieved=True))
    results = calculate_all(
        ["epos-platinum", "rakuten-premium", "paypay-gold"],
        profile,
    )
    from src.data_loader import load_cards

    cards = load_cards()
    winners = get_axis_winners(
        "effective_rate",
        list(results.keys()),
        results,
        cards,
    )
    assert winners
    assert "paypay-gold" in winners or "epos-platinum" in winners
