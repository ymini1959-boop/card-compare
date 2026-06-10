from __future__ import annotations

import streamlit as st

from src.calculator.effective_rate import ANCHOR_ID, MAX_COMPARE_CARDS
from src.data_loader import cards_by_issuer, load_issuers


def render_card_selector(
    cards_data: dict[str, dict],
    default_ids: list[str],
) -> list[str]:
    issuers = load_issuers()
    grouped = cards_by_issuer(cards_data)

    st.caption(f"発行会社別に選択（最大{MAX_COMPARE_CARDS}枚）")

    if "compare_card_selection" not in st.session_state:
        st.session_state.compare_card_selection = [
            c for c in default_ids if c in cards_data and c != ANCHOR_ID
        ][:MAX_COMPARE_CARDS]

    selected: list[str] = []
    for issuer in issuers:
        issuer_id = issuer["id"]
        card_ids = [c for c in grouped.get(issuer_id, []) if c != ANCHOR_ID]
        if not card_ids:
            continue
        color = issuer.get("color", "#334155")
        with st.container(border=True):
            st.markdown(
                f'<p class="issuer-block-title" style="color:{color};margin-bottom:0;">'
                f"{issuer['label']}</p>",
                unsafe_allow_html=True,
            )
            picks = st.multiselect(
                f"{issuer['label']}のカード",
                options=card_ids,
                default=[
                    c for c in st.session_state.compare_card_selection if c in card_ids
                ],
                format_func=lambda cid: cards_data[cid]["name"],
                key=f"pick_{issuer_id}",
                label_visibility="collapsed",
            )
            selected.extend(picks)

    if len(selected) > MAX_COMPARE_CARDS:
        st.warning(f"比較は最大{MAX_COMPARE_CARDS}枚までです。先頭{MAX_COMPARE_CARDS}枚を使用します。")
        selected = selected[:MAX_COMPARE_CARDS]

    st.session_state.compare_card_selection = selected

    if selected:
        chips = "".join(
            f'<span class="card-chip">{cards_data[c]["name"]}</span>'
            for c in selected
        )
        st.markdown(
            f'<div class="selected-cards-chip">{chips}</div>',
            unsafe_allow_html=True,
        )

    return selected
