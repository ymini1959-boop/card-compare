from src.calculator.ecosystem_scores import build_ecosystem_scores
from src.models.comparison import CardResult
from src.models.profile import ResolvedProfile


def _epos_bonus_points(annual_spend: int, rules: dict) -> int:
    tiers = rules["epos"]["bonus_tiers"]
    bonus = 0
    for tier in sorted(tiers, key=lambda t: t["min_spend"], reverse=True):
        if annual_spend >= tier["min_spend"]:
            bonus = tier.get("bonus_points", 0)
            break
    if annual_spend < 500_000:
        bonus += int(annual_spend * rules["epos"]["under_500k_bonus_rate"])
    return bonus


def _epos_annual_fee(profile: ResolvedProfile, card: dict) -> int:
    if profile.epos_invite:
        fee = card["annual_fee"]["invite"]
    else:
        fee = card["annual_fee"]["standard"]
    if profile.epos_million_achieved or profile.annual_spend >= 1_000_000:
        fee = card["annual_fee"]["discounted"]["amount"]
    return fee


def calculate(card: dict, profile: ResolvedProfile, rules: dict) -> CardResult:
    base_rate = card["base_rate"]
    spend = profile.annual_spend

    base_points = int(spend * base_rate)
    bonus_points = _epos_bonus_points(spend, rules)

    shop_bonus = int(profile.marui_annual_spend * 0.005)
    birth_bonus = int(profile.birth_month_spend * 0.005) if profile.birth_month_spend else 0
    family_bonus = int(profile.family_annual_spend * 0.002) if profile.has_family_card else 0

    total_points = base_points + bonus_points + shop_bonus + birth_bonus + family_bonus
    annual_fee = _epos_annual_fee(profile, card)

    effective_rate = total_points / spend if spend > 0 else 0.0

    notes = []
    if profile.epos_invite:
        notes.append("招待入会（年会費2万円）を反映")
    if profile.annual_spend >= 1_000_000:
        notes.append("年間100万円以上利用で翌年年会費2万円を反映")

    return CardResult(
        card_id=card["id"],
        card_name=card["name"],
        effective_rate=effective_rate,
        effective_annual_fee=annual_fee,
        annual_bonus_points=bonus_points,
        annual_bonus_yen=bonus_points,
        total_points_value=total_points,
        ecosystem_scores=build_ecosystem_scores(card, profile),
        notes=notes,
        static_values=card,
    )
