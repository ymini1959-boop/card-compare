from __future__ import annotations

from src.ui.axis_values import (
    HIGHER_BETTER_AXES,
    LOWER_BETTER_AXES,
    format_axis_value,
    parse_numeric,
)

BENEFIT_AXES = {
    "priority_pass",
    "lounge",
    "travel_insurance",
    "concierge",
}

COMPARABLE_AXES = (
    HIGHER_BETTER_AXES
    | LOWER_BETTER_AXES
    | BENEFIT_AXES
    | {"mobile_pay", "point_expiry"}
)


def _benefit_score(value: str) -> float:
    if not value or value in ("なし", "—", "False"):
        return 0.0
    return float(len(value))


def score_cell(axis_id: str, value: str) -> float | None:
    if axis_id in HIGHER_BETTER_AXES or axis_id in LOWER_BETTER_AXES:
        return parse_numeric(axis_id, value)
    if axis_id in BENEFIT_AXES:
        return _benefit_score(value)
    if axis_id == "mobile_pay":
        return 1.0 if value == "対応" else 0.0
    if axis_id == "point_expiry":
        if "永久" in value:
            return 3.0
        if "実質無期限" in value:
            return 2.5
        return 1.0 if value not in ("—", "") else 0.0
    if axis_id == "car_insurance":
        return parse_numeric(axis_id, value)
    return None


def get_axis_winners(
    axis_id: str,
    card_ids: list[str],
    results: dict,
    cards_data: dict,
) -> list[str]:
    scores: dict[str, float] = {}
    for cid in card_ids:
        card = cards_data[cid]
        value = format_axis_value(card, axis_id, results[cid])
        score = score_cell(axis_id, value)
        if score is None:
            return []
        scores[cid] = score

    if axis_id in LOWER_BETTER_AXES:
        best = min(scores.values())
    else:
        best = max(scores.values())

    if best <= 0 and axis_id in BENEFIT_AXES | {"mobile_pay"}:
        return []

    return [cid for cid, s in scores.items() if s == best]


def compute_win_counts(
    selected_axes: list[str],
    card_ids: list[str],
    results: dict,
    cards_data: dict,
) -> tuple[dict[str, int], dict[str, list[str]]]:
    counts = {cid: 0 for cid in card_ids}
    axis_winners: dict[str, list[str]] = {}

    for axis_id in selected_axes:
        winners = get_axis_winners(axis_id, card_ids, results, cards_data)
        axis_winners[axis_id] = winners
        if not winners or len(winners) == len(card_ids):
            continue
        for w in winners:
            counts[w] += 1

    return counts, axis_winners
