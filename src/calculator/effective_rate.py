from __future__ import annotations

from src.calculator import amex, dcard, epos, epos_gold, epos_standard, generic, jcb, paypay, rakuten
from src.calculator.category_enrich import enrich_category_fields
from src.data_loader import load_cards, load_rules
from src.models.comparison import CardResult
from src.models.profile import ResolvedProfile

CALCULATOR_BY_TYPE = {
    "epos": epos.calculate,
    "epos_gold": epos_gold.calculate,
    "epos_standard": epos_standard.calculate,
    "rakuten": rakuten.calculate,
    "dcard": dcard.calculate,
    "paypay": paypay.calculate,
    "amex": amex.calculate,
    "jcb": jcb.calculate,
    "generic": generic.calculate,
}

ANCHOR_ID = "epos-platinum"
MAX_COMPARE_CARDS = 8


def get_available_card_ids() -> list[str]:
    return list(load_cards().keys())


def calculate_card(card_id: str, profile: ResolvedProfile) -> CardResult:
    cards = load_cards()
    rules = load_rules()
    if card_id not in cards:
        raise ValueError(f"Unknown card: {card_id}")
    card = cards[card_id]
    calc_type = card.get("calculator", "generic")
    calculator = CALCULATOR_BY_TYPE.get(calc_type, generic.calculate)
    result = calculator(card, profile, rules)
    return enrich_category_fields(card, profile, result)


def calculate_all(card_ids: list[str], profile: ResolvedProfile) -> dict[str, CardResult]:
    ordered = [ANCHOR_ID] + [c for c in card_ids if c != ANCHOR_ID]
    seen = set()
    results = {}
    for card_id in ordered:
        if card_id in seen:
            continue
        seen.add(card_id)
        results[card_id] = calculate_card(card_id, profile)
    return results


def effective_rate_curve(
    card_id: str,
    profile: ResolvedProfile,
    steps: list[int] | None = None,
) -> list[tuple[int, float]]:
    from dataclasses import replace

    from src.models.profile import resolve_profile, UserProfile

    if steps is None:
        steps = list(range(300_000, 5_100_000, 200_000))

    base_user = UserProfile(
        annual_spend=profile.annual_spend,
        ecosystems=profile.ecosystems,
        rakuten_annual_spend=profile.rakuten_annual_spend or None,
        docomo_monthly_fee=profile.docomo_monthly_fee or None,
        paypay_monthly_count=profile.paypay_monthly_count or None,
        yahoo_annual_spend=profile.yahoo_annual_spend or None,
        marui_annual_spend=profile.marui_annual_spend or None,
        amazon_annual_spend=profile.amazon_annual_spend or None,
        aeon_annual_spend=profile.aeon_annual_spend or None,
        overseas_trips=profile.overseas_trips,
        pp_usage_count=profile.pp_usage_count,
        has_family_card=profile.has_family_card,
        family_annual_spend=profile.family_annual_spend,
        epos_invite=profile.epos_invite,
        epos_million_achieved=profile.epos_million_achieved,
        birth_month_spend=profile.birth_month_spend,
        paypay_step_achieved=profile.paypay_step_achieved,
        amex_mile_exchange=profile.amex_mile_exchange,
        supermarket_heavy=profile.supermarket_annual_spend > int(profile.annual_spend * 0.18),
        convenience_heavy=profile.convenience_annual_spend > int(profile.annual_spend * 0.12),
        has_car=profile.has_car,
        supermarket_annual_spend=profile.supermarket_annual_spend or None,
        convenience_annual_spend=profile.convenience_annual_spend or None,
        mode="detail" if profile.rakuten_annual_spend else "quick",
    )

    curve = []
    for spend in steps:
        user = replace(
            base_user,
            annual_spend=spend,
            epos_million_achieved=spend >= 1_000_000,
        )
        resolved = resolve_profile(user)
        result = calculate_card(card_id, resolved)
        curve.append((spend, result.effective_rate))
    return curve
