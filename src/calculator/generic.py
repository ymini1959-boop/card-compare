from src.calculator.ecosystem_scores import build_ecosystem_scores
from src.models.comparison import CardResult
from src.models.profile import ResolvedProfile


def calculate(card: dict, profile: ResolvedProfile, rules: dict) -> CardResult:
    spend = profile.annual_spend
    base_rate = card["base_rate"]

    shop_rate = card.get("shop_bonus_rate", 0)
    shop_spend = 0
    if card.get("shop_bonus_key") == "amazon":
        shop_spend = profile.amazon_annual_spend
    elif card.get("shop_bonus_key") == "aeon":
        shop_spend = profile.aeon_annual_spend

    general = max(0, spend - shop_spend)
    total_points = int(general * base_rate)
    if shop_spend > 0 and shop_rate:
        total_points += int(shop_spend * shop_rate)

    bonus_yen = 0
    for tier in sorted(card.get("annual_bonus_tiers", []), key=lambda t: t["min_spend"]):
        if spend >= tier["min_spend"]:
            bonus_yen = max(bonus_yen, tier.get("bonus_yen", tier.get("bonus_points", 0)))

    total_points += bonus_yen
    annual_fee = card["annual_fee"]["standard"]
    effective_rate = total_points / spend if spend > 0 else 0.0

    notes = []
    if bonus_yen > 0:
        notes.append(f"年間特典 {bonus_yen:,}円相当を反映")

    return CardResult(
        card_id=card["id"],
        card_name=card["name"],
        effective_rate=effective_rate,
        effective_annual_fee=annual_fee,
        annual_bonus_points=bonus_yen,
        annual_bonus_yen=bonus_yen,
        total_points_value=total_points,
        ecosystem_scores=build_ecosystem_scores(card, profile),
        notes=notes,
        static_values=card,
    )
