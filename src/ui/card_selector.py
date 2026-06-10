from __future__ import annotations

import streamlit as st

from src.calculator.effective_rate import ANCHOR_ID, MAX_COMPARE_CARDS
from src.data_loader import cards_by_issuer, load_issuers
from src.ui.styles import card_header_color


def _normalize_defaults(default_ids: list[str], cards_data: dict[str, dict]) -> list[str]:
    return [
        c for c in default_ids if c in cards_data and c != ANCHOR_ID
    ][:MAX_COMPARE_CARDS]


def finalize_card_selection(
    previous: list[str],
    picks_by_issuer: list[list[str]],
    max_cards: int = MAX_COMPARE_CARDS,
) -> list[str]:
    """選択カードの順序を維持する。

    - 既存選択: previous（URL・前回の確定順）を優先
    - 新規追加: 前回に無かったカードだけ末尾へ（クリック順を保持）
    - Streamlit multiselect の返却順（tier_order / options 順）は使わない
    """
    picked_set: set[str] = set()
    for picks in picks_by_issuer:
        picked_set.update(picks)

    ordered = [c for c in previous if c in picked_set]
    known = set(previous)

    for picks in picks_by_issuer:
        for cid in picks:
            if cid in picked_set and cid not in known:
                ordered.append(cid)
                known.add(cid)

    return ordered[:max_cards]


def _sync_widget_order(widget_key: str, canonical: list[str]) -> None:
    """multiselect のタグ表示を確定順に揃える（選択内容は変えない）。"""
    if widget_key not in st.session_state:
        st.session_state[widget_key] = list(canonical)
        return
    current = st.session_state[widget_key]
    if set(current) == set(canonical) and current != canonical:
        st.session_state[widget_key] = list(canonical)


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

    previous_order = list(st.session_state.get("compare_card_selection", []))

    st.caption(
        f"発行会社別に選択（最大{MAX_COMPARE_CARDS}枚）"
        "・比較表の列順は選択順（URLの cards= 順）を維持します"
    )

    issuer_picks: list[list[str]] = []
    for issuer in issuers:
        issuer_id = issuer["id"]
        card_ids = [c for c in grouped.get(issuer_id, []) if c != ANCHOR_ID]
        if not card_ids:
            continue
        color = issuer.get("color", "#334155")
        widget_key = f"pick_{issuer_id}"
        canonical_for_issuer = [c for c in previous_order if c in card_ids]
        _sync_widget_order(widget_key, canonical_for_issuer)

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
            issuer_picks.append(picks)

    selected = finalize_card_selection(previous_order, issuer_picks)

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
