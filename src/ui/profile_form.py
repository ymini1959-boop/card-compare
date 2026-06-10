from __future__ import annotations

import streamlit as st

from src.models.profile import (
    PRIORITY_AXIS_PRESETS,
    PRIORITY_OPTIONS,
    UserProfile,
    resolve_profile,
)

ECO_OPTIONS = {
    "rakuten": "楽天",
    "docomo": "ドコモ",
    "paypay": "PayPay",
    "yahoo": "Yahoo!ショッピング",
    "marui": "マルイ",
    "amazon": "Amazon",
    "aeon": "イオン",
}


def render_profile_form(defaults: dict | None = None) -> UserProfile:
    defaults = defaults or {}

    tab_quick, tab_detail = st.tabs(["クイック（30秒）", "詳細（精密試算）"])

    with tab_quick:
        annual_spend = st.slider(
            "年間カード利用額",
            min_value=300_000,
            max_value=5_000_000,
            value=int(defaults.get("spend", 1_000_000)),
            step=50_000,
            format="%d円",
        )
        priority_default = defaults.get("priority", "reward")
        if priority_default not in PRIORITY_OPTIONS:
            priority_default = "reward"
        priority = st.selectbox(
            "いちばん重視すること",
            options=list(PRIORITY_OPTIONS.keys()),
            index=list(PRIORITY_OPTIONS.keys()).index(priority_default),
            format_func=lambda k: PRIORITY_OPTIONS[k],
        )
        default_eco = defaults.get("eco", [])
        ecosystems = st.multiselect(
            "よく使う経済圏",
            options=list(ECO_OPTIONS.keys()),
            default=[e for e in default_eco if e in ECO_OPTIONS],
            format_func=lambda k: ECO_OPTIONS[k],
        )
        col_d1, col_d2, col_d3 = st.columns(3)
        supermarket_heavy = col_d1.checkbox(
            "スーパーでの買い物が多い",
            value=bool(defaults.get("supermarket_heavy", False)),
        )
        convenience_heavy = col_d2.checkbox(
            "コンビニ利用が多い",
            value=bool(defaults.get("convenience_heavy", False)),
        )
        has_car = col_d3.checkbox(
            "自動車を保有",
            value=bool(defaults.get("has_car", False)),
        )

    detail_kwargs = {
        "supermarket_heavy": supermarket_heavy,
        "convenience_heavy": convenience_heavy,
        "has_car": has_car,
    }
    with tab_detail:
        st.caption("詳細入力はクイック設定を上書きして試算に反映されます。")
        detail_kwargs["rakuten_annual_spend"] = st.number_input(
            "楽天市場 年間利用額（円）", min_value=0, value=0, step=10000
        )
        detail_kwargs["docomo_monthly_fee"] = st.number_input(
            "ドコモ月額料金（円）", min_value=0, value=0, step=500
        )
        detail_kwargs["paypay_monthly_count"] = st.number_input(
            "PayPay決済 月間回数", min_value=0, max_value=100, value=0
        )
        detail_kwargs["yahoo_annual_spend"] = st.number_input(
            "Yahoo!ショッピング 年間利用額（円）", min_value=0, value=0, step=10000
        )
        detail_kwargs["marui_annual_spend"] = st.number_input(
            "マルイ 年間利用額（円）", min_value=0, value=0, step=10000
        )
        detail_kwargs["amazon_annual_spend"] = st.number_input(
            "Amazon 年間利用額（円）", min_value=0, value=0, step=10000
        )
        detail_kwargs["aeon_annual_spend"] = st.number_input(
            "イオン 年間利用額（円）", min_value=0, value=0, step=10000
        )
        detail_kwargs["overseas_trips"] = st.number_input(
            "海外旅行（年間回数）", min_value=0, max_value=20, value=0
        )
        detail_kwargs["pp_usage_count"] = st.number_input(
            "プライオリティパス利用見込み（年間回数）", min_value=0, max_value=50, value=0
        )
        detail_kwargs["has_family_card"] = st.checkbox("家族カードあり")
        detail_kwargs["family_annual_spend"] = st.number_input(
            "家族カード年間利用額（円）", min_value=0, value=0, step=10000
        )
        detail_kwargs["epos_invite"] = st.checkbox("エポスプラチナ招待あり")
        detail_kwargs["epos_million_achieved"] = st.checkbox(
            "年間100万円以上利用見込み（翌年年会費割引）",
            value=annual_spend >= 1_000_000,
        )
        detail_kwargs["birth_month_spend"] = st.number_input(
            "誕生月の利用額（円）", min_value=0, value=0, step=10000
        )
        detail_kwargs["paypay_step_achieved"] = st.checkbox(
            "PayPayステップ達成見込み", value=True
        )
        detail_kwargs["amex_mile_exchange"] = st.checkbox("Amexマイル交換利用")
        detail_kwargs["supermarket_annual_spend"] = st.number_input(
            "スーパー 年間利用額（円）", min_value=0, value=0, step=10000
        )
        detail_kwargs["convenience_annual_spend"] = st.number_input(
            "コンビニ 年間利用額（円）", min_value=0, value=0, step=10000
        )
        detail_kwargs["has_car"] = st.checkbox(
            "自動車を保有している", value=detail_kwargs["has_car"]
        )

    has_detail_input = (
        detail_kwargs["rakuten_annual_spend"] > 0
        or detail_kwargs["docomo_monthly_fee"] > 0
        or detail_kwargs["paypay_monthly_count"] > 0
        or detail_kwargs["yahoo_annual_spend"] > 0
        or detail_kwargs["marui_annual_spend"] > 0
        or detail_kwargs["amazon_annual_spend"] > 0
        or detail_kwargs["aeon_annual_spend"] > 0
        or detail_kwargs["overseas_trips"] > 0
        or detail_kwargs["pp_usage_count"] > 0
        or detail_kwargs["birth_month_spend"] > 0
        or detail_kwargs["has_family_card"]
        or detail_kwargs["epos_invite"]
        or detail_kwargs["amex_mile_exchange"]
        or detail_kwargs.get("supermarket_annual_spend", 0) > 0
        or detail_kwargs.get("convenience_annual_spend", 0) > 0
    )

    profile_mode = "detail" if has_detail_input else "quick"
    if defaults.get("mode") == "detail":
        profile_mode = "detail"

    profile = UserProfile(
        mode=profile_mode,
        annual_spend=annual_spend,
        priority=priority,
        ecosystems=ecosystems,
        rakuten_annual_spend=detail_kwargs["rakuten_annual_spend"] or None,
        docomo_monthly_fee=detail_kwargs["docomo_monthly_fee"] or None,
        paypay_monthly_count=detail_kwargs["paypay_monthly_count"] or None,
        yahoo_annual_spend=detail_kwargs["yahoo_annual_spend"] or None,
        marui_annual_spend=detail_kwargs["marui_annual_spend"] or None,
        amazon_annual_spend=detail_kwargs["amazon_annual_spend"] or None,
        aeon_annual_spend=detail_kwargs["aeon_annual_spend"] or None,
        overseas_trips=int(detail_kwargs["overseas_trips"]),
        pp_usage_count=int(detail_kwargs["pp_usage_count"]),
        has_family_card=detail_kwargs["has_family_card"],
        family_annual_spend=int(detail_kwargs["family_annual_spend"]),
        epos_invite=detail_kwargs["epos_invite"],
        epos_million_achieved=detail_kwargs["epos_million_achieved"],
        birth_month_spend=int(detail_kwargs["birth_month_spend"]),
        paypay_step_achieved=detail_kwargs["paypay_step_achieved"],
        amex_mile_exchange=detail_kwargs["amex_mile_exchange"],
        supermarket_heavy=detail_kwargs["supermarket_heavy"],
        convenience_heavy=detail_kwargs["convenience_heavy"],
        has_car=detail_kwargs["has_car"],
        supermarket_annual_spend=detail_kwargs.get("supermarket_annual_spend") or None,
        convenience_annual_spend=detail_kwargs.get("convenience_annual_spend") or None,
    )

    if supermarket_heavy or convenience_heavy or has_car:
        resolved = resolve_profile(profile)
        hints = []
        if supermarket_heavy or convenience_heavy:
            hints.append(
                f"スーパー {resolved.supermarket_annual_spend:,}円／"
                f"コンビニ {resolved.convenience_annual_spend:,}円 を試算に反映"
            )
        if has_car:
            hints.append("自動車保険優遇の比較を表示")
        st.caption("✓ " + " ｜ ".join(hints))

    return profile


def get_preset_axes(priority: str) -> list[str]:
    return PRIORITY_AXIS_PRESETS.get(priority, PRIORITY_AXIS_PRESETS["reward"])
