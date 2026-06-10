import streamlit as st

CARD_COLORS = {
    "epos-platinum": "#1e5a9e",
    "epos-gold": "#3b82f6",
    "rakuten-premium": "#e60026",
    "rakuten-card": "#ff1a3d",
    "rakuten-black": "#2d2d3a",
    "rakuten-gold": "#ff2d6a",
    "dcard": "#ff1744",
    "dcard-gold": "#d50032",
    "dcard-platinum": "#9b0028",
    "dcard-gold-u": "#ff4d7a",
    "paypay-gold": "#ff2244",
    "paypay-card": "#5c4d7a",
    "amex-gold": "#0077ee",
    "amex-platinum": "#3d4f6f",
    "amex-green": "#00a86b",
    "epos-card": "#4f8fd9",
    "jcb-card-w": "#00a854",
    "jcb-gold": "#008f47",
    "jcb-platinum": "#006b38",
    "jcb-original-gold": "#1a8f5a",
    "saison-platinum-amex": "#1d4ed8",
    "saison-pearl-amex": "#3b82f6",
    "saison-classic-amex": "#60a5fa",
    "mitsui-sumitomo-nl": "#0052cc",
    "aeon-card-select": "#d4008f",
    "mufg-card": "#e60028",
}

GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;600;700&display=swap');

:root {
    --bg: #dde4f0;
    --surface: #ffffff;
    --surface-2: #f4f7fc;
    --ink: #0a0f1a;
    --ink-muted: #5a6a85;
    --ink-subtle: #8b9cb8;
    --brand: #0a1628;
    --brand-mid: #1e40af;
    --brand-light: #dbeafe;
    --accent: #f59e0b;
    --accent-2: #ec4899;
    --accent-soft: #fff7ed;
    --radius: 18px;
    --radius-sm: 14px;
    --shadow: 0 8px 32px rgba(30, 64, 175, 0.12);
    --shadow-sm: 0 4px 16px rgba(30, 64, 175, 0.08);
    --safe-top: env(safe-area-inset-top, 0px);
    --safe-bottom: env(safe-area-inset-bottom, 0px);
    --safe-left: env(safe-area-inset-left, 0px);
    --safe-right: env(safe-area-inset-right, 0px);
}

html, body, [class*="css"] {
    font-family: 'Noto Sans JP', -apple-system, BlinkMacSystemFont, sans-serif;
    -webkit-font-smoothing: antialiased;
}

.stApp {
    background:
        radial-gradient(ellipse 80% 50% at 50% -10%, rgba(59,130,246,0.15) 0%, transparent 55%),
        radial-gradient(ellipse 60% 40% at 100% 0%, rgba(236,72,153,0.08) 0%, transparent 50%),
        linear-gradient(180deg, #c8d4e8 0%, var(--bg) 180px, var(--bg) 100%) !important;
}

#MainMenu, footer, header[data-testid="stHeader"] {
    visibility: hidden !important;
    height: 0 !important;
    min-height: 0 !important;
}

.block-container {
    padding-top: calc(0.75rem + var(--safe-top)) !important;
    padding-bottom: calc(2rem + var(--safe-bottom)) !important;
    padding-left: calc(0.85rem + var(--safe-left)) !important;
    padding-right: calc(0.85rem + var(--safe-right)) !important;
    max-width: 680px !important;
}

/* ── Hero ── */
.hero-banner {
    position: relative;
    overflow: hidden;
    background: linear-gradient(135deg, #020617 0%, #1e3a8a 40%, #7c3aed 85%, #db2777 100%);
    color: #fff;
    padding: 1.5rem 1.25rem 1.35rem;
    border-radius: 22px;
    margin-bottom: 1.25rem;
    box-shadow: 0 12px 40px rgba(30, 58, 138, 0.35);
}

.hero-banner::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -25%;
    width: 260px;
    height: 260px;
    background: radial-gradient(circle, rgba(251,191,36,0.35) 0%, transparent 65%);
    pointer-events: none;
}

.hero-banner::after {
    content: '';
    position: absolute;
    bottom: -40%;
    left: -15%;
    width: 200px;
    height: 200px;
    background: radial-gradient(circle, rgba(56,189,248,0.2) 0%, transparent 70%);
    pointer-events: none;
}

.hero-inner { position: relative; z-index: 1; }

.hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.75);
    margin-bottom: 0.5rem;
}

.hero-banner h1 {
    color: #fff !important;
    font-size: 1.45rem !important;
    font-weight: 700 !important;
    line-height: 1.35 !important;
    margin: 0 0 0.5rem 0 !important;
    padding: 0 !important;
    letter-spacing: -0.02em;
}

