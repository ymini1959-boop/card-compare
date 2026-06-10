from __future__ import annotations

import re

from src.models.comparison import CardResult


def _truthy(val: object) -> bool:
    if not val:
        return False
    if val is True:
        return True
    text = str(val).strip()
    return text not in ("", "なし", "False", "false")


def _max_numbers(text: str) -> int:
    nums = [int(n) for n in re.findall(r"(\d+)", text.replace(",", ""))]
    return max(nums) if nums else 0


def score_priority_pass(card: dict) -> float:
    val = card.get("priority_pass", False)
    if not _truthy(val):
        return 0.0
    text = str(val)
    if any(k in text for k in ("制限なし", "無制限", "回数制限なし")):
        return 100.0
    m = re.search(r"年(\d+)回", text)
    if m:
        free_count = int(m.group(1))
        return min(92.0, 30.0 + free_count * 12.0)
    if "無料" in text:
        return 75.0
    return 40.0


def score_lounge(card: dict) -> float:
    val = card.get("lounge", False)
    if not _truthy(val):
        return 0.0
    text = str(val)
    scale = _max_numbers(text)
    if scale <= 0:
        return 55.0
    return min(100.0, 25.0 + (scale ** 0.55) * 3.2)


def score_concierge(card: dict) -> float:
    return 100.0 if _truthy(card.get("concierge")) else 0.0


def score_travel_insurance(card: dict) -> float:
    val = card.get("travel_insurance", False)
    if not _truthy(val):
        return 0.0
    text = str(val)
    if "国内" in text and "海外" in text:
        base = 60.0
    else:
        base = 45.0
    nums = _max_numbers(text)
    if "億" in text and nums:
        return min(100.0, base + nums * 25.0)
    if "万" in text and nums:
        return min(100.0, base + nums / 80.0)
    return base


def score_brands(card: dict) -> float:
    return float(len(card.get("brands", [])))


def score_point_expiry(card: dict) -> float:
    text = str(card.get("point_expiry", ""))
    if "永久" in text:
        return 100.0
    if "実質無期限" in text:
        return 85.0
    if text and text not in ("—", ""):
        return 50.0
    return 0.0


BENEFIT_SCORERS = {
    "priority_pass": score_priority_pass,
    "lounge": score_lounge,
    "concierge": score_concierge,
    "travel_insurance": score_travel_insurance,
}


def score_card_axis(card: dict, axis_id: str, result: CardResult) -> float | None:
    if axis_id == "effective_rate":
        return result.effective_rate * 100.0
    if axis_id == "base_rate":
        return card["base_rate"] * 100.0
    if axis_id == "supermarket_rate":
        return result.supermarket_rate * 100.0
    if axis_id == "convenience_rate":
        return result.convenience_rate * 100.0
    if axis_id == "daily_effective_rate":
        return result.daily_effective_rate * 100.0
    if axis_id == "annual_bonus":
        return float(result.annual_bonus_yen)
    if axis_id == "annual_fee":
        return float(card["annual_fee"]["standard"])
    if axis_id == "effective_annual_fee":
        return float(result.effective_annual_fee)
    if axis_id == "family_card_fee":
        return float(card.get("family_card_fee", 0))
    if axis_id == "car_insurance":
        return float(result.car_insurance_score)
    if axis_id.endswith("_fit"):
        return float(result.ecosystem_scores.get(axis_id.replace("_fit", ""), 0))
    if axis_id in BENEFIT_SCORERS:
        return BENEFIT_SCORERS[axis_id](card)
    if axis_id == "brands":
        return score_brands(card)
    if axis_id == "mobile_pay":
        return 1.0 if card.get("mobile_pay") else 0.0
    if axis_id == "point_expiry":
        return score_point_expiry(card)
    return None
