from src.calculator.ecosystem_scores import build_ecosystem_scores
from src.models.comparison import CardResult
from src.models.profile import ResolvedProfile


def calculate(card: dict, profile: ResolvedProfile, rules: dict) -> CardResult:
    spend = profile.annual_spend
    base_rate = card["base_rate"]
    docomo_rate = card.get("docomo_rate", 0.10)

    docomo_annual = profile.docomo_monthly_fee * 12
    general_spend = max(0, spend - docomo_annual)

    base_points = int(general_spend * base_rate)
    docomo_points = int(docomo_annual * docomo_rate) if docomo_annual > 0 else 0

    bonus_yen = 0
    for tier in sorted(card.get("annual_bonus_tiers", []), key=lambda t: t["min_spend"]):
        if spend >= tier["min_spend"]:
            bonus_yen = max(bonus_yen, tier.get("bonus_yen", tier.get("bonus_points", 0)))

    total_points = base_points + docomo_points + bonus_yen
    annual_fee = card["annual_fee"]["standard"]
    effective_rate = total_points / spend if spend > 0 else 0.0

    notes = []
    if docomo_annual > 0:
        notes.append("ドコモ料金10%還元を反映")
    if bonus_yen > 0:
        notes.append(f"年間利用特典 {bonus_yen:,}円相当を反映")

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
