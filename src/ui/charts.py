import plotly.graph_objects as go
import streamlit as st

from src.calculator.effective_rate import effective_rate_curve
from src.data_loader import load_cards
from src.models.profile import ResolvedProfile
from src.ui.styles import card_header_color

CHART_COLORS = {
    "epos-platinum": "#1a4d7c",
    "epos-gold": "#2d6a9f",
    "rakuten-premium": "#bf0000",
    "rakuten-card": "#e60012",
    "rakuten-black": "#1a1a1a",
    "dcard": "#cc0033",
    "dcard-gold": "#b8002e",
    "dcard-platinum": "#8b0020",
    "paypay-gold": "#ff0033",
    "paypay-card": "#64748b",
    "amex-gold": "#006fcf",
    "amex-platinum": "#4a4a4a",
    "amex-green": "#007a3e",
    "epos-card": "#4a7ba7",
    "rakuten-gold": "#d4145a",
    "dcard-gold-u": "#e85d75",
    "jcb-card-w": "#0b6b3a",
    "jcb-gold": "#096b38",
    "jcb-platinum": "#054d28",
    "jcb-original-gold": "#1a5c3a",
    "saison-platinum-amex": "#1e3a8a",
    "saison-pearl-amex": "#2563eb",
    "saison-classic-amex": "#3b82f6",
    "mitsui-sumitomo-nl": "#004098",
    "aeon-card-select": "#b60081",
    "mufg-card": "#d4002a",
}


def render_rate_chart(
    card_ids: list[str],
    profile: ResolvedProfile,
) -> None:
    cards = load_cards()
    fig = go.Figure()

    for card_id in card_ids:
        if card_id not in cards:
            continue
        curve = effective_rate_curve(card_id, profile)
        spends, rates = zip(*curve) if curve else ([], [])
        color = CHART_COLORS.get(card_id, card_header_color(card_id))
        fig.add_trace(
            go.Scatter(
                x=[s / 10_000 for s in spends],
                y=[r * 100 for r in rates],
                mode="lines",
                name=cards[card_id]["name"],
                line=dict(color=color, width=2.5 if card_id == "epos-platinum" else 2),
            )
        )

    fig.update_layout(
        title=None,
        xaxis_title="年間利用額（万円）",
        yaxis_title="還元率（%）",
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.28,
            xanchor="center",
            x=0.5,
            font=dict(size=10, family="Noto Sans JP, sans-serif"),
        ),
        height=420,
        margin=dict(l=40, r=16, t=16, b=100),
        plot_bgcolor="#f8fafc",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(gridcolor="#e8edf3", zeroline=False, tickfont=dict(size=11)),
        yaxis=dict(gridcolor="#e8edf3", zeroline=False, tickfont=dict(size=11)),
        hovermode="x unified",
        hoverlabel=dict(font_size=12),
    )
    st.plotly_chart(fig, use_container_width=True)
