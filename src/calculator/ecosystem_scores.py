from __future__ import annotations

from src.models.profile import ResolvedProfile

ALL_ECOSYSTEMS = ("rakuten", "docomo", "paypay", "marui", "yahoo", "amazon", "aeon")

DEFAULT_AFFINITY = {
    "rakuten": 15,
    "docomo": 15,
    "paypay": 15,
    "marui": 15,
    "yahoo": 15,
    "amazon": 15,
    "aeon": 15,
}


def build_ecosystem_scores(card: dict, profile: ResolvedProfile) -> dict[str, int]:
    scores = dict(DEFAULT_AFFINITY)
    scores.update(card.get("ecosystem_affinity", {}))

    spend = profile.annual_spend or 1
    spend_map = {
        "rakuten": profile.rakuten_annual_spend,
        "yahoo": profile.yahoo_annual_spend,
        "marui": profile.marui_annual_spend,
        "amazon": profile.amazon_annual_spend,
        "aeon": profile.aeon_annual_spend,
        "docomo": profile.docomo_monthly_fee * 12,
        "paypay": profile.paypay_monthly_count * 12 * 500,
    }

    for eco, amount in spend_map.items():
        if amount > 0:
            scores[eco] = min(100, 45 + int(amount / spend * 55))

    if profile.paypay_monthly_count >= 30 and "paypay" in profile.ecosystems:
        scores["paypay"] = min(100, scores.get("paypay", 15) + 20)

    for eco in profile.ecosystems:
        if spend_map.get(eco, 0) == 0:
            scores[eco] = min(100, scores.get(eco, 15) + 15)

    return scores