.hero-sub {
    opacity: 0.9;
    font-size: 0.88rem;
    line-height: 1.55;
    margin: 0 0 0.85rem 0;
    color: rgba(255,255,255,0.88);
}

.hero-pills {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
}

.disclaimer-pill {
    display: inline-block;
    background: rgba(255,255,255,0.1);
    border: 1px solid rgba(255,255,255,0.18);
    border-radius: 999px;
    padding: 0.3rem 0.7rem;
    font-size: 0.68rem;
    font-weight: 500;
    color: rgba(255,255,255,0.85);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
}

/* ── Sections ── */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--surface) !important;
    border: none !important;
    border-radius: var(--radius) !important;
    box-shadow: var(--shadow-sm) !important;
    padding: 0.25rem 0 !important;
    margin-bottom: 0.85rem !important;
    overflow: hidden;
}

div[data-testid="stVerticalBlockBorderWrapper"] > div {
    padding: 1rem 1rem 1.1rem !important;
}

.section-title {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 1rem;
    font-weight: 700;
    color: var(--ink);
    margin: 0 0 0.85rem 0;
    padding-bottom: 0.65rem;
    border-bottom: 1px solid #eef2f6;
    letter-spacing: -0.01em;
}

.section-title::before {
    content: '';
    display: block;
    width: 4px;
    height: 1.1rem;
    background: linear-gradient(180deg, #f59e0b, #ec4899, #8b5cf6);
    border-radius: 4px;
    flex-shrink: 0;
}

.section-icon-title {
    font-size: 0.95rem;
    font-weight: 700;
    color: var(--ink);
    margin: 0 0 0.75rem 0;
    letter-spacing: -0.01em;
}

/* ── Anchor card badge ── */
.anchor-badge {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    background: linear-gradient(135deg, #dbeafe 0%, #ede9fe 50%, #fff 100%);
    border: 1px solid #93c5fd;
    border-radius: var(--radius-sm);
    padding: 0.85rem 1rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 14px rgba(59, 130, 246, 0.12);
}

.anchor-badge-icon {
    font-size: 1.5rem;
    line-height: 1;
    flex-shrink: 0;
}

.anchor-badge-label {
    font-size: 0.68rem;
    font-weight: 600;
    color: var(--brand-mid);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 2px;
}

.anchor-badge-name {
    font-size: 0.95rem;
    font-weight: 700;
    color: var(--ink);
    line-height: 1.3;
}

/* ── Issuer picker cards ── */
.issuer-block {
    background: var(--surface-2);
    border: 1px solid #e8edf3;
    border-radius: var(--radius-sm);
    padding: 0.75rem 0.85rem;
    margin-bottom: 0.65rem;
}

.issuer-block-title {
    font-size: 0.8rem;
    font-weight: 700;
    margin: 0 0 0.35rem 0;
    letter-spacing: -0.01em;
}

.selected-cards-chip {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 0.5rem;
}

.issuer-block-header {
    border-left: 3px solid var(--issuer-color, #64748b);
    padding-left: 0.5rem;
    margin-bottom: 0.25rem;
}

.card-chip {
    display: inline-flex;
    align-items: center;
    font-size: 0.72rem;
    font-weight: 600;
    color: #fff;
    border-radius: 999px;
    padding: 0.38rem 0.75rem;
    line-height: 1.3;
    box-shadow: 0 2px 8px rgba(0,0,0,0.12);
}

/* ── Win metrics (horizontal scroll on mobile) ── */
.win-metrics-scroll {
    display: flex;
    gap: 10px;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    scroll-snap-type: x mandatory;
    padding: 4px 2px 12px;
    margin: 0 -4px;
}

.win-metrics-scroll::-webkit-scrollbar { height: 4px; }
.win-metrics-scroll::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 4px;
}

.win-metric {
    flex: 0 0 132px;
    scroll-snap-align: start;
    text-align: center;
    padding: 1rem 0.65rem;
    border-radius: var(--radius-sm);
    border: 1px solid #e8edf3;
    background: var(--surface-2);
}

.win-metric.anchor {
    border-color: #3b82f6;
    background: linear-gradient(180deg, #dbeafe 0%, #fff 100%);
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);
}

.win-metric .count {
    font-size: 1.75rem;
    font-weight: 700;
    line-height: 1.1;
    letter-spacing: -0.03em;
}

.win-metric .label {
    font-size: 0.65rem;
    color: var(--ink-muted);
    margin-top: 0.3rem;
    line-height: 1.35;
}

.win-metric .name {
    font-size: 0.72rem;
    font-weight: 600;
    margin-top: 0.4rem;
    color: var(--ink);
    line-height: 1.35;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.win-metric .crown {
    font-size: 0.85rem;
}

/* ── Axis summary grid ── */
.axis-summary-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 8px;
    margin-bottom: 1rem;
}

.axis-summary-item {
    background: var(--surface-2);
    border: 1px solid #e8edf3;
    border-radius: var(--radius-sm);
    padding: 0.75rem 0.85rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
}

.axis-summary-item .axis-name {
    font-size: 0.78rem;
    color: var(--ink-muted);
    flex: 1;
    min-width: 0;
}

.axis-summary-item .winner-name {
    font-size: 0.78rem;
    font-weight: 700;
    color: var(--ink);
    text-align: right;
    flex-shrink: 0;
    max-width: 55%;
}

/* ── Insurance highlight ── */
.insurance-hero {
    background: linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 100%);
    border: 1px solid #86efac;
    border-radius: var(--radius-sm);
    padding: 0.85rem 1rem;
    margin-bottom: 0.85rem;
    font-size: 0.82rem;
    line-height: 1.5;
}

.insurance-row {
    display: grid;
    grid-template-columns: 1fr;
    gap: 10px;
    margin: 6px 0;
}

.insurance-card {
    background: var(--surface-2);
    border: 1px solid #e8edf3;
    border-radius: 10px;
    padding: 0.65rem 0.75rem;
}

.insurance-card-name {
    font-size: 0.78rem;
    font-weight: 700;
    color: var(--ink);
    margin-bottom: 6px;
}

.insurance-bar-track {
    background: #e2e8f0;
    border-radius: 6px;
    height: 6px;
    overflow: hidden;
    margin-bottom: 6px;
}

.insurance-bar-fill {
    height: 6px;
    border-radius: 6px;
    transition: width 0.3s ease;
}

.insurance-card-val {
    font-size: 0.72rem;
    color: var(--ink-muted);
    line-height: 1.4;
}

/* ── Comparison table ── */
.table-scroll-hint {
    font-size: 0.68rem;
    color: var(--ink-subtle);
    text-align: center;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 4px;
}

.compare-table-wrap {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    border-radius: var(--radius-sm);
    border: 1px solid #e8edf3;
    margin: 0.5rem 0 1rem;
    box-shadow: inset 0 0 0 1px rgba(255,255,255,0.5);
}

.compare-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.78rem;
    min-width: 520px;
}

