from __future__ import annotations

import streamlit as st

from src.calculator.effective_rate import ANCHOR_ID
from src.ui.axis_values import format_axis_value
from src.ui.styles import card_header_color
from src.ui.winners import compute_win_counts, get_axis_winners


def render_car_insurance_highlight(
    card_ids: list[str],
    results: dict,
    cards_data: dict,
    has_car: bool,
) -> None:
    winners = get_axis_winners("car_insurance", card_ids, results, cards_data)
    if not winners:
        return

    title = (
        "自動車保有者向け"
        if has_car
        else "自動車保険（保有時の参考）"
    )
    st.markdown(f'<p class="section-icon-title">🚗 {title}</p>', unsafe_allow_html=True)

    best = winners[0]
    best_val = format_axis_value(cards_data[best], "car_insurance", results[best])
    names = "・".join(results[w].card_name for w in winners)
    color = card_header_color(best)

    st.markdown(
        f'<div class="insurance-hero">'
        f'<strong style="color:#166534;">優位:</strong> '
        f'<span class="axis-winner-chip" style="background:{color};">{names}</span>'
        f'<br><span style="color:#475569;font-size:0.78rem;">{best_val}</span>'
        f"</div>",
        unsafe_allow_html=True,
    )

    rows = ['<div class="insurance-row">']
    for cid in card_ids:
        val = format_axis_value(cards_data[cid], "car_insurance", results[cid])
        score = results[cid].car_insurance_score
        color = card_header_color(cid)
        rows.append(
            f'<div class="insurance-card">'
            f'<div class="insurance-card-name">{results[cid].card_name}</div>'
            f'<div class="insurance-bar-track">'
            f'<div class="insurance-bar-fill" style="width:{score}%;background:{color};"></div>'
            f"</div>"
            f'<div class="insurance-card-val">{val}</div>'
            f"</div>"
        )
    rows.append("</div>")
    st.markdown("".join(rows), unsafe_allow_html=True)


def render_win_summary(
    selected_axes: list[str],
    axis_defs: dict,
    card_ids: list[str],
    results: dict,
    cards_data: dict,
) -> dict[str, list[str]]:
    counts, axis_winners, comparable_count = compute_win_counts(
        selected_axes, card_ids, results, cards_data
    )

    st.markdown('<p class="section-icon-title">軸別の優位カード</p>', unsafe_allow_html=True)
    chips_html = ['<div class="axis-summary-grid">']
    for axis_id in selected_axes:
        winners = axis_winners.get(axis_id, [])
        label = axis_defs[axis_id]["label"]
        if not winners:
            winner_text = '<span style="color:#94a3b8;font-size:0.78rem;">比較不可</span>'
        elif len(winners) == len(card_ids):
            winner_text = '<span style="color:#94a3b8;font-size:0.78rem;">同率</span>'
        else:
            names = [results[w].card_name for w in winners]
            color = card_header_color(winners[0])
            winner_text = (
                f'<span class="axis-winner-chip" style="background:{color};">'
                f'{"・".join(names)}</span>'
            )
        chips_html.append(
            f'<div class="axis-summary-item">'
            f'<div class="axis-name">{label}</div>'
            f'<div class="winner-name">{winner_text}</div></div>'
        )
    chips_html.append("</div>")
    st.markdown("".join(chips_html), unsafe_allow_html=True)

    st.markdown('<p class="section-icon-title">優位軸の獲得数</p>', unsafe_allow_html=True)
    st.caption(
        f"選択した {len(selected_axes)} 軸のうち、"
        f"勝敗がついた {comparable_count} 軸で集計しています。"
    )

    max_count = max(counts.values()) if counts else 0
    leaders = [cid for cid, c in counts.items() if c == max_count and max_count > 0]
    sorted_ids = sorted(
        card_ids,
        key=lambda cid: (-counts[cid], cid == ANCHOR_ID),
    )

    metrics_html = ['<div class="win-metrics-scroll">']
    for cid in sorted_ids:
        count = counts[cid]
        is_anchor = cid == ANCHOR_ID
        color = card_header_color(cid)
        anchor_cls = " anchor" if is_anchor else ""
        crown = ""
        if count == max_count and max_count > 0 and len(leaders) == 1:
            crown = '<span class="crown">👑</span>'
        elif count == max_count and max_count > 0 and len(leaders) > 1:
            crown = '<span class="crown">🤝</span>'
        metrics_html.append(
            f'<div class="win-metric{anchor_cls}">'
            f'<div class="count" style="color:{color};">{count}{crown}</div>'
            f'<div class="label">{count} / {comparable_count} 軸で優位</div>'
            f'<div class="name">{results[cid].card_name}</div>'
            f"</div>"
        )
    metrics_html.append("</div>")
    st.markdown("".join(metrics_html), unsafe_allow_html=True)

    if len(leaders) > 1 and comparable_count > 0:
        names = "・".join(results[c].card_name for c in leaders)
        st.caption(f"同率トップ: {names}")

    return axis_winners
