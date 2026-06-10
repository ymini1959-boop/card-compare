from __future__ import annotations

from src.models.comparison import CardResult
from src.models.profile import ResolvedProfile


def _category_rate(card: dict, key: str) -> float:
    rates = card.get("category_rates", {})
    return float(rates.get(key, card["base_rate"]))


def enrich_category_fields(
    card: dict, profile: ResolvedProfile, result: CardResult
) -> CardResult:
    sm_rate = _category_rate(card, "supermarket")
    cv_rate = _category_rate(card, "convenience")
    sm_spend = profile.supermarket_annual_spend
    cv_spend = profile.convenience_annual_spend
    daily_spend = sm_spend + cv_spend

    result.supermarket_rate = sm_rate
    result.convenience_rate = cv_rate

    if daily_spend > 0:
        daily_points = int(sm_spend * sm_rate) + int(cv_spend * cv_rate)
        result.daily_effective_rate = daily_points / daily_spend
    else:
        result.daily_effective_rate = max(sm_rate, cv_rate)

    car_info = card.get("car_insurance", {})
    result.car_insurance_score = int(car_info.get("score", 0))
    result.car_insurance_summary = str(car_info.get("summary", "なし"))
    return result
