"""カード・軸・プロファイルの組み合わせで計算・勝敗集計が落ちないことを検証する。"""

from __future__ import annotations

import itertools
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.calculator.effective_rate import ANCHOR_ID, MAX_COMPARE_CARDS, calculate_all, get_available_card_ids
from src.data_loader import load_axes, load_cards
from src.models.profile import UserProfile, resolve_profile
from src.ui.automotive_axes import _merge_automotive, _valid_automotive_ids
from src.ui.benefit_scores import score_card_axis
from src.ui.winners import compute_win_counts, get_axis_winners

COMPARE_IDS = [c for c in get_available_card_ids() if c != ANCHOR_ID]
CARDS = load_cards()
AXES_DATA = load_axes()
PRESETS = AXES_DATA["presets"]
ALL_AXIS_IDS = [a["id"] for cat in AXES_DATA["categories"] for a in cat["axes"]]

TEST_PROFILES = [
    UserProfile(annual_spend=300_000),
    UserProfile(annual_spend=1_000_000),
    UserProfile(annual_spend=3_000_000, epos_million_achieved=True),
    UserProfile(annual_spend=1_200_000, supermarket_heavy=True, convenience_heavy=True),
    UserProfile(annual_spend=1_000_000, has_car=True),
    UserProfile(
        mode="detail",
        annual_spend=1_500_000,
        ecosystems=["rakuten", "paypay"],
        rakuten_annual_spend=800_000,
        paypay_monthly_count=30,
        has_car=True,
        supermarket_heavy=True,
    ),
]


def _axis_defs() -> dict[str, dict]:
    defs: dict[str, dict] = {}
    for cat in AXES_DATA["categories"]:
        for axis in cat["axes"]:
            defs[axis["id"]] = axis
    return defs


def _leader_caption_names(results: dict, leaders: list[str]) -> str:
    """render_win_summary の同率トップ表示と同じアクセスパターン。"""
    return "・".join(results[c].card_name for c in leaders)


def _run_win_pipeline(
    card_ids: list[str],
    selected_axes: list[str],
    profile: UserProfile,
) -> None:
    resolved = resolve_profile(profile)
    results = calculate_all(card_ids, resolved)
    assert len(results) == len(set(card_ids))

    counts, axis_winners, comparable_count = compute_win_counts(
        selected_axes, card_ids, results, CARDS
    )
    assert set(counts) == set(card_ids)

    for axis_id in selected_axes:
        winners = get_axis_winners(axis_id, card_ids, results, CARDS)
        assert winners == axis_winners.get(axis_id, [])

    max_count = max(counts.values()) if counts else 0
    leaders = [cid for cid, c in counts.items() if c == max_count and max_count > 0]
    if len(leaders) > 1 and comparable_count > 0:
        caption = _leader_caption_names(results, leaders)
        assert caption

    for cid in card_ids:
        assert results[cid].card_name == CARDS[cid]["name"]

    for axis_id in selected_axes:
        for cid in card_ids:
            score_card_axis(CARDS[cid], axis_id, results[cid])


@pytest.mark.parametrize("profile", TEST_PROFILES, ids=lambda p: f"spend{p.annual_spend}")
@pytest.mark.parametrize("compare_id", COMPARE_IDS)
@pytest.mark.parametrize("preset_name", list(PRESETS.keys()))
def test_pair_preset_combinations(profile, compare_id, preset_name):
    card_ids = [ANCHOR_ID, compare_id]
    axes = [a for a in PRESETS[preset_name] if a in _axis_defs()]
    _run_win_pipeline(card_ids, axes, profile)


@pytest.mark.parametrize("profile", TEST_PROFILES[:3], ids=lambda p: f"spend{p.annual_spend}")
@pytest.mark.parametrize("axis_id", ALL_AXIS_IDS)
def test_single_axis_all_pairs(profile, axis_id):
    for compare_id in COMPARE_IDS:
        _run_win_pipeline([ANCHOR_ID, compare_id], [axis_id], profile)


def test_max_cards_all_axes_preset():
    """比較上限枚数・全軸プリセットの組み合わせ。"""
    compare = COMPARE_IDS[: MAX_COMPARE_CARDS - 1]
    card_ids = [ANCHOR_ID] + compare
    profile = UserProfile(annual_spend=1_000_000, has_car=True)
    axes = PRESETS["all"]
    _run_win_pipeline(card_ids, axes, profile)


def test_automotive_axis_merge():
    valid = _valid_automotive_ids()
    merged = _merge_automotive(["effective_rate"], valid)
    assert "car_insurance" in merged
    assert "gasoline_rate" in merged
    assert merged[0] == "effective_rate"


def test_three_card_combos_sample():
    """3枚比較のサンプル（同率トップが起きやすい）。"""
    sample = COMPARE_IDS[:12]
    profile = UserProfile(annual_spend=1_000_000)
    axes = PRESETS["reward"]
    for trio in itertools.combinations(sample, 3):
        _run_win_pipeline([ANCHOR_ID, *trio], axes, profile)
