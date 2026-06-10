from src.calculator.ecosystem_scores import build_ecosystem_scores
from src.models.comparison import CardResult
from src.models.profile import ResolvedProfile


def calculate(card: dict, profile: ResolvedProfile, rules: dict) -> CardResult:
    spend = profile.annual_spend
    rakuten_spend = profile.rakuten_annual_spend
    general_spend = spend - rakuten_spend

    base_rate = card["base_rate"]
    market_rate = card.get("rakuten_market_rate", base_rate)

    base_points = int(general_spend * base_rate)
    rakuten_points = int(rakuten_spend * market_rate)
    total_points = base_points + rakuten_points

    annual_fee = card["annual_fee"]["standard"]
    effective_rate = total_points / spend if spend > 0 else 0.0

    notes = []
    if rakuten_spend > 0:
        notes.append("楽天市場等3%還元を反映（+1%期間限定分は含まず）")

    pp_free = 5
    if profile.pp_usage_count > pp_free:
        notes.append(f"PP利用{profile.pp_usage_count}回: 6回目以降US$35/回")

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
