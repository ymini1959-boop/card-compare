from __future__ import annotations

import re

from src.models.comparison import CardResult

HIGHER_BETTER_AXES = {
    "effective_rate",
    "supermarket_rate",
    "convenience_rate",
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
}
LOWER_BETTER_AXES = {"annual_fee", "effective_annual_fee", "family_card_fee"}


def _format_rate(rate: float) -> str:
    return f"{rate * 100:.2f}%"


def _format_yen(amount: int) -> str:
    return f"{amount:,}円"


def _format_score(score: int) -> str:
    stars = "★" * (score // 20) + "☆" * (5 - score // 20)
    return f"{stars} ({score}/100)"


def parse_numeric(axis_id: str, value: str) -> float | None:
    if axis_id in {
        "effective_rate", "base_rate", "supermarket_rate",
        "convenience_rate", "daily_effective_rate",
    }:
        m = re.search(r"([\d.]+)%", value)
        return float(m.group(1)) if m else None
    if axis_id == "car_insurance":
        m = re.search(r"\((\d+)/100\)", value)
        return float(m.group(1)) if m else None
    if axis_id in {"annual_fee", "effective_annual_fee", "family_card_fee", "annual_bonus"}:
        m = re.search(r"([\d,]+)", value.replace("円相当", ""))
        return float(m.group(1).replace(",", "")) if m else None
    if axis_id.endswith("_fit"):
        m = re.search(r"\((\d+)/100\)", value)
        return float(m.group(1)) if m else None
    return None


def format_axis_value(card: dict, axis_id: str, result: CardResult) -> str:
    if axis_id == "annual_fee":
        return _format_yen(card["annual_fee"]["standard"])
    if axis_id == "effective_annual_fee":
        return _format_yen(result.effective_annual_fee)
    if axis_id == "family_card_fee":
        fee = card.get("family_card_fee", 0)
        return _format_yen(fee) if fee else "無料"
    if axis_id == "base_rate":
        return _format_rate(card["base_rate"])
    if axis_id == "effective_rate":
        return _format_rate(result.effective_rate)
    if axis_id == "annual_bonus":
        if result.annual_bonus_yen:
            return f"{result.annual_bonus_yen:,}円相当"
        return "—"
    if axis_id == "point_expiry":
        return str(card.get("point_expiry", "—"))
    if axis_id == "priority_pass":
        val = card.get("priority_pass", False)
        return str(val) if val else "なし"
    if axis_id == "lounge":
        val = card.get("lounge", False)
        return str(val) if val else "なし"
    if axis_id == "travel_insurance":
        val = card.get("travel_insurance", False)
        return str(val) if val else "なし"
    if axis_id == "supermarket_rate":
        return _format_rate(result.supermarket_rate)
    if axis_id == "convenience_rate":
        return _format_rate(result.convenience_rate)
    if axis_id == "daily_effective_rate":
        return _format_rate(result.daily_effective_rate)
    if axis_id == "car_insurance":
        if result.car_insurance_score <= 0:
            return "なし"
        stars = "★" * (result.car_insurance_score // 20) + "☆" * (
            5 - result.car_insurance_score // 20
        )
        return f"{result.car_insurance_summary} {stars} ({result.car_insurance_score}/100)"
    if axis_id == "concierge":
        val = card.get("concierge", False)
        return str(val) if val else "なし"
    if axis_id == "rakuten_fit":
        return _format_score(result.ecosystem_scores.get("rakuten", 0))
    if axis_id == "docomo_fit":
        return _format_score(result.ecosystem_scores.get("docomo", 0))
    if axis_id == "paypay_fit":
        return _format_score(result.ecosystem_scores.get("paypay", 0))
    if axis_id == "marui_fit":
        return _format_score(result.ecosystem_scores.get("marui", 0))
    if axis_id == "yahoo_fit":
        return _format_score(result.ecosystem_scores.get("yahoo", 0))
    if axis_id == "amazon_fit":
        return _format_score(result.ecosystem_scores.get("amazon", 0))
    if axis_id == "aeon_fit":
        return _format_score(result.ecosystem_scores.get("aeon", 0))
    if axis_id == "brands":
        return " / ".join(card.get("brands", []))
    if axis_id == "mobile_pay":
        return "対応" if card.get("mobile_pay") else "—"
    return "—"
