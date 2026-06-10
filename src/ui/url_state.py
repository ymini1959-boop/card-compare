from urllib.parse import urlencode

import streamlit as st

from src.calculator.effective_rate import ANCHOR_ID, MAX_COMPARE_CARDS
from src.models.profile import PRIORITY_AXIS_PRESETS, PRIORITY_OPTIONS

DEFAULT_CARDS = ["rakuten-premium"]


def parse_query_params() -> dict:
    params = st.query_params
    spend = int(params.get("spend", "1000000"))
    if "cards" in params and str(params.get("cards", "")).strip():
        cards_raw = str(params["cards"])
        cards = [
            c.strip()
            for c in cards_raw.split(",")
            if c.strip() and c.strip() != ANCHOR_ID
        ]
    else:
        cards = list(DEFAULT_CARDS)
    cards = cards[:MAX_COMPARE_CARDS]

    axes_raw = params.get("axes", "")
    axes = [a.strip() for a in axes_raw.split(",") if a.strip()] if axes_raw else []

    mode = params.get("mode", "quick")
    eco_raw = params.get("eco", "")
    eco = [e.strip() for e in eco_raw.split(",") if e.strip()] if eco_raw else []

    priority = params.get("priority", "reward")
    if priority not in PRIORITY_OPTIONS:
        priority = "reward"

    def _flag(name: str) -> bool:
        return str(params.get(name, "")).lower() in ("1", "true", "yes", "on")

    return {
        "spend": spend,
        "cards": cards,
        "axes": axes,
        "mode": mode,
        "eco": eco,
        "priority": priority,
        "supermarket_heavy": _flag("supermarket"),
        "convenience_heavy": _flag("convenience"),
        "has_car": _flag("car"),
    }


def build_share_url(
    spend: int,
    cards: list[str],
    axes: list[str],
    mode: str,
    eco: list[str],
    priority: str,
    supermarket_heavy: bool = False,
    convenience_heavy: bool = False,
    has_car: bool = False,
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
    if supermarket_heavy:
        params["supermarket"] = "1"
    if convenience_heavy:
        params["convenience"] = "1"
    if has_car:
        params["car"] = "1"
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
    supermarket_heavy: bool = False,
    convenience_heavy: bool = False,
    has_car: bool = False,
) -> None:
    compare_cards = [c for c in cards if c != ANCHOR_ID][:MAX_COMPARE_CARDS]
    params = {
        "spend": str(spend),
        "cards": ",".join(compare_cards),
        "axes": ",".join(axes),
        "mode": mode,
        "eco": ",".join(eco),
        "priority": priority,
    }
    if supermarket_heavy:
        params["supermarket"] = "1"
    if convenience_heavy:
        params["convenience"] = "1"
    if has_car:
        params["car"] = "1"
    st.query_params.from_dict(params)


def render_share_section(share_url: str) -> None:
    st.caption("URLを長押ししてコピー。同じ条件で比較画面が開きます。")
    st.markdown(
        f'<div class="share-box"><div class="share-url">{share_url}</div></div>',
        unsafe_allow_html=True,
    )
