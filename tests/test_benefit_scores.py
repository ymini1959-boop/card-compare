import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.calculator.effective_rate import calculate_all, effective_rate_curve
from src.data_loader import load_cards
from src.models.profile import UserProfile, resolve_profile
from src.ui.benefit_scores import score_priority_pass
from src.ui.winners import get_axis_winners


def test_epos_beats_rakuten_on_priority_pass():
    cards = load_cards()
    epos = score_priority_pass(cards["epos-platinum"])
    rakuten = score_priority_pass(cards["rakuten-premium"])
    assert epos > rakuten

    profile = resolve_profile(UserProfile(annual_spend=1_000_000))
    results = calculate_all(["epos-platinum", "rakuten-premium"], profile)
    winners = get_axis_winners(
        "priority_pass", list(results.keys()), results, cards
    )
    assert winners == ["epos-platinum"]


def test_brands_axis_has_winner():
    cards = load_cards()
    profile = resolve_profile(UserProfile(annual_spend=1_000_000))
    results = calculate_all(["epos-platinum", "rakuten-premium"], profile)
    winners = get_axis_winners("brands", list(results.keys()), results, cards)
    assert winners == ["rakuten-premium"]


def test_effective_rate_curve_epos_jumps_at_1m():
    profile = resolve_profile(
        UserProfile(annual_spend=1_000_000, epos_million_achieved=True)
    )
    curve = effective_rate_curve("epos-platinum", profile, steps=[900_000, 1_000_000, 1_100_000])
    rates = {spend: rate for spend, rate in curve}
    assert rates[1_000_000] >= rates[900_000]