.compare-table thead th {
    padding: 11px 8px;
    text-align: center;
    font-weight: 600;
    font-size: 0.72rem;
    color: #fff;
    border-bottom: none;
    white-space: nowrap;
}

.compare-table thead th.axis-col {
    background: #1e293b;
    text-align: left;
    color: #f8fafc;
    min-width: 110px;
    position: sticky;
    left: 0;
    z-index: 2;
}

.compare-table tbody td {
    padding: 11px 8px;
    border-bottom: 1px solid #f1f5f9;
    text-align: center;
    vertical-align: middle;
    line-height: 1.4;
}

.compare-table tbody td.axis-label {
    text-align: left;
    font-weight: 600;
    font-size: 0.75rem;
    color: var(--ink);
    background: #f8fafc;
    position: sticky;
    left: 0;
    z-index: 1;
    box-shadow: 2px 0 6px rgba(0,0,0,0.04);
}

.cell-anchor { background: var(--brand-light) !important; font-weight: 600; }
.cell-winner {
    background: linear-gradient(180deg, var(--accent-soft) 0%, #fffbeb 100%) !important;
    box-shadow: inset 0 0 0 2px var(--accent);
    font-weight: 700;
}
.cell-better { background: #ecfdf5 !important; }
.cell-worse { background: #fef2f2 !important; }

.badge-best {
    display: inline-block;
    background: linear-gradient(135deg, #d97706, #b45309);
    color: #fff;
    font-size: 0.58rem;
    font-weight: 700;
    padding: 2px 6px;
    border-radius: 999px;
    margin-bottom: 3px;
    letter-spacing: 0.04em;
}

.badge-tie { background: linear-gradient(135deg, #6366f1, #4f46e5); }

.axis-winner-chip {
    display: inline-block;
    font-size: 0.68rem;
    font-weight: 600;
    padding: 3px 8px;
    border-radius: 999px;
    color: #fff;
    line-height: 1.3;
}

.legend-row {
    display: flex;
    flex-direction: column;
    gap: 8px;
    font-size: 0.72rem;
    color: var(--ink-muted);
    margin: 0.5rem 0 0;
}

.legend-item { display: flex; align-items: center; gap: 8px; }

.legend-swatch {
    width: 12px;
    height: 12px;
    border-radius: 3px;
    flex-shrink: 0;
}

/* ── Result callout ── */
.result-callout {
    border-radius: var(--radius-sm);
    padding: 0.9rem 1rem;
    font-size: 0.88rem;
    line-height: 1.55;
    margin: 0.75rem 0;
}

.result-callout.success {
    background: linear-gradient(135deg, #ecfdf5, #f0fdf4);
    border: 1px solid #86efac;
    color: #14532d;
}

.result-callout.info {
    background: linear-gradient(135deg, var(--brand-light), #fff);
    border: 1px solid #93c5fd;
    color: var(--brand);
}

/* ── Share box ── */
.share-box {
    background: var(--surface-2);
    border: 1px dashed #cbd5e1;
    border-radius: var(--radius-sm);
    padding: 0.85rem;
    margin-top: 0.5rem;
}

.share-url {
    font-size: 0.72rem;
    word-break: break-all;
    color: var(--ink-muted);
    line-height: 1.5;
    font-family: ui-monospace, monospace;
}

/* ── Footer ── */
.site-footer {
    margin-top: 2rem;
    padding-top: 1.25rem;
    border-top: 1px solid #e2e8f0;
    font-size: 0.75rem;
    color: var(--ink-muted);
    line-height: 1.65;
}

.site-footer h4 {
    font-size: 0.8rem;
    font-weight: 700;
    color: var(--ink);
    margin: 1rem 0 0.4rem 0;
}

/* ── Streamlit widgets (touch-friendly) ── */
.stButton > button {
    min-height: 44px !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: 0.78rem !important;
    border: 1px solid #c7d8f0 !important;
    background: linear-gradient(180deg, #fff 0%, #f0f5ff 100%) !important;
    color: #1e3a8a !important;
    transition: all 0.15s ease !important;
    box-shadow: 0 2px 6px rgba(30, 64, 175, 0.08) !important;
}

.stButton > button:hover {
    border-color: #3b82f6 !important;
    color: #1d4ed8 !important;
    background: linear-gradient(180deg, #eff6ff 0%, #dbeafe 100%) !important;
}

.stButton > button:active {
    transform: scale(0.98);
}

.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    background: var(--surface-2);
    border-radius: 12px;
    padding: 4px;
}

.stTabs [data-baseweb="tab"] {
    min-height: 44px;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    padding: 0 14px !important;
}

.stSlider label, .stSelectbox label, .stMultiSelect label,
.stNumberInput label, .stCheckbox label {
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    color: var(--ink) !important;
}

.stCaption { font-size: 0.75rem !important; color: var(--ink-muted) !important; }

div[data-testid="stExpander"] {
    border: 1px solid #e8edf3 !important;
    border-radius: var(--radius-sm) !important;
    background: var(--surface-2) !important;
}

div[data-baseweb="select"] > div {
    min-height: 44px !important;
    border-radius: 10px !important;
}

.stAlert {
    border-radius: var(--radius-sm) !important;
    font-size: 0.82rem !important;
}

/* Force single-column layout on phone */
@media (max-width: 768px) {
    [data-testid="column"] {
        width: 100% !important;
        flex: 1 1 100% !important;
        min-width: 100% !important;
    }

    [data-testid="stHorizontalBlock"] {
        flex-wrap: wrap !important;
        gap: 0.5rem !important;
    }

    .hero-banner h1 { font-size: 1.35rem !important; }

    .axis-summary-item {
        flex-direction: column;
        align-items: flex-start;
    }

    .axis-summary-item .winner-name {
        text-align: left;
        max-width: 100%;
    }
}

@media (min-width: 769px) {
    .axis-summary-grid {
        grid-template-columns: repeat(2, 1fr);
    }

    .insurance-row {
        grid-template-columns: repeat(2, 1fr);
    }

    .legend-row {
        flex-direction: row;
        flex-wrap: wrap;
        gap: 14px;
    }

    .block-container { max-width: 820px !important; }
}
</style>
"""


def inject_styles() -> None:
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


from contextlib import contextmanager


@contextmanager
def section(title: str, icon: str = ""):
    icon_html = f'<span style="opacity:0.7;font-size:0.9rem;">{icon}</span>' if icon else ""
    with st.container(border=True):
        st.markdown(
            f'<p class="section-title">{icon_html}{title}</p>',
            unsafe_allow_html=True,
        )
        yield


def card_header_color(card_id: str) -> str:
    return CARD_COLORS.get(card_id, "#475569")
