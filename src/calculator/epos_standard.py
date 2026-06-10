from src.calculator.ecosystem_scores import build_ecosystem_scores
from src.models.comparison import CardResult
from src.models.profile import ResolvedProfile


def calculate(card: dict, profile: ResolvedProfile, rules: dict) -> CardResult:
    spend = profile.annual_spend
    base_rate = card["base_rate"]
    total_points = int(spend * base_rate)
    shop_bonus = int(profile.marui_annual_spend * 0.005)

    total_points += shop_bonus
    annual_fee = card["annual_fee"]["standard"]
    effective_rate = total_points / spend if spend > 0 else 0.0

    notes = []
    if profile.marui_annual_spend > 0:
        notes.append("マルイ系列ボーナスを簡易反映")

    return CardResult(
        card_id=card["id"],
        card_name=card["name"],
        effective_rate=effective_rate,
        effective_annual_fee=annual_fee,
        annual_bonus_points=0,
        annual_bonus_yen=0,
        total_points_value=total_points,
        ecosystem_scores=build_ecosystem_scores(card, profile),
        notes=notes,
        static_values=card,
    )
