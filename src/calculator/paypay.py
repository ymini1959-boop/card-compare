from src.calculator.ecosystem_scores import build_ecosystem_scores
from src.models.comparison import CardResult
from src.models.profile import ResolvedProfile


def calculate(card: dict, profile: ResolvedProfile, rules: dict) -> CardResult:
    spend = profile.annual_spend
    base_rate = card["base_rate"]
    step_rate = card.get("step_max_rate", base_rate)
    yahoo_rate = card.get("yahoo_rate", step_rate)

    rate = step_rate if profile.paypay_step_achieved else base_rate
    yahoo_spend = profile.yahoo_annual_spend
    general_spend = max(0, spend - yahoo_spend)

    total_points = int(general_spend * rate)
    if yahoo_spend > 0:
        total_points += int(yahoo_spend * yahoo_rate)

    bonus_points = 0
    for tier in card.get("annual_bonus_tiers", []):
        if spend >= tier["min_spend"]:
            bonus_points = tier.get("bonus_points", 0)

    if card["id"] == "paypay-gold" and spend >= 1_000_000:
        total_points += bonus_points

    annual_fee = card["annual_fee"]["standard"]
    effective_rate = total_points / spend if spend > 0 else 0.0

    notes = []
    if profile.paypay_step_achieved:
        notes.append("PayPayステップ達成（最大1.5%）を反映")
    if yahoo_spend > 0:
        notes.append("Yahoo!ショッピング利用分を反映")
    if bonus_points > 0:
        notes.append(f"年間100万円特典 {bonus_points:,}ptを反映")

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
