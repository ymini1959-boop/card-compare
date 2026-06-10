from urllib.parse import urlencode

import streamlit as st

from src.calculator.effective_rate import ANCHOR_ID, MAX_COMPARE_CARDS
from src.models.profile import PRIORITY_AXIS_PRESETS, PRIORITY_OPTIONS

DEFAULT_CARDS = [
    "rakuten-premium",
    "rakuten-black",
    "dcard-platinum",
    "jcb-platinum",
    "amex-platinum",
    "saison-platinum-amex",
    "mitsui-sumitomo-nl",
]


def parse_query_params() -> dict:
    params = st.query_params
    spend = int(params.get("spend", "1000000"))
    cards_raw = params.get("cards", ",".join(DEFAULT_CARDS))
    cards = [c.strip() for c in cards_raw.split(",") if c.strip() and c.strip() != ANCHOR_ID]
    cards = cards[:MAX_COMPARE_CARDS]

    axes_raw = params.get("axes", "")
    axes = [a.strip() for a in axes_raw.split(",") if a.strip()] if axes_raw else []

    mode = params.get("mode", "quick")
    eco_raw = params.get("eco", "")
    eco = [e.strip() for e in eco_raw.split(",") if e.strip()] if eco_raw else []

    priority = params.get("priority", "reward")
    if priority not in PRIORITY_OPTIONS:
        priority = "reward"

    return {
        "spend": spend,
        "cards": cards,
        "axes": axes,
        "mode": mode,
        "eco": eco,
        "priority": priority,
    }


def build_share_url(
    spend: int,
    cards: list[str],
    axes: list[str],
    mode: str,
    eco: list[str],
    priority: str,
) -> str:
    compare_cards = [c for c in cards if c != ANCHOR_ID][:MAX_COMPARE_CARDS]
    params = {
        "spend": str(spend),
        "cards": ",".join(compare_cards),
        "axes": ",".join(axes),
        "mode": mode,
        "eco": ",".join(eco),
        "priority": priority,
    }
    query = urlencode(params)
    try:
        host = st.context.headers.get("Host", "")
        if host:
            scheme = "https" if "streamlit" in host else "http"
            return f"{scheme}://{host}/?{query}"
    except Exception:
        pass
    return f"?{query}"


def sync_query_params(
    spend: int,
    cards: list[str],
    axes: list[str],
    mode: str,
    eco: list[str],
    priority: str,
) -> None:
    compare_cards = [c for c in cards if c != ANCHOR_ID][:MAX_COMPARE_CARDS]
    st.query_params.from_dict(
        {
            "spend": str(spend),
            "cards": ",".join(compare_cards),
            "axes": ",".join(axes),
            "mode": mode,
            "eco": ",".join(eco),
            "priority": priority,
        }
    )


def render_share_section(share_url: str) -> None:
    st.caption("URLを長押ししてコピー。同じ条件で比較画面が開きます。")
    st.markdown(
        f'<div class="share-box"><div class="share-url">{share_url}</div></div>',
        unsafe_allow_html=True,
    )
