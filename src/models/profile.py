from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

ECO_DEFAULT_SHARE = {
    "rakuten": 0.28,
    "docomo": 0.14,
    "paypay": 0.22,
    "marui": 0.18,
    "yahoo": 0.12,
    "amazon": 0.20,
    "aeon": 0.16,
}

PRIORITY_OPTIONS = {
    "cost": "コスト・年会費",
    "reward": "還元率・ポイント",
    "travel": "旅行・空港特典",
    "ecosystem": "経済圏との相性",
    "insurance": "保険・補償",
    "family": "家族カード",
    "status": "ステータス・付帯サービス",
    "ease": "使いやすさ・利便性",
}

PRIORITY_AXIS_PRESETS = {
    "cost": ["annual_fee", "effective_annual_fee", "family_card_fee"],
    "reward": [
        "base_rate", "effective_rate", "supermarket_rate", "convenience_rate",
        "daily_effective_rate", "annual_bonus", "point_expiry",
    ],
    "travel": ["priority_pass", "lounge", "travel_insurance", "concierge"],
    "ecosystem": [
        "rakuten_fit", "docomo_fit", "paypay_fit", "marui_fit",
        "yahoo_fit", "amazon_fit", "aeon_fit",
    ],
    "insurance": ["travel_insurance", "car_insurance", "gasoline_rate", "priority_pass"],
    "family": ["family_card_fee", "annual_fee", "effective_annual_fee"],
    "status": ["concierge", "lounge", "priority_pass", "brands"],
    "ease": ["mobile_pay", "brands", "point_expiry", "family_card_fee"],
}


def _normalized_eco_shares(ecosystems: list[str]) -> dict[str, float]:
    if not ecosystems:
        return {}
    weights = {e: ECO_DEFAULT_SHARE.get(e, 0.12) for e in ecosystems}
    total = sum(weights.values())
    return {e: w / total for e, w in weights.items()}


@dataclass
class UserProfile:
    mode: str = "quick"
    annual_spend: int = 1_000_000
    priority: str = "reward"
    ecosystems: list[str] = field(default_factory=list)

    rakuten_annual_spend: Optional[int] = None
    docomo_monthly_fee: Optional[int] = None
    paypay_monthly_count: Optional[int] = None
    yahoo_annual_spend: Optional[int] = None
    marui_annual_spend: Optional[int] = None
    amazon_annual_spend: Optional[int] = None
    aeon_annual_spend: Optional[int] = None
    overseas_trips: int = 0
    pp_usage_count: int = 0
    has_family_card: bool = False
    family_annual_spend: int = 0
    epos_invite: bool = False
    epos_million_achieved: bool = False
    birth_month_spend: int = 0
    paypay_step_achieved: bool = True
    amex_mile_exchange: bool = False
    supermarket_heavy: bool = False
    convenience_heavy: bool = False
    has_car: bool = False
    supermarket_annual_spend: Optional[int] = None
    convenience_annual_spend: Optional[int] = None
    spend_by_category: dict[str, int] = field(default_factory=dict)


@dataclass
class ResolvedProfile:
    annual_spend: int
    rakuten_annual_spend: int
    docomo_monthly_fee: int
    paypay_monthly_count: int
    yahoo_annual_spend: int
    marui_annual_spend: int
    amazon_annual_spend: int
    aeon_annual_spend: int
    general_spend: int
    overseas_trips: int
    pp_usage_count: int
    has_family_card: bool
    family_annual_spend: int
    epos_invite: bool
    epos_million_achieved: bool
    birth_month_spend: int
    paypay_step_achieved: bool
    amex_mile_exchange: bool
    supermarket_annual_spend: int
    convenience_annual_spend: int
    has_car: bool
    ecosystems: list[str]


def resolve_profile(profile: UserProfile) -> ResolvedProfile:
    eco = profile.ecosystems or []
    annual = profile.annual_spend
    shares = _normalized_eco_shares(eco)

    if profile.mode == "detail" and profile.rakuten_annual_spend is not None:
        rakuten = profile.rakuten_annual_spend
    elif "rakuten" in shares:
        rakuten = int(annual * shares["rakuten"])
    else:
        rakuten = 0

    if profile.mode == "detail" and profile.docomo_monthly_fee is not None:
        docomo_monthly = profile.docomo_monthly_fee
    elif "docomo" in shares:
        docomo_monthly = 8000
    else:
        docomo_monthly = 0

    if profile.mode == "detail" and profile.paypay_monthly_count is not None:
        paypay_count = profile.paypay_monthly_count
    elif "paypay" in shares:
        paypay_count = 30
    else:
        paypay_count = 0

    if profile.mode == "detail" and profile.yahoo_annual_spend is not None:
        yahoo = profile.yahoo_annual_spend
    elif "yahoo" in shares:
        yahoo = int(annual * shares["yahoo"])
    elif "paypay" in shares:
        yahoo = int(annual * shares["paypay"] * 0.4)
    else:
        yahoo = 0

    if profile.mode == "detail" and profile.marui_annual_spend is not None:
        marui = profile.marui_annual_spend
    elif "marui" in shares:
        marui = int(annual * shares["marui"])
    else:
        marui = 0

    if profile.mode == "detail" and profile.amazon_annual_spend is not None:
        amazon = profile.amazon_annual_spend
    elif "amazon" in shares:
        amazon = int(annual * shares["amazon"])
    else:
        amazon = 0

    if profile.mode == "detail" and profile.aeon_annual_spend is not None:
        aeon = profile.aeon_annual_spend
    elif "aeon" in shares:
        aeon = int(annual * shares["aeon"])
    else:
        aeon = 0

    if profile.mode == "detail" and profile.supermarket_annual_spend is not None:
        supermarket = profile.supermarket_annual_spend
    elif profile.supermarket_heavy or "aeon" in eco:
        supermarket = int(annual * (0.25 if profile.supermarket_heavy else 0.20))
    else:
        supermarket = int(annual * 0.15)

    if profile.mode == "detail" and profile.convenience_annual_spend is not None:
        convenience = profile.convenience_annual_spend
    elif profile.convenience_heavy:
        convenience = int(annual * 0.18)
    else:
        convenience = int(annual * 0.10)

    allocated = (
        rakuten + yahoo + marui + amazon + aeon
        + docomo_monthly * 12 + supermarket + convenience
    )
    general = max(0, annual - allocated)

    return ResolvedProfile(
        annual_spend=annual,
        rakuten_annual_spend=rakuten,
        docomo_monthly_fee=docomo_monthly,
        paypay_monthly_count=paypay_count,
        yahoo_annual_spend=yahoo,
        marui_annual_spend=marui,
        amazon_annual_spend=amazon,
        aeon_annual_spend=aeon,
        general_spend=general,
        overseas_trips=profile.overseas_trips,
        pp_usage_count=profile.pp_usage_count,
        has_family_card=profile.has_family_card,
        family_annual_spend=profile.family_annual_spend,
        epos_invite=profile.epos_invite,
        epos_million_achieved=profile.epos_million_achieved,
        birth_month_spend=profile.birth_month_spend,
        paypay_step_achieved=profile.paypay_step_achieved,
        amex_mile_exchange=profile.amex_mile_exchange,
        supermarket_annual_spend=supermarket,
        convenience_annual_spend=convenience,
        has_car=profile.has_car,
        ecosystems=eco,
    )
