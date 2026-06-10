from src.calculator.ecosystem_scores import build_ecosystem_scores
from src.models.comparison import CardResult
from src.models.profile import ResolvedProfile


def calculate(card: dict, profile: ResolvedProfile, rules: dict) -> CardResult:
    spend = profile.annual_spend
    base_rate = card["base_rate"]
    overseas_rate = card.get("overseas_rate", base_rate)

    overseas_estimate = profile.overseas_trips * 200_000
    overseas_estimate = min(overseas_estimate, int(spend * 0.3))
    domestic_spend = spend - overseas_estimate

    base_points = int(domestic_spend * base_rate)
    overseas_points = int(overseas_estimate * overseas_rate)
    total_points = base_points + overseas_points

    annual_fee = card["annual_fee"]["standard"]
    effective_rate = total_points / spend if spend > 0 else 0.0

    notes = [
        "還元率のみの試算。ラウンジ・保険・ホテル特典は旅行軸で別途比較",
    ]
    if profile.overseas_trips > 0:
        notes.append(f"海外旅行{profile.overseas_trips}回分の利用を反映（1回20万円想定）")
    if profile.amex_mile_exchange:
        notes.append("マイル交換利用時は実質価値が変動します")

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
