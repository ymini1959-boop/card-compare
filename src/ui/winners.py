from __future__ import annotations

from src.models.comparison import CardResult
from src.ui.benefit_scores import score_card_axis

BENEFIT_AXES = {
    "priority_pass",
    "lounge",
    "travel_insurance",
    "concierge",
}

HIGHER_BETTER_AXES = {
    "effective_rate",
    "base_rate",
    "supermarket_rate",
    "convenience_rate",
    "gasoline_rate",
    "daily_effective_rate",
    "annual_bonus",
    "car_insurance",
    "rakuten_fit",
    "docomo_fit",
    "paypay_fit",
    "marui_fit",
    "yahoo_fit",
    "amazon_fit",
    "aeon_fit",
    "brands",
    "point_expiry",
    *BENEFIT_AXES,
}

LOWER_BETTER_AXES = {"annual_fee", "effective_annual_fee", "family_card_fee"}


def score_cell(axis_id: str, card: dict, result: CardResult) -> float | None:
    return score_card_axis(card, axis_id, result)


def get_axis_winners(
    axis_id: str,
    card_ids: list[str],
    results: dict,
    cards_data: dict,
) -> list[str]:
    scores: dict[str, float] = {}
    for cid in card_ids:
        score = score_cell(axis_id, cards_data[cid], results[cid])
        if score is None:
            return []
        scores[cid] = score

    if axis_id in LOWER_BETTER_AXES:
        best = min(scores.values())
    else:
        best = max(scores.values())

    if best <= 0 and axis_id in BENEFIT_AXES | {"mobile_pay", "brands"}:
        return []

    return [cid for cid, s in scores.items() if s == best]


def compute_win_counts(
    selected_axes: list[str],
    card_ids: list[str],
    results: dict,
    cards_data: dict,
) -> tuple[dict[str, int], dict[str, list[str]], int]:
    counts = {cid: 0 for cid in card_ids}
    axis_winners: dict[str, list[str]] = {}

    for axis_id in selected_axes:
        winners = get_axis_winners(axis_id, card_ids, results, cards_data)
        axis_winners[axis_id] = winners
        if not winners or len(winners) == len(card_ids):
            continue
        for w in winners:
            counts[w] += 1

    comparable_count = sum(
        1
        for aid in selected_axes
        if axis_winners.get(aid) and len(axis_winners[aid]) < len(card_ids)
    )
    return counts, axis_winners, comparable_count
