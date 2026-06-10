from __future__ import annotations

import streamlit as st

from src.calculator.effective_rate import ANCHOR_ID, MAX_COMPARE_CARDS
from src.data_loader import cards_by_issuer, load_issuers
from src.ui.styles import card_header_color


def _normalize_defaults(default_ids: list[str], cards_data: dict[str, dict]) -> list[str]:
    return [
        c for c in default_ids if c in cards_data and c != ANCHOR_ID
    ][:MAX_COMPARE_CARDS]


def _sync_selection_from_defaults(
    default_ids: list[str],
    cards_data: dict[str, dict],
    issuers: list[dict],
) -> None:
    normalized = _normalize_defaults(default_ids, cards_data)
    sig = ",".join(normalized)
    if st.session_state.get("_card_defaults_sig") == sig:
        return
    st.session_state._card_defaults_sig = sig
    st.session_state.compare_card_selection = normalized
    for issuer in issuers:
        st.session_state.pop(f"pick_{issuer['id']}", None)


def render_card_selector(
    cards_data: dict[str, dict],
    default_ids: list[str],
) -> list[str]:
    issuers = load_issuers()
    grouped = cards_by_issuer(cards_data)

    _sync_selection_from_defaults(default_ids, cards_data, issuers)

    st.caption(f"発行会社別に選択（最大{MAX_COMPARE_CARDS}枚）")

    selected: list[str] = []
    for issuer in issuers:
        issuer_id = issuer["id"]
        card_ids = [c for c in grouped.get(issuer_id, []) if c != ANCHOR_ID]
        if not card_ids:
            continue
        color = issuer.get("color", "#334155")
        widget_key = f"pick_{issuer_id}"
        if widget_key not in st.session_state:
            st.session_state[widget_key] = [
                c for c in st.session_state.compare_card_selection if c in card_ids
            ]

        with st.container(border=True):
            st.markdown(
                f'<div class="issuer-block-header" style="--issuer-color:{color};">'
                f'<p class="issuer-block-title" style="color:{color};">'
                f"{issuer['label']}</p></div>",
                unsafe_allow_html=True,
            )
            picks = st.multiselect(
                f"{issuer['label']}のカード",
                options=card_ids,
                format_func=lambda cid: cards_data[cid]["name"],
                key=widget_key,
                label_visibility="collapsed",
            )
            selected.extend(picks)

    if len(selected) > MAX_COMPARE_CARDS:
        st.warning(f"比較は最大{MAX_COMPARE_CARDS}枚までです。先頭{MAX_COMPARE_CARDS}枚を使用します。")
        selected = selected[:MAX_COMPARE_CARDS]

    st.session_state.compare_card_selection = selected

    if selected:
        chips = "".join(
            f'<span class="card-chip" style="background:linear-gradient(135deg,'
            f'{card_header_color(c)} 0%, {card_header_color(c)}cc 100%);">'
            f'{cards_data[c]["name"]}</span>'
            for c in selected
        )
        st.markdown(
            f'<div class="selected-cards-chip">{chips}</div>',
            unsafe_allow_html=True,
        )

    return selected
