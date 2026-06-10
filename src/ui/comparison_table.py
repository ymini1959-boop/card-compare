from __future__ import annotations

import streamlit as st

from src.calculator.effective_rate import ANCHOR_ID
from src.models.comparison import CardResult
from src.ui.axis_values import (
    HIGHER_BETTER_AXES,
    LOWER_BETTER_AXES,
    format_axis_value,
    parse_numeric,
)
from src.ui.styles import card_header_color
from src.ui.winners import get_axis_winners


def _cell_classes(
    axis_id: str,
    cid: str,
    value: str,
    anchor_val: str,
    winners: list[str],
    card_count: int,
) -> str:
    classes = []
    if cid == ANCHOR_ID:
        classes.append("cell-anchor")
    if cid in winners and winners and len(winners) < card_count:
        classes.append("cell-winner")
    elif cid != ANCHOR_ID and axis_id in HIGHER_BETTER_AXES | LOWER_BETTER_AXES:
        num = parse_numeric(axis_id, value)
        anchor_num = parse_numeric(axis_id, anchor_val)
        if num is not None and anchor_num is not None:
            if axis_id in HIGHER_BETTER_AXES:
                if num > anchor_num:
                    classes.append("cell-better")
                elif num < anchor_num:
                    classes.append("cell-worse")
            else:
                if num < anchor_num:
                    classes.append("cell-better")
                elif num > anchor_num:
                    classes.append("cell-worse")
    return " ".join(classes)


def render_comparison_table(
    selected_axes: list[str],
    axis_defs: dict,
    results: dict[str, CardResult],
    cards_data: dict[str, dict],
) -> None:
    card_ids = list(results.keys())

    html = [
        '<p class="table-scroll-hint">← 横にスワイプして比較 →</p>',
        '<div class="compare-table-wrap"><table class="compare-table">',
        "<thead><tr>",
    ]
    html.append('<th class="axis-col">比較軸</th>')
    for cid in card_ids:
        color = card_header_color(cid)
        name = results[cid].card_name
        badge = "（基準）" if cid == ANCHOR_ID else ""
        html.append(f'<th style="background:{color};">{name}{badge}</th>')
    html.append("</tr></thead><tbody>")

    for axis_id in selected_axes:
        label = axis_defs[axis_id]["label"]
        winners = get_axis_winners(axis_id, card_ids, results, cards_data)
        row_values = {
            cid: format_axis_value(cards_data[cid], axis_id, results[cid])
            for cid in card_ids
        }
        anchor_val = row_values.get(ANCHOR_ID, "")

        html.append("<tr>")
        winner_label = ""
        if winners and len(winners) < len(card_ids):
            wnames = "・".join(results[w].card_name for w in winners)
            winner_label = (
                f'<br><span class="axis-winner-chip" '
                f'style="background:{card_header_color(winners[0])};">'
                f"◎ {wnames}</span>"
            )
        html.append(f'<td class="axis-label">{label}{winner_label}</td>')

        for cid in card_ids:
            val = row_values[cid]
            cls = _cell_classes(axis_id, cid, val, anchor_val, winners, len(card_ids))
            badge = ""
            if cid in winners and len(winners) < len(card_ids):
                tie_cls = "badge-tie" if len(winners) > 1 else ""
                label_badge = "同率" if len(winners) > 1 else "BEST"
                badge = f'<div class="badge-best {tie_cls}">{label_badge}</div>'
            display_val = val if len(str(val)) < 48 else str(val)[:45] + "…"
            html.append(f'<td class="{cls}">{badge}{display_val}</td>')
        html.append("</tr>")

    html.append("</tbody></table></div>")
    html.append(
        '<div class="legend-row">'
        '<span class="legend-item"><span class="legend-swatch" '
        'style="background:linear-gradient(135deg,#f59e0b,#d97706);"></span>'
        "BEST＝その軸で最優位</span>"
        '<span class="legend-item"><span class="legend-swatch" '
        'style="background:#ecfdf5;border:1px solid #86efac;"></span>'
        "緑＝エポスより有利</span>"
        '<span class="legend-item"><span class="legend-swatch" '
        'style="background:#fef2f2;border:1px solid #fca5a5;"></span>'
        "赤＝エポスより不利</span>"
        '<span class="legend-item"><span class="legend-swatch" '
        'style="background:#f0f6fc;border:1px solid #93c5fd;"></span>'
        "青＝基準カード（エポス）</span>"
        "</div>"
    )

    st.markdown("".join(html), unsafe_allow_html=True)

    with st.expander("カード別の試算メモ"):
        for cid, result in results.items():
            if result.notes:
                st.markdown(f"**{result.card_name}**")
                for note in result.notes:
                    st.markdown(f"- {note}")

    with st.expander("公式サイト・最終確認日"):
        for cid in results:
            card = cards_data[cid]
            st.markdown(
                f"- [{card['name']}]({card['official_url']}) "
                f"（最終確認: {card.get('last_updated', '—')}）"
            )
