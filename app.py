import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st

from src.calculator.effective_rate import ANCHOR_ID, calculate_all
from src.data_loader import cards_by_issuer, load_axes, load_cards, load_issuers
from src.models.profile import resolve_profile
from src.ui.axis_picker import render_axis_picker
from src.ui.card_selector import render_card_selector
from src.ui.charts import render_rate_chart
from src.ui.comparison_table import render_comparison_table
from src.ui.compliance import render_footer, render_header
from src.ui.profile_form import get_preset_axes, render_profile_form
from src.ui.styles import inject_styles, section
from src.ui.summary import render_car_insurance_highlight, render_win_summary
from src.ui.url_state import (
    build_share_url,
    parse_query_params,
    render_share_section,
    sync_query_params,
)

st.set_page_config(
    page_title="クレジットカード比較 | エポスプラチナ基準",
    page_icon="💳",
    layout="centered",
    initial_sidebar_state="collapsed",
)

inject_styles()
render_header()

qp = parse_query_params()
cards_data = load_cards()
issuer_groups = cards_by_issuer(cards_data)

defaults = {
    "spend": qp["spend"],
    "mode": qp["mode"],
    "eco": qp["eco"],
    "priority": qp["priority"],
}

with section("あなたの条件", "📋"):
    profile = render_profile_form(defaults=defaults)

with section("比較するカード", "💳"):
    st.markdown(
        f"""
        <div class="anchor-badge">
            <div class="anchor-badge-icon">⚓</div>
            <div>
                <div class="anchor-badge-label">基準カード（固定）</div>
                <div class="anchor-badge-name">{cards_data[ANCHOR_ID]["name"]}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    default_compare = qp["cards"]
    with st.expander("登録カード一覧（発行会社別）", expanded=False):
        for issuer in load_issuers():
            ids = issuer_groups.get(issuer["id"], [])
            if not ids:
                continue
            names = " / ".join(cards_data[c]["name"] for c in ids)
            st.markdown(f"**{issuer['label']}**（{len(ids)}枚）: {names}")
    selected_compare = render_card_selector(cards_data, default_compare)

if "last_priority" not in st.session_state:
    st.session_state.last_priority = profile.priority
if profile.priority != st.session_state.last_priority:
    st.session_state.axis_preset = profile.priority
    st.session_state.last_priority = profile.priority

if qp["axes"] and "axis_preset" not in st.session_state:
    default_axes = qp["axes"]
elif st.session_state.get("axis_preset"):
    presets = load_axes()["presets"]
    preset_key = st.session_state["axis_preset"]
    default_axes = presets.get(preset_key, get_preset_axes(profile.priority))
else:
    default_axes = get_preset_axes(profile.priority)

with section("比較する軸", "📊"):
    selected_axes, axis_defs = render_axis_picker(default_axes=default_axes)

card_ids = [ANCHOR_ID] + selected_compare
resolved = resolve_profile(profile)
results = calculate_all(card_ids, resolved)

with section("比較結果", "🏆"):
    render_win_summary(selected_axes, axis_defs, card_ids, results, cards_data)
    if profile.has_car or "car_insurance" in selected_axes:
        render_car_insurance_highlight(
            card_ids, results, cards_data, profile.has_car
        )
    render_comparison_table(selected_axes, axis_defs, results, cards_data)

with section("還元率シミュレーション", "📈"):
    render_rate_chart(card_ids, resolved)

if results:
    best = max(results.values(), key=lambda r: r.effective_rate)
    anchor = results.get(ANCHOR_ID)
    if anchor and best.card_id != ANCHOR_ID:
        diff_pts = best.total_points_value - anchor.total_points_value
        st.markdown(
            f"""
            <div class="result-callout success">
                <strong>試算結果</strong><br>
                あなたの条件では <strong>{best.card_name}</strong> の実効還元率が最も高く、
                年間ポイント換算で約 <strong>{diff_pts:,}円</strong> の差が出ます（エポスプラチナ比）。
            </div>
            """,
            unsafe_allow_html=True,
        )
    elif anchor:
        st.markdown(
            """
            <div class="result-callout info">
                <strong>試算結果</strong><br>
                あなたの条件では <strong>エポスプラチナ</strong> の実効還元率が最も高い結果です。
            </div>
            """,
            unsafe_allow_html=True,
        )

sync_query_params(
    spend=profile.annual_spend,
    cards=selected_compare,
    axes=selected_axes,
    mode=profile.mode,
    eco=profile.ecosystems,
    priority=profile.priority,
)

share_url = build_share_url(
    spend=profile.annual_spend,
    cards=selected_compare,
    axes=selected_axes,
    mode=profile.mode,
    eco=profile.ecosystems,
    priority=profile.priority,
)

with section("この比較を共有", "🔗"):
    render_share_section(share_url)

render_footer()
