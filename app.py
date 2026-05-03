import json
from urllib.parse import urlencode

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st
import streamlit.components.v1 as components

# ============================================================================
# PAGE CONFIG & CUSTOM CSS
# ============================================================================

st.set_page_config(
    page_title="Cibercrimen Colombia · Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Premium Light Theme CSS ─────────────────────────────────────────────────
CUSTOM_CSS = """
<style>
    /* ── Google Font ─────────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    /* ── Root variables ──────────────────────────────────────── */
    :root {
        --bg-primary: #ffffff;
        --bg-card: #f4f6f9;
        --bg-card-hover: #ffffff;
        --border-card: rgba(30, 58, 95, 0.1);
        --border-glow: rgba(0, 180, 216, 0.3);
        --text-primary: #111111;
        --text-secondary: #1a1a1a;
        --text-muted: #4b5563;
        --accent-1: #1e3a5f; /* deep blue */
        --accent-2: #00b4d8; /* turquoise */
        --accent-3: #2d9e6b; /* emerald green */
        --accent-4: #6c63ff; /* soft violet */
        --gradient-1: linear-gradient(135deg, #1e3a5f, #6c63ff);
        --gradient-2: linear-gradient(135deg, #00b4d8, #2d9e6b);
        --gradient-3: linear-gradient(135deg, #6c63ff, #f472b6);
        --gradient-4: linear-gradient(135deg, #2d9e6b, #1e3a5f);
        --shadow-soft: 0 4px 12px rgba(0, 0, 0, 0.05);
        --shadow-hover: 0 8px 24px rgba(30, 58, 95, 0.12);
    }

    /* ── Global background ───────────────────────────────────── */
    .stApp {
        background: var(--bg-primary);
        font-family: 'Inter', sans-serif;
        color: var(--text-primary);
    }

    /* ── Sidebar ─────────────────────────────────────────────── */
    section[data-testid="stSidebar"] {
        background: #fdfdfd;
        border-right: 1px solid var(--border-card);
    }
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: var(--accent-1) !important;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    section[data-testid="stSidebar"] .stSelectbox label {
        color: var(--text-secondary) !important;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-size: 0.75rem;
    }

    /* ── Hide default hamburger & footer ──────────────────────  */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* ── Layout margins ──────────────────────────────────────── */
    .block-container {
        padding-top: 2.5rem !important;
        padding-bottom: 1rem !important;
    }

    /* ── Custom scrollbar ────────────────────────────────────── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg-card); }
    ::-webkit-scrollbar-thumb { background: var(--border-card); border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--accent-2); }

    /* ── Card containers ─────────────────────────────────────── */
    .glass-card {
        background: var(--bg-card);
        border: 1px solid var(--border-card);
        border-radius: 16px;
        padding: 1.5rem;
        transition: all 0.3s ease;
        box-shadow: var(--shadow-soft);
    }
    .glass-card:hover {
        background: var(--bg-card-hover);
        border-color: var(--border-glow);
        box-shadow: var(--shadow-hover);
    }

    /* ── KPI metric cards ────────────────────────────────────── */
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(2, minmax(180px, 1fr));
        gap: 1.2rem;
        margin-bottom: 1.5rem;
        width: min(100%, 980px);
        margin-left: auto;
        margin-right: auto;
    }
    .kpi-card {
        aspect-ratio: 1;
        max-width: 280px;
        background: var(--bg-card);
        border: 1px solid var(--border-card);
        border-radius: 14px;
        padding: 1rem 1.1rem;
        text-align: center;
        position: relative;
        overflow: hidden;
        transition: all 0.35s ease;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        box-shadow: var(--shadow-soft);
    }

    @media (min-width: 1250px) {
        .kpi-container {
            grid-template-columns: repeat(4, minmax(160px, 1fr));
            width: min(100%, 1200px);
        }
    }
    .kpi-container > .kpi-card:nth-child(odd) {
        margin-right: 0;
    }
    .kpi-card:hover {
        transform: translateY(-4px);
        border-color: var(--accent-2);
        background: var(--bg-card-hover);
        box-shadow: var(--shadow-hover);
    }
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 4px;
        border-radius: 14px 14px 0 0;
    }
    .kpi-card:nth-child(1)::before { background: var(--gradient-1); }
    .kpi-card:nth-child(2)::before { background: var(--gradient-2); }
    .kpi-card:nth-child(3)::before { background: var(--gradient-3); }
    .kpi-card:nth-child(4)::before { background: var(--gradient-4); }

    .kpi-icon { font-size: 1.6rem; margin-bottom: 0.3rem; }
    .kpi-label {
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--text-muted);
        margin-bottom: 0.35rem;
    }
    .kpi-value {
        font-size: 1.7rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        line-height: 1.1;
        word-break: break-word;
    }
    .kpi-card:nth-child(1) .kpi-value { color: var(--accent-1); }
    .kpi-card:nth-child(2) .kpi-value { color: var(--accent-2); }
    .kpi-card:nth-child(3) .kpi-value { color: var(--accent-4); }
    .kpi-card:nth-child(4) .kpi-value { color: var(--accent-3); }

    .kpi-sub {
        font-size: 0.72rem;
        color: var(--text-secondary);
        margin-top: 0.35rem;
        font-weight: 500;
    }

    
    /* ── Section titles ──────────────────────────────────────── */
    .section-title {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1.2rem;
    }
    .section-title .icon {
        font-size: 1.2rem;
        width: 2.6rem;
        height: 2.6rem;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 10px;
        flex-shrink: 0;
        box-shadow: var(--shadow-soft);
    }
    .section-title .icon.purple { background: rgba(108, 99, 255, 0.1); color: var(--accent-4); border: 1px solid rgba(108, 99, 255, 0.2); }
    .section-title .icon.cyan   { background: rgba(0, 180, 216, 0.1); color: var(--accent-2); border: 1px solid rgba(0, 180, 216, 0.2); }
    .section-title .icon.pink   { background: rgba(30, 58, 95, 0.1); color: var(--accent-1); border: 1px solid rgba(30, 58, 95, 0.2); }
    .section-title .icon.yellow { background: rgba(45, 158, 107, 0.1); color: var(--accent-3); border: 1px solid rgba(45, 158, 107, 0.2); }

    .section-title h3 {
        margin: 0 !important;
        padding: 0 !important;
        font-size: 1.15rem !important;
        font-weight: 800 !important;
        color: var(--accent-1) !important;
        letter-spacing: -0.01em;
        flex: 1;
        min-width: 150px;
    }
    .section-title .badge {
        font-size: 0.65rem;
        font-weight: 700;
        padding: 0.25rem 0.75rem;
        border-radius: 999px;
        background: rgba(30, 58, 95, 0.08);
        color: var(--accent-1);
        margin-left: auto;
        flex-shrink: 0;
        border: 1px solid rgba(30, 58, 95, 0.15);
    }

    @media (max-width: 768px) {
        .section-title { gap: 0.5rem; margin-bottom: 0.8rem; }
        .section-title .icon { font-size: 1.1rem; width: 2.1rem; height: 2.1rem; }
        .section-title h3 { font-size: 1rem !important; min-width: 120px; }
        .section-title .badge { font-size: 0.6rem; padding: 0.15rem 0.5rem; }
    }

    @media (max-width: 480px) {
        .section-title { gap: 0.4rem; }
        .section-title .icon { font-size: 0.95rem; width: 1.9rem; height: 1.9rem; }
        .section-title h3 { font-size: 0.9rem !important; min-width: auto; }
        .section-title .badge { width: 100%; text-align: center; font-size: 0.55rem; margin-left: 0; margin-top: 0.3rem; }
    }

    /* ── Hero header ─────────────────────────────────────────── */
    .hero {
        text-align: center;
        padding: 2.5rem 0 1.5rem 0;
    }
    .hero h1 {
        font-size: 2.6rem;
        font-weight: 900;
        letter-spacing: -0.04em;
        background: var(--gradient-1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        line-height: 1.15;
    }
    .hero p {
        color: var(--text-secondary);
        font-size: 0.95rem;
        font-weight: 400;
        max-width: 650px;
        margin: 0 auto;
        line-height: 1.6;
    }
    .hero .tag {
        display: inline-block;
        margin-top: 0.8rem;
        font-size: 0.7rem;
        font-weight: 700;
        padding: 0.35rem 1rem;
        border-radius: 999px;
        background: rgba(0, 180, 216, 0.1);
        color: var(--accent-2);
        border: 1px solid rgba(0, 180, 216, 0.25);
    }

    /* ── Plotly chart containers ──────────────────────────────── */
    .stPlotlyChart {
        border-radius: 12px;
        overflow: hidden;
        width: 100% !important;
        box-shadow: var(--shadow-soft);
        background: #0f172a;
    }

    /* ── Dividers ─────────────────────────────────────────────── */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--border-card), transparent);
        margin: 2rem 0;
    }

    /* ── Tip box ──────────────────────────────────────────────── */
    .tip-box {
        background: rgba(45, 158, 107, 0.05);
        border: 1px solid rgba(45, 158, 107, 0.2);
        border-radius: 12px;
        padding: 0.8rem 1.2rem;
        font-size: 0.82rem;
        color: var(--text-secondary);
        margin-bottom: 1.2rem;
        display: flex;
        align-items: center;
        gap: 0.6rem;
        box-shadow: var(--shadow-soft);
    }
    .tip-box .tip-icon { font-size: 1.2rem; color: var(--accent-3); }
    
    /* ── Streamlit Native UI Adjustments ──────────────────────── */
    div.stButton > button {
        background: var(--bg-card);
        color: var(--accent-1);
        border: 1px solid var(--border-card);
        box-shadow: var(--shadow-soft);
        font-weight: 600;
        transition: all 0.2s ease;
    }
    div.stButton > button:hover {
        background: var(--accent-1);
        color: #fff;
        border-color: var(--accent-1);
        box-shadow: var(--shadow-hover);
    }

    /* ── Footer / Glossary ────────────────────────────────────── */
    .glossary-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 1.2rem;
        margin-top: 1rem;
    }
    .glossary-card {
        background: var(--bg-card);
        border: 1px solid var(--border-card);
        border-radius: 16px;
        padding: 1.5rem;
        min-height: 142px;
        box-shadow: var(--shadow-soft);
        transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
    }
    .glossary-card:hover {
        transform: translateY(-4px);
        background: var(--bg-card-hover);
        border-color: var(--accent-2);
        box-shadow: var(--shadow-hover);
    }
    .glossary-card-header {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        margin-bottom: 1rem;
    }
    .glossary-card-icon {
        font-size: 1.1rem;
        line-height: 1;
        color: var(--accent-1);
    }
    .glossary-card h4 {
        margin: 0 !important;
        font-size: 1rem !important;
        font-weight: 800 !important;
        line-height: 1.3;
        color: var(--accent-1) !important;
        letter-spacing: -0.01em;
    }
    .glossary-card p {
        margin: 0 !important;
        color: var(--text-primary) !important;
        font-size: 0.9rem !important;
        line-height: 1.6;
    }

    @media (max-width: 1100px) {
        .glossary-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    }

    @media (max-width: 768px) {
        .glossary-grid { grid-template-columns: 1fr; gap: 1rem; }
        .glossary-card { min-height: auto; padding: 1.2rem; }
        .glossary-card h4 { font-size: 0.95rem !important; }
        .glossary-card p { font-size: 0.85rem !important; }
    }

    @media (max-width: 480px) {
        .glossary-card-icon { font-size: 0.9rem; }
        .glossary-card h4 { font-size: 0.9rem !important; }
        .glossary-card p { font-size: 0.85rem !important; line-height: 1.5; }
    }

    /* ── Responsive adjustments ──────────────────────────────── */
    @media (max-width: 768px) {
        .tip-box { padding: 0.7rem 1rem; font-size: 0.75rem; gap: 0.5rem; }
        .tip-box .tip-icon { font-size: 1rem; flex-shrink: 0; }
    }
    @media (max-width: 480px) {
        .tip-box { padding: 0.6rem 0.8rem; font-size: 0.7rem; }
        .tip-box .tip-icon { font-size: 0.9rem; }
    }
    @media (max-width: 768px) {
        .block-container { padding-top: 1.5rem !important; padding-left: 0.8rem !important; padding-right: 0.8rem !important; }
    }
    @media (max-width: 480px) {
        .block-container { padding-top: 1rem !important; padding-left: 0.5rem !important; padding-right: 0.5rem !important; }
    }

    .dashboard-footer {
        text-align: center;
        padding: 2rem 0 1rem 0;
        color: var(--text-muted);
        font-size: 0.75rem;
    }
    .dashboard-footer a { color: var(--accent-1); text-decoration: none; font-weight: 600; }

    @media (max-width: 768px) {
        .dashboard-footer { padding: 1.5rem 0 0.75rem 0; font-size: 0.7rem; }
    }
    @media (max-width: 480px) {
        .dashboard-footer { padding: 1rem 0 0.5rem 0; font-size: 0.65rem; }
    }

    .startup-target-text { color: #000000; }

    /* ══════════════════════════════════════════════════════════
       ── DETAIL VIEW – navegación interna dinámica ───────────
       ══════════════════════════════════════════════════════════ */

    /* Breadcrumb / back-bar */
    .detail-breadcrumb {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        font-size: 0.78rem;
        color: var(--text-muted);
        margin-bottom: 1.6rem;
        flex-wrap: wrap;
    }
    .detail-breadcrumb .bc-home {
        color: var(--accent-1);
        font-weight: 600;
        cursor: pointer;
        text-decoration: underline;
        text-underline-offset: 2px;
    }
    .detail-breadcrumb .bc-sep { opacity: 0.45; }
    .detail-breadcrumb .bc-current {
        font-weight: 700;
        color: var(--text-primary);
    }

    /* Detail hero strip */
    .detail-hero {
        background: linear-gradient(135deg, #1e3a5f 0%, #6c63ff 100%);
        border-radius: 18px;
        padding: 2rem 2.4rem;
        margin-bottom: 1.8rem;
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        box-shadow: 0 8px 32px rgba(30, 58, 95, 0.18);
    }
    .detail-hero.cyan  { background: linear-gradient(135deg, #00b4d8 0%, #2d9e6b 100%); }
    .detail-hero.violet { background: linear-gradient(135deg, #6c63ff 0%, #f472b6 100%); }
    .detail-hero.green  { background: linear-gradient(135deg, #2d9e6b 0%, #1e3a5f 100%); }

    .detail-hero .dh-eyebrow {
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: rgba(255,255,255,0.7);
    }
    .detail-hero .dh-title {
        font-size: 2rem;
        font-weight: 900;
        letter-spacing: -0.03em;
        color: #ffffff;
        line-height: 1.15;
    }
    .detail-hero .dh-value {
        font-size: 3rem;
        font-weight: 900;
        letter-spacing: -0.04em;
        color: #ffffff;
        line-height: 1;
        margin-top: 0.3rem;
    }
    .detail-hero .dh-sub {
        font-size: 0.88rem;
        color: rgba(255,255,255,0.75);
        font-weight: 500;
        margin-top: 0.15rem;
    }

    @media (max-width: 768px) {
        .detail-hero { padding: 1.5rem 1.6rem; }
        .detail-hero .dh-title { font-size: 1.4rem; }
        .detail-hero .dh-value { font-size: 2.2rem; }
    }

    /* Stats grid inside detail */
    .detail-stats-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin-bottom: 1.6rem;
    }
    @media (max-width: 900px) {
        .detail-stats-grid { grid-template-columns: repeat(2, 1fr); }
    }
    @media (max-width: 560px) {
        .detail-stats-grid { grid-template-columns: 1fr; }
    }

    .detail-stat-card {
        background: var(--bg-card);
        border: 1px solid var(--border-card);
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
        box-shadow: var(--shadow-soft);
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }
    .detail-stat-card:hover {
        transform: translateY(-3px);
        box-shadow: var(--shadow-hover);
        border-color: var(--border-glow);
    }
    .detail-stat-card .dsc-label {
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--text-muted);
        margin-bottom: 0.45rem;
    }
    .detail-stat-card .dsc-value {
        font-size: 1.35rem;
        font-weight: 800;
        color: var(--accent-1);
        line-height: 1.15;
        letter-spacing: -0.02em;
    }
    .detail-stat-card .dsc-note {
        font-size: 0.72rem;
        color: var(--text-muted);
        margin-top: 0.25rem;
    }

    /* Insight box */
    .detail-insight {
        background: rgba(0, 180, 216, 0.04);
        border: 1px solid rgba(0, 180, 216, 0.2);
        border-radius: 14px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1.6rem;
        display: flex;
        gap: 0.8rem;
        align-items: flex-start;
    }
    .detail-insight .di-icon {
        font-size: 1.4rem;
        flex-shrink: 0;
        margin-top: 0.1rem;
    }
    .detail-insight .di-body { flex: 1; }
    .detail-insight .di-body strong {
        display: block;
        font-size: 0.88rem;
        font-weight: 800;
        color: var(--accent-1);
        margin-bottom: 0.3rem;
    }
    .detail-insight .di-body p {
        margin: 0;
        font-size: 0.84rem;
        color: var(--text-secondary);
        line-height: 1.55;
    }

    div[data-testid="element-container"]:has(.detail-chart-anchor) + div[data-testid="element-container"] {
        max-width: 100%;
        overflow-x: hidden;
    }
    div[data-testid="element-container"]:has(.detail-chart-anchor) + div[data-testid="element-container"] div[data-testid="stPlotlyChart"] {
        width: 100% !important;
        max-width: 100%;
        overflow-x: hidden;
    }
    div[data-testid="element-container"]:has(.detail-chart-anchor) + div[data-testid="element-container"] div[data-testid="stPlotlyChart"] > div,
    div[data-testid="element-container"]:has(.detail-chart-anchor) + div[data-testid="element-container"] .js-plotly-plot,
    div[data-testid="element-container"]:has(.detail-chart-anchor) + div[data-testid="element-container"] .plotly,
    div[data-testid="element-container"]:has(.detail-chart-anchor) + div[data-testid="element-container"] .plot-container {
        width: 100% !important;
        max-width: 100% !important;
        overflow-x: hidden !important;
    }

    @media (max-width: 480px) {
        div[data-testid="element-container"]:has(.detail-chart-anchor) + div[data-testid="element-container"] .xtick text,
        div[data-testid="element-container"]:has(.detail-chart-anchor) + div[data-testid="element-container"] .ytick text,
        div[data-testid="element-container"]:has(.detail-chart-anchor) + div[data-testid="element-container"] .legendtext,
        div[data-testid="element-container"]:has(.detail-chart-anchor) + div[data-testid="element-container"] .annotation-text,
        div[data-testid="element-container"]:has(.detail-chart-anchor) + div[data-testid="element-container"] .textpoint text {
            font-size: 10px !important;
        }
    }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def _inject_plotly_hover_close_bridge():
    """Agrega un botÃ³n de cierre a los tooltips nativos de Plotly sin tocar cada grÃ¡fico."""
    components.html(
        """
        <style>
            html, body {
                margin: 0;
                padding: 0;
                overflow: hidden;
            }
        </style>
        <script>
            (() => {
                let hostWindow = window;
                let hostDocument = document;

                try {
                    if (window.parent && window.parent !== window && window.parent.document) {
                        hostWindow = window.parent;
                        hostDocument = window.parent.document;
                    }
                } catch (error) {
                    return;
                }

                if (hostWindow.__plotlyHoverCloseBridgeInstalled) {
                    return;
                }
                hostWindow.__plotlyHoverCloseBridgeInstalled = true;

                const STYLE_ID = "plotly-hover-close-bridge-style";
                if (!hostDocument.getElementById(STYLE_ID)) {
                    const style = hostDocument.createElement("style");
                    style.id = STYLE_ID;
                    style.textContent = `
                        .plotly-hover-close-btn {
                            position: absolute;
                            z-index: 30;
                            width: 22px;
                            height: 22px;
                            display: inline-flex;
                            align-items: center;
                            justify-content: center;
                            border: 1px solid rgba(148, 163, 184, 0.85);
                            border-radius: 999px;
                            background: rgba(255, 255, 255, 0.98);
                            color: #0f172a;
                            font-size: 14px;
                            font-weight: 700;
                            line-height: 1;
                            cursor: pointer;
                            box-shadow: 0 6px 16px rgba(15, 23, 42, 0.16);
                            opacity: 0;
                            pointer-events: none;
                            padding: 0;
                            transform: translate(-9999px, -9999px);
                            transition: opacity 0.12s ease;
                        }
                        .plotly-hover-close-btn:hover {
                            background: #f8fafc;
                            border-color: rgba(100, 116, 139, 0.9);
                        }
                        .plotly-hover-close-btn:focus-visible {
                            outline: 2px solid rgba(59, 130, 246, 0.65);
                            outline-offset: 1px;
                        }
                    `;
                    hostDocument.head.appendChild(style);
                }

                const hideButton = (button) => {
                    if (!button) return;
                    button.style.opacity = "0";
                    button.style.pointerEvents = "none";
                    button.style.transform = "translate(-9999px, -9999px)";
                };

                const getVisibleHoverLabels = (plot) =>
                    Array.from(plot.querySelectorAll(".hoverlayer .hovertext")).filter((node) => {
                        const rect = node.getBoundingClientRect();
                        return rect.width > 0 && rect.height > 0;
                    });

                const syncButton = (plot) => {
                    const button = plot.__plotlyHoverCloseButton;
                    if (!button) return;

                    const labels = getVisibleHoverLabels(plot);
                    if (!labels.length) {
                        hideButton(button);
                        return;
                    }

                    const plotRect = plot.getBoundingClientRect();
                    const bounds = labels.reduce((acc, node) => {
                        const rect = node.getBoundingClientRect();
                        return {
                            top: Math.min(acc.top, rect.top),
                            right: Math.max(acc.right, rect.right),
                            bottom: Math.max(acc.bottom, rect.bottom),
                            left: Math.min(acc.left, rect.left),
                        };
                    }, {
                        top: Number.POSITIVE_INFINITY,
                        right: Number.NEGATIVE_INFINITY,
                        bottom: Number.NEGATIVE_INFINITY,
                        left: Number.POSITIVE_INFINITY,
                    });

                    const buttonSize = 22;
                    const left = Math.min(
                        Math.max(plotRect.width - buttonSize - 6, 6),
                        Math.max(bounds.right - plotRect.left - buttonSize - 4, 6),
                    );
                    const top = Math.max(bounds.top - plotRect.top + 4, 6);

                    button.style.transform = `translate(${left}px, ${top}px)`;
                    button.style.opacity = "1";
                    button.style.pointerEvents = "auto";
                };

                const bindPlot = (plot) => {
                    if (!plot || plot.dataset.hoverCloseBound === "1") {
                        return;
                    }

                    if (typeof plot.on !== "function") {
                        hostWindow.requestAnimationFrame(() => bindPlot(plot));
                        return;
                    }

                    plot.dataset.hoverCloseBound = "1";
                    if (hostWindow.getComputedStyle(plot).position === "static") {
                        plot.style.position = "relative";
                    }

                    const button = hostDocument.createElement("button");
                    button.type = "button";
                    button.className = "plotly-hover-close-btn";
                    button.innerHTML = "&times;";
                    button.setAttribute("aria-label", "Cerrar tooltip");
                    button.title = "Cerrar";
                    button.addEventListener("click", (event) => {
                        event.preventDefault();
                        event.stopPropagation();
                        try {
                            hostWindow.Plotly?.Fx?.unhover?.(plot);
                        } catch (error) {
                            // No-op: el botÃ³n debe ser seguro aunque Plotly cambie.
                        }
                        hideButton(button);
                    });

                    plot.appendChild(button);
                    plot.__plotlyHoverCloseButton = button;

                    const scheduleSync = () => hostWindow.requestAnimationFrame(() => syncButton(plot));

                    plot.on("plotly_hover", scheduleSync);
                    plot.on("plotly_click", scheduleSync);
                    plot.on("plotly_afterplot", scheduleSync);
                    plot.on("plotly_redraw", scheduleSync);
                    plot.on("plotly_relayout", scheduleSync);
                    plot.on("plotly_unhover", () => hostWindow.setTimeout(() => syncButton(plot), 0));
                    plot.addEventListener("mouseleave", () => hostWindow.setTimeout(() => syncButton(plot), 0), {
                        passive: true,
                    });

                    scheduleSync();
                };

                const scanPlots = () => {
                    hostDocument.querySelectorAll(".js-plotly-plot").forEach(bindPlot);
                };

                scanPlots();

                const observer = new hostWindow.MutationObserver(() => scanPlots());
                observer.observe(hostDocument.body, { childList: true, subtree: true });
            })();
        </script>
        """,
        height=0,
    )


_inject_plotly_hover_close_bridge()

# ============================================================================
# CONFIG
# ============================================================================

BASE_API = "https://www.datos.gov.co/resource/4v6r-wu98.json"
MAPA_URL = "https://raw.githubusercontent.com/jacasta2/colombian_map/main/from_shapefiles/departamentos/mapa_departamentos_q3.json"
MAPA_MUNICIPIOS_URL = "https://raw.githubusercontent.com/jacasta2/colombian_map/main/from_shapefiles/municipios/mapa_municipios_q3.json"
HISTORICAL_YEAR_START = 2006
HISTORICAL_YEAR_END = 2025
MAPA_COLOMBIA_LOADING_TEXT = "Cargando mapa de Colombia..."
MAPA_MUNICIPAL_LOADING_TEXT = "Cargando mapa municipal..."
API_LOADING_TEXT = "Consultando datos desde la API..."
API_DEPTO_EMPTY_TEXT = "La API no devolvió datos por departamento."

# ── Shared Plotly layout template ────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#cbd5e1"),
    hoverlabel=dict(
        bgcolor="#1e293b",
        font_size=13,
        font_family="Inter, sans-serif",
        font_color="#e2e8f0",
        bordercolor="#334155",
    ),
    margin=dict(t=10, b=40, l=50, r=20),
)

# ============================================================================
# SESSION STATE – navegación interna
# ============================================================================
# `active_view` puede ser: None (vista principal) o una clave de KPI:
#   "total_casos" | "depto_top" | "delito_top" | "anio_pico"

if "active_view" not in st.session_state:
    st.session_state.active_view = None

if "pending_scroll_reset" not in st.session_state:
    st.session_state.pending_scroll_reset = False

if "scroll_reset_nonce" not in st.session_state:
    st.session_state.scroll_reset_nonce = 0


def _schedule_scroll_reset():
    """Marca un reset de scroll para el siguiente cambio dashboard <-> detalle."""
    st.session_state.pending_scroll_reset = True
    st.session_state.scroll_reset_nonce += 1


def _render_pending_scroll_reset():
    """Resetea el scroll sólo al entrar al dashboard o a una sub-vista KPI."""
    if not st.session_state.get("pending_scroll_reset"):
        return

    nonce = st.session_state.get("scroll_reset_nonce", 0)
    components.html(
        f"""
        <script>
            const resetScrollPosition = () => {{
                const parentWindow = window.parent;
                const targets = [
                    window,
                    document.documentElement,
                    document.body,
                    parentWindow,
                    parentWindow?.document?.documentElement,
                    parentWindow?.document?.body,
                    parentWindow?.document?.querySelector('section.main'),
                    parentWindow?.document?.querySelector('[data-testid="stAppViewContainer"]'),
                    parentWindow?.document?.querySelector('[data-testid="block-container"]'),
                ];

                targets.forEach((target) => {{
                    try {{
                        if (!target) return;
                        if (typeof target.scrollTo === "function") {{
                            target.scrollTo(0, 0);
                        }}
                        if ("scrollTop" in target) {{
                            target.scrollTop = 0;
                        }}
                    }} catch (error) {{
                        // Ignore cross-context issues and keep the transition silent.
                    }}
                }});
            }};

            resetScrollPosition();
            requestAnimationFrame(resetScrollPosition);
            setTimeout(resetScrollPosition, 0);
        </script>
        <div data-scroll-reset="{nonce}" style="height:0;"></div>
        """,
        height=0,
    )
    st.session_state.pending_scroll_reset = False


def navigate_to(view_key: str):
    """Cambia la vista activa sin recargar toda la app."""
    st.session_state.active_view = view_key
    _schedule_scroll_reset()


def navigate_home():
    """Regresa a la vista principal."""
    st.session_state.active_view = None
    _schedule_scroll_reset()


# ============================================================================
# HELPERS
# ============================================================================

def preparar_participacion_geografica(df, casos_col="Casos"):
    df = df.copy()
    total_casos = float(df[casos_col].sum())
    if total_casos <= 0:
        df["Pct_Seleccionado"] = 0.0
        df["Pct_Resto"] = 0.0
    else:
        df["Pct_Seleccionado"] = (df[casos_col] / total_casos) * 100
        df["Pct_Resto"] = 100 - df["Pct_Seleccionado"]
    return df


def formatear_delito_principal_popup(valor):
    if pd.isna(valor):
        return "Sin dato"
    texto = str(valor).strip()
    if not texto:
        return "Sin dato"
    encabezado, separador, _ = texto.partition(".")
    return encabezado.strip() if separador and encabezado.strip() else texto


def truncateArticle(fullText: str) -> str:
    if fullText is None:
        return fullText
    text = str(fullText)
    if not text:
        return fullText
    dotIndex = text.find(".")
    return text[:dotIndex].strip() if dotIndex != -1 else text.strip()


def render_target_text(text):
    return f'<div class="startup-target-text">{text}</div>'


def ejecutar_con_texto_temporal(text, callback):
    placeholder = st.empty()
    placeholder.markdown(render_target_text(text), unsafe_allow_html=True)
    try:
        return callback()
    finally:
        placeholder.empty()


def construir_mapa_con_panel(
    fig,
    component_id,
    height,
    panel_title,
    placeholder_text,
    selected_label,
    other_label,
    selected_color,
    other_color,
    cases_idx,
    crime_idx,
    selected_pct_idx,
    other_pct_idx,
    subtitle_idx=None,
    subtitle_prefix="",
):
    plot_id = f"plot-{component_id}"
    wrapper_id = f"map-wrapper-{component_id}"
    card_id = f"map-card-{component_id}"
    content_id = f"map-content-{component_id}"
    close_id = f"map-close-{component_id}"

    panel_config = {
        "panel_title": panel_title,
        "placeholder": placeholder_text,
        "selected_label": selected_label,
        "other_label": other_label,
        "selected_color": selected_color,
        "other_color": other_color,
        "cases_idx": cases_idx,
        "crime_idx": crime_idx,
        "selected_pct_idx": selected_pct_idx,
        "other_pct_idx": other_pct_idx,
        "subtitle_idx": subtitle_idx,
        "subtitle_prefix": subtitle_prefix,
    }

    plot_html = fig.to_html(
        full_html=False,
        include_plotlyjs="cdn",
        config={
            "responsive": True,
            "displayModeBar": False,
            "scrollZoom": False,
        },
        default_width="100%",
        default_height=f"{height}px",
        div_id=plot_id,
    )

    html = f"""
    <div id="{wrapper_id}" class="map-panel-shell">
        <style>
            #{wrapper_id} {{
                position: relative;
                width: 100%;
            }}
            #{wrapper_id} .map-panel-shell__plot {{
                width: 100%;
            }}
            #{wrapper_id} .map-panel-shell__plot .plotly-graph-div {{
                width: 100% !important;
            }}
            #{card_id} {{
                position: absolute;
                top: 16px;
                right: 16px;
                width: min(260px, calc(100% - 32px));
                padding: 0.95rem 1rem 0.9rem;
                border-radius: 16px;
                border: 1px solid rgba(148, 163, 184, 0.35);
                background: rgba(255, 255, 255, 0.96);
                box-shadow: 0 12px 28px rgba(15, 23, 42, 0.18);
                backdrop-filter: blur(10px);
                z-index: 6;
                pointer-events: auto;
                opacity: 0;
                visibility: hidden;
            }}
            #{card_id}.is-visible {{
                opacity: 1;
                visibility: visible;
            }}
            #{card_id}.is-empty {{
                border-style: dashed;
            }}
            #{card_id} .map-panel-card__header {{
                display: flex;
                align-items: flex-start;
                justify-content: space-between;
                gap: 0.65rem;
            }}
            #{card_id} .map-panel-card__eyebrow {{
                margin-bottom: 0.35rem;
                font-size: 0.68rem;
                font-weight: 700;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                color: #475569;
            }}
            #{card_id} .map-panel-card__close {{
                width: 24px;
                height: 24px;
                flex: 0 0 24px;
                border: 1px solid rgba(148, 163, 184, 0.65);
                border-radius: 999px;
                background: rgba(255, 255, 255, 0.96);
                color: #0f172a;
                font-size: 1rem;
                font-weight: 700;
                line-height: 1;
                cursor: pointer;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                padding: 0;
                margin: -0.1rem -0.1rem 0 0;
            }}
            #{card_id} .map-panel-card__close:hover {{
                background: #f8fafc;
            }}
            #{card_id} .map-panel-card__close:focus-visible {{
                outline: 2px solid rgba(59, 130, 246, 0.55);
                outline-offset: 1px;
            }}
            #{card_id} .map-panel-card__title {{
                margin: 0;
                font-size: 1rem;
                font-weight: 800;
                color: #0f172a;
                line-height: 1.2;
            }}
            #{card_id} .map-panel-card__subtitle {{
                margin-top: 0.2rem;
                font-size: 0.78rem;
                color: #475569;
                font-weight: 600;
            }}
            #{card_id} .map-panel-card__placeholder {{
                font-size: 0.82rem;
                line-height: 1.5;
                color: #475569;
            }}
            #{card_id} .map-panel-card__metric {{
                margin-top: 0.7rem;
                display: flex;
                justify-content: space-between;
                gap: 0.8rem;
                align-items: flex-start;
                font-size: 0.82rem;
            }}
            #{card_id} .map-panel-card__metric-label {{
                color: #475569;
                font-weight: 700;
            }}
            #{card_id} .map-panel-card__metric-value {{
                color: #0f172a;
                font-weight: 800;
                text-align: right;
            }}
            #{card_id} .map-panel-card__metric--stack {{
                display: block;
            }}
            #{card_id} .map-panel-card__metric--stack .map-panel-card__metric-value {{
                display: block;
                margin-top: 0.28rem;
                text-align: left;
                font-weight: 700;
                line-height: 1.35;
            }}
            #{card_id} .map-panel-card__pie-block {{
                margin-top: 0.85rem;
                padding-top: 0.75rem;
                border-top: 1px solid rgba(148, 163, 184, 0.28);
                display: flex;
                gap: 0.75rem;
                align-items: center;
            }}
            #{card_id} .map-panel-card__pie-figure {{
                position: relative;
                width: 94px;
                height: 94px;
                flex: 0 0 94px;
            }}
            #{card_id} .map-panel-card__pie-figure svg {{
                width: 94px;
                height: 94px;
                display: block;
            }}
            #{card_id} .map-panel-card__pie-center {{
                position: absolute;
                inset: 0;
                display: flex;
                align-items: center;
                justify-content: center;
                text-align: center;
                font-size: 0.72rem;
                font-weight: 800;
                color: #ffffff;
                line-height: 1.15;
            }}
            #{card_id} .map-panel-card__pie-center span {{
                color: #ffffff !important;
            }}
            #{card_id} .map-panel-card__legend {{
                flex: 1 1 auto;
                display: grid;
                gap: 0.4rem;
            }}
            #{card_id} .map-panel-card__legend-row {{
                display: flex;
                align-items: center;
                gap: 0.45rem;
                font-size: 0.76rem;
                color: #334155;
                line-height: 1.25;
            }}
            #{card_id} .map-panel-card__legend-swatch {{
                width: 10px;
                height: 10px;
                border-radius: 999px;
                flex: 0 0 10px;
            }}
            #{card_id} .map-panel-card__legend-row strong {{
                margin-left: auto;
                color: #0f172a;
                font-size: 0.78rem;
            }}
            #{card_id} .map-panel-card__footnote {{
                margin-top: 0.55rem;
                font-size: 0.72rem;
                color: #64748b;
                line-height: 1.35;
            }}
            @media (max-width: 768px) {{
                #{card_id} {{
                    top: auto;
                    bottom: 12px;
                    right: 12px;
                    left: 12px;
                    width: auto;
                    max-width: none;
                    padding: 0.85rem 0.9rem 0.8rem;
                }}
                #{card_id} .map-panel-card__pie-block {{
                    gap: 0.65rem;
                }}
            }}
        </style>

        <div class="map-panel-shell__plot">
            {plot_html}
        </div>

        <div id="{card_id}" class="map-panel-card is-empty">
            <div class="map-panel-card__header">
                <div class="map-panel-card__eyebrow">{panel_title}</div>
                <button id="{close_id}" type="button" class="map-panel-card__close" aria-label="Cerrar detalle">&times;</button>
            </div>
            <div id="{content_id}">
                <div class="map-panel-card__placeholder">{placeholder_text}</div>
            </div>
        </div>
    </div>

    <script>
        (() => {{
            const plot = document.getElementById("{plot_id}");
            const card = document.getElementById("{card_id}");
            const content = document.getElementById("{content_id}");
            const closeButton = document.getElementById("{close_id}");
            const cfg = {json.dumps(panel_config, ensure_ascii=False)};
            let pinnedPayload = null;

            const escapeHtml = (value) => String(value ?? "")
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;")
                .replace(/"/g, "&quot;")
                .replace(/'/g, "&#39;");

            const formatNumber = (value) =>
                new Intl.NumberFormat("es-CO").format(Math.round(Number(value) || 0));

            const formatPercent = (value) => `${{(Number(value) || 0).toFixed(1)}}%`;

            function polarToCartesian(cx, cy, radius, angleDegrees) {{
                const angle = (angleDegrees - 90) * Math.PI / 180.0;
                return {{
                    x: cx + (radius * Math.cos(angle)),
                    y: cy + (radius * Math.sin(angle)),
                }};
            }}

            function buildSlicePath(percentage) {{
                const pct = Math.max(0, Math.min(100, Number(percentage) || 0));
                if (pct <= 0) return "";
                if (pct >= 100) {{
                    return `<circle cx="50" cy="50" r="40" fill="${{cfg.selected_color}}"></circle>`;
                }}
                const start = polarToCartesian(50, 50, 40, 0);
                const end = polarToCartesian(50, 50, 40, (pct / 100) * 360);
                const largeArcFlag = pct > 50 ? 1 : 0;
                return `
                    <path
                        d="M 50 50 L ${{start.x}} ${{start.y}} A 40 40 0 ${{largeArcFlag}} 1 ${{end.x}} ${{end.y}} Z"
                        fill="${{cfg.selected_color}}">
                    </path>
                `;
            }}

            function renderPie(selectedPct, otherPct) {{
                const selected = Math.max(0, Math.min(100, Number(selectedPct) || 0));
                const other = Math.max(0, Math.min(100, Number(otherPct) || 0));
                return `
                    <div class="map-panel-card__pie-block">
                        <div class="map-panel-card__pie-figure">
                            <svg viewBox="0 0 100 100" aria-hidden="true">
                                <circle cx="50" cy="50" r="40" fill="${{cfg.other_color}}"></circle>
                                ${{buildSlicePath(selected)}}
                                <circle cx="50" cy="50" r="40" fill="none" stroke="rgba(255,255,255,0.7)" stroke-width="1.4"></circle>
                            </svg>
                            <div class="map-panel-card__pie-center">
                                <div>${{formatPercent(selected)}}<br><span style="font-size:0.63rem;font-weight:700;color:#475569;">del total</span></div>
                            </div>
                        </div>
                        <div class="map-panel-card__legend">
                            <div class="map-panel-card__legend-row">
                                <span class="map-panel-card__legend-swatch" style="background:${{cfg.selected_color}};"></span>
                                <span>${{escapeHtml(cfg.selected_label)}}</span>
                                <strong>${{formatPercent(selected)}}</strong>
                            </div>
                            <div class="map-panel-card__legend-row">
                                <span class="map-panel-card__legend-swatch" style="background:${{cfg.other_color}};"></span>
                                <span>${{escapeHtml(cfg.other_label)}}</span>
                                <strong>${{formatPercent(other)}}</strong>
                            </div>
                        </div>
                    </div>
                `;
            }}

            function extractPayload(point) {{
                if (!point) return null;
                const customdata = Array.isArray(point.customdata) ? point.customdata : [];
                return {{
                    title: point.hovertext || point.location || cfg.panel_title,
                    subtitle: cfg.subtitle_idx === null ? "" : String(customdata[cfg.subtitle_idx] ?? ""),
                    cases: Number(customdata[cfg.cases_idx] ?? point.z ?? 0),
                    crime: String(customdata[cfg.crime_idx] ?? "Sin dato"),
                    selectedPct: Number(customdata[cfg.selected_pct_idx] ?? 0),
                    otherPct: Number(customdata[cfg.other_pct_idx] ?? 0),
                }};
            }}

            function renderPayload(payload) {{
                card.classList.remove("is-empty");
                card.classList.add("is-visible");
                const subtitleHtml = payload.subtitle
                    ? `<div class="map-panel-card__subtitle">${{escapeHtml(cfg.subtitle_prefix)}}${{escapeHtml(payload.subtitle)}}</div>`
                    : "";
                content.innerHTML = `
                    <h4 class="map-panel-card__title">${{escapeHtml(payload.title)}}</h4>
                    ${{subtitleHtml}}
                    <div class="map-panel-card__metric">
                        <span class="map-panel-card__metric-label">Casos</span>
                        <strong class="map-panel-card__metric-value">${{formatNumber(payload.cases)}}</strong>
                    </div>
                    <div class="map-panel-card__metric map-panel-card__metric--stack">
                        <span class="map-panel-card__metric-label">Delito principal</span>
                        <strong class="map-panel-card__metric-value">${{escapeHtml(payload.crime || "Sin dato")}}</strong>
                    </div>
                    ${{renderPie(payload.selectedPct, payload.otherPct)}}
                    <div class="map-panel-card__footnote">Participación calculada sobre el total visible en este mapa.</div>
                `;
            }}

            function showPlaceholder() {{
                if (pinnedPayload) {{
                    renderPayload(pinnedPayload);
                    return;
                }}
                card.classList.add("is-empty");
                card.classList.remove("is-visible");
                content.innerHTML = `<div class="map-panel-card__placeholder">${{escapeHtml(cfg.placeholder)}}</div>`;
            }}

            function dismissCard() {{
                pinnedPayload = null;
                card.classList.remove("is-visible");
                card.classList.remove("is-empty");
            }}

            function bindEvents() {{
                if (!plot || typeof plot.on !== "function") {{
                    window.requestAnimationFrame(bindEvents);
                    return;
                }}
                if (closeButton) {{
                    closeButton.addEventListener("click", (event) => {{
                        event.preventDefault();
                        event.stopPropagation();
                        dismissCard();
                    }});
                }}
                plot.on("plotly_hover", (eventData) => {{
                    const payload = extractPayload(eventData?.points?.[0]);
                    if (payload) renderPayload(payload);
                }});
                plot.on("plotly_click", (eventData) => {{
                    const payload = extractPayload(eventData?.points?.[0]);
                    if (payload) {{
                        pinnedPayload = payload;
                        renderPayload(payload);
                    }}
                }});
                plot.on("plotly_unhover", () => {{
                    if (pinnedPayload) renderPayload(pinnedPayload);
                    else showPlaceholder();
                }});
                plot.on("plotly_doubleclick", () => {{
                    pinnedPayload = null;
                    window.setTimeout(showPlaceholder, 0);
                }});
                showPlaceholder();
            }}

            bindEvents();
        }})();
    </script>
    """

    components.html(html, height=height + 20, scrolling=False)


# ============================================================================
# TOPOJSON -> GEOJSON
# ============================================================================

def _decode_delta(arcs_encoded):
    result = []
    x, y = 0, 0
    for dx, dy in arcs_encoded:
        x += dx
        y += dy
        result.append([x, y])
    return result

def _transform_point(point, transform):
    scale = transform["scale"]
    translate = transform["translate"]
    return [
        point[0] * scale[0] + translate[0],
        point[1] * scale[1] + translate[1],
    ]

def _arc_to_coords(arc_index, arcs_raw, transform):
    if arc_index < 0:
        arc_index = ~arc_index
        pts = [_transform_point(p, transform) for p in _decode_delta(arcs_raw[arc_index])]
        pts.reverse()
    else:
        pts = [_transform_point(p, transform) for p in _decode_delta(arcs_raw[arc_index])]
    return pts

def _ring_coords(ring, arcs_raw, transform):
    coords = []
    for i, arc_idx in enumerate(ring):
        pts = _arc_to_coords(arc_idx, arcs_raw, transform)
        if i == 0:
            coords.extend(pts)
        else:
            coords.extend(pts[1:])
    return coords

def topojson_to_geojson(topo, object_name):
    transform = topo.get("transform", {"scale": [1, 1], "translate": [0, 0]})
    arcs_raw = topo["arcs"]
    obj = topo["objects"][object_name]
    features = []
    for geom in obj["geometries"]:
        props = geom.get("properties", {})
        gtype = geom["type"]
        if gtype == "Polygon":
            rings = [[_ring_coords(r, arcs_raw, transform)] for r in geom["arcs"]]
            geo = {"type": "Polygon", "coordinates": rings[0]}
        elif gtype == "MultiPolygon":
            polys = []
            for poly_arcs in geom["arcs"]:
                polys.append([_ring_coords(r, arcs_raw, transform) for r in poly_arcs])
            geo = {"type": "MultiPolygon", "coordinates": polys}
        else:
            continue
        features.append({
            "type": "Feature",
            "geometry": geo,
            "properties": props,
        })
    return {"type": "FeatureCollection", "features": features}


# ============================================================================
# HELPERS GEO
# ============================================================================

def extraer_puntos_geometria(geometry):
    gtype = geometry["type"]
    coords = geometry["coordinates"]
    puntos = []
    if gtype == "Polygon":
        for ring in coords:
            puntos.extend(ring)
    elif gtype == "MultiPolygon":
        for poly in coords:
            for ring in poly:
                puntos.extend(ring)
    return puntos

def centroid_simple(geometry):
    puntos = extraer_puntos_geometria(geometry)
    if not puntos:
        return 4.5709, -74.2973
    lons = [p[0] for p in puntos]
    lats = [p[1] for p in puntos]
    return sum(lats) / len(lats), sum(lons) / len(lons)

def construir_centroides_por_departamento(geojson_col):
    filas = []
    for feature in geojson_col["features"]:
        props = feature["properties"]
        codigo = props.get("codigo_departamento_n")
        nombre = props.get("departamento")
        lat, lon = centroid_simple(feature["geometry"])
        filas.append({
            "Codigo_DANE": pd.to_numeric(codigo, errors="coerce"),
            "Departamento_geo": str(nombre).upper().strip(),
            "Lat": lat,
            "Lon": lon,
        })
    df = pd.DataFrame(filas).dropna(subset=["Codigo_DANE"])
    df["Codigo_DANE"] = df["Codigo_DANE"].astype(int)
    return df

def construir_centroides_por_municipio(geojson_col):
    filas = []
    for feature in geojson_col["features"]:
        props = feature["properties"]
        codigo = props.get("codigo_municipio_n")
        lat, lon = centroid_simple(feature["geometry"])
        filas.append({
            "Codigo_Municipio": pd.to_numeric(codigo, errors="coerce"),
            "Lat_Ciudad": lat,
            "Lon_Ciudad": lon,
        })
    df = pd.DataFrame(filas).dropna(subset=["Codigo_Municipio"])
    df["Codigo_Municipio"] = df["Codigo_Municipio"].astype(int)
    return df


# ============================================================================
# CONSUMO API
# ============================================================================

def consultar_api(params):
    url = f"{BASE_API}?{urlencode(params)}"
    try:
        resp = requests.get(url, timeout=60)
        resp.raise_for_status()
        return resp.json()

    except requests.exceptions.HTTPError as e:
        st.warning(f"⚠️ Error HTTP en la API: {e}")
        return []

    except requests.exceptions.Timeout:
        st.warning("⏱️ La API tardó demasiado en responder.")
        return []

    except requests.exceptions.RequestException as e:
        st.warning(f"❌ Error de conexión con la API: {e}")
        return []

@st.cache_data(show_spinner=False, ttl=300)
def consultar_api_todas_paginas(params, page_size: int = 1000):
    resultados = []
    offset = 0

    while True:
        page_params = dict(params)
        page_params["$limit"] = page_size
        page_params["$offset"] = offset
        batch = consultar_api(page_params)

        if not batch:
            break

        resultados.extend(batch)
        if len(batch) < page_size:
            break

        offset += page_size

    return resultados

@st.cache_data(show_spinner=False)
def cargar_geojson():
    resp = requests.get(MAPA_URL, timeout=30)
    resp.raise_for_status()
    topo = resp.json()
    return topojson_to_geojson(topo, "MGN_DPTO_POLITICO_rJAC")

@st.cache_data(show_spinner=False)
def cargar_geojson_municipios():
    resp = requests.get(MAPA_MUNICIPIOS_URL, timeout=60)
    resp.raise_for_status()
    topo = resp.json()
    return topojson_to_geojson(topo, "MGN_MPIO_POLITICO_rJAC")

@st.cache_data(show_spinner=False, ttl=300)
def cargar_datos_departamentos_api():
    # 1) Casos por departamento
    params_depto = {
        "$select": "cod_depto, departamento, count(*) as casos",
        "$where": "cod_depto IS NOT NULL AND departamento IS NOT NULL",
        "$group": "cod_depto, departamento",
        "$order": "count(*) DESC",
    }
    data_depto = consultar_api_todas_paginas(params_depto)
    df_depto = pd.DataFrame(data_depto)
    if df_depto.empty:
        st.warning("⚠️ No se pudieron cargar datos de la API.")
        return pd.DataFrame(), pd.DataFrame()
    df_depto["Codigo_DANE"] = pd.to_numeric(df_depto["cod_depto"], errors="coerce")
    df_depto["Departamento"] = df_depto["departamento"].astype(str).str.upper().str.strip()
    df_depto["Casos"] = pd.to_numeric(df_depto["casos"], errors="coerce").fillna(0).astype(int)
    df_depto = df_depto[["Codigo_DANE", "Departamento", "Casos"]].dropna(subset=["Codigo_DANE"])
    df_depto["Codigo_DANE"] = df_depto["Codigo_DANE"].astype(int)

    # 2) Delito principal por departamento
    params_delito_depto = {
        "$select": "cod_depto, departamento, descripcion_conducta, count(*) as casos",
        "$where": "cod_depto IS NOT NULL AND departamento IS NOT NULL AND descripcion_conducta IS NOT NULL",
        "$group": "cod_depto, departamento, descripcion_conducta",
        "$order": "cod_depto ASC, count(*) DESC, descripcion_conducta ASC",
    }
    data_delito_depto = consultar_api_todas_paginas(params_delito_depto)
    df_delito_depto = pd.DataFrame(data_delito_depto)
    if df_delito_depto.empty:
        raise ValueError("La API no devolvió datos de delitos por departamento.")
    df_delito_depto["Codigo_DANE"] = pd.to_numeric(df_delito_depto["cod_depto"], errors="coerce")
    df_delito_depto["Departamento"] = df_delito_depto["departamento"].astype(str).str.upper().str.strip()
    df_delito_depto["Delito_Principal"] = df_delito_depto["descripcion_conducta"].astype(str).str.strip()
    df_delito_depto["Casos_Delito"] = pd.to_numeric(df_delito_depto["casos"], errors="coerce").fillna(0).astype(int)
    df_delito_depto = df_delito_depto.dropna(subset=["Codigo_DANE"])
    df_delito_depto["Codigo_DANE"] = df_delito_depto["Codigo_DANE"].astype(int)
    df_delito_depto = (
        df_delito_depto
        .sort_values(["Codigo_DANE", "Casos_Delito", "Delito_Principal"], ascending=[True, False, True])
        .drop_duplicates(subset=["Codigo_DANE"])
        [["Codigo_DANE", "Delito_Principal"]]
    )

    return df_depto, df_delito_depto


@st.cache_data(show_spinner=False, ttl=300)
def cargar_datos_municipios_api():
    # 3) Casos por municipio
    params_muni = {
        "$select": "cod_muni, municipio, cod_depto, departamento, count(*) as casos",
        "$where": "cod_muni IS NOT NULL AND municipio IS NOT NULL AND cod_depto IS NOT NULL AND departamento IS NOT NULL",
        "$group": "cod_muni, municipio, cod_depto, departamento",
        "$order": "count(*) DESC",
    }
    data_muni = consultar_api_todas_paginas(params_muni)
    df_muni = pd.DataFrame(data_muni)
    if df_muni.empty:
        raise ValueError("La API no devolvio datos por municipio.")
    df_muni["Codigo_Municipio"] = pd.to_numeric(df_muni["cod_muni"], errors="coerce")
    df_muni["Codigo_DANE"] = pd.to_numeric(df_muni["cod_depto"], errors="coerce")
    df_muni["Ciudad"] = df_muni["municipio"].astype(str).str.strip()
    df_muni["Departamento"] = df_muni["departamento"].astype(str).str.upper().str.strip()
    df_muni["Casos"] = pd.to_numeric(df_muni["casos"], errors="coerce").fillna(0).astype(int)
    df_muni = df_muni[["Codigo_Municipio", "Codigo_DANE", "Ciudad", "Departamento", "Casos"]].dropna(
        subset=["Codigo_Municipio", "Codigo_DANE"]
    )
    df_muni["Codigo_Municipio"] = df_muni["Codigo_Municipio"].astype(int)
    df_muni["Codigo_DANE"] = df_muni["Codigo_DANE"].astype(int)

    # 4) Delito principal por municipio
    params_delito_muni = {
        "$select": "cod_muni, municipio, descripcion_conducta, count(*) as casos",
        "$where": "cod_muni IS NOT NULL AND municipio IS NOT NULL AND descripcion_conducta IS NOT NULL",
        "$group": "cod_muni, municipio, descripcion_conducta",
        "$order": "cod_muni ASC, count(*) DESC, descripcion_conducta ASC",
    }
    data_delito_muni = consultar_api_todas_paginas(params_delito_muni)
    df_delito_muni = pd.DataFrame(data_delito_muni)
    if df_delito_muni.empty:
        raise ValueError("La API no devolvio datos de delitos por municipio.")
    df_delito_muni["Codigo_Municipio"] = pd.to_numeric(df_delito_muni["cod_muni"], errors="coerce")
    df_delito_muni["Delito_Principal_Ciudad"] = df_delito_muni["descripcion_conducta"].astype(str).str.strip()
    df_delito_muni["Casos_Delito"] = pd.to_numeric(df_delito_muni["casos"], errors="coerce").fillna(0).astype(int)
    df_delito_muni = df_delito_muni.dropna(subset=["Codigo_Municipio"])
    df_delito_muni["Codigo_Municipio"] = df_delito_muni["Codigo_Municipio"].astype(int)
    df_delito_muni = (
        df_delito_muni
        .sort_values(["Codigo_Municipio", "Casos_Delito", "Delito_Principal_Ciudad"], ascending=[True, False, True])
        .drop_duplicates(subset=["Codigo_Municipio"])
        [["Codigo_Municipio", "Delito_Principal_Ciudad"]]
    )

    return df_muni, df_delito_muni


@st.cache_data(show_spinner=False, ttl=300)
def cargar_datos_historicos_api():
    # 5) Serie histórica nacional por año
    params_hist = {
        "$select": "date_extract_y(fecha_hecho) as anio, count(*) as casos",
        "$where": "fecha_hecho IS NOT NULL",
        "$group": "date_extract_y(fecha_hecho)",
        "$order": "date_extract_y(fecha_hecho) ASC",
    }
    data_hist = consultar_api_todas_paginas(params_hist)
    df_hist = pd.DataFrame(data_hist)
    if df_hist.empty:
        raise ValueError("La API no devolvió serie histórica.")
    df_hist["Año"] = pd.to_numeric(df_hist["anio"], errors="coerce")
    df_hist["Casos"] = pd.to_numeric(df_hist["casos"], errors="coerce").fillna(0).astype(int)
    df_hist = df_hist[["Año", "Casos"]].dropna().sort_values("Año")
    df_hist["Año"] = df_hist["Año"].astype(int)

    # 6) Ciudad top por año
    params_ciudad = {
        "$select": "date_extract_y(fecha_hecho) as anio, municipio, count(*) as casos",
        "$where": "fecha_hecho IS NOT NULL AND municipio IS NOT NULL",
        "$group": "date_extract_y(fecha_hecho), municipio",
        "$order": "date_extract_y(fecha_hecho) ASC, count(*) DESC, municipio ASC",
    }
    data_ciudad = consultar_api_todas_paginas(params_ciudad)
    df_ciudad = pd.DataFrame(data_ciudad)
    if not df_ciudad.empty:
        df_ciudad["Año"] = pd.to_numeric(df_ciudad["anio"], errors="coerce")
        df_ciudad["Ciudad_Top"] = df_ciudad["municipio"].astype(str).str.strip()
        df_ciudad["Casos_Ciudad"] = pd.to_numeric(df_ciudad["casos"], errors="coerce").fillna(0).astype(int)
        df_ciudad = (
            df_ciudad
            .dropna(subset=["Año"])
            .sort_values(["Año", "Casos_Ciudad", "Ciudad_Top"], ascending=[True, False, True])
            .drop_duplicates(subset=["Año"])
            [["Año", "Ciudad_Top"]]
        )
        df_ciudad["Año"] = df_ciudad["Año"].astype(int)
    else:
        df_ciudad = pd.DataFrame(columns=["Año", "Ciudad_Top"])

    # 7) Delito top por año
    params_delito_anio = {
        "$select": "date_extract_y(fecha_hecho) as anio, descripcion_conducta, count(*) as casos",
        "$where": "fecha_hecho IS NOT NULL AND descripcion_conducta IS NOT NULL",
        "$group": "date_extract_y(fecha_hecho), descripcion_conducta",
        "$order": "date_extract_y(fecha_hecho) ASC, count(*) DESC, descripcion_conducta ASC",
    }
    data_delito_anio = consultar_api_todas_paginas(params_delito_anio)
    df_delito_anio = pd.DataFrame(data_delito_anio)
    if not df_delito_anio.empty:
        df_delito_anio["Año"] = pd.to_numeric(df_delito_anio["anio"], errors="coerce")
        df_delito_anio["Delito_Top"] = df_delito_anio["descripcion_conducta"].astype(str).str.strip()
        df_delito_anio["Casos_Delito"] = pd.to_numeric(df_delito_anio["casos"], errors="coerce").fillna(0).astype(int)
        df_delito_anio = (
            df_delito_anio
            .dropna(subset=["Año"])
            .sort_values(["Año", "Casos_Delito", "Delito_Top"], ascending=[True, False, True])
            .drop_duplicates(subset=["Año"])
            [["Año", "Delito_Top"]]
        )
        df_delito_anio["Año"] = df_delito_anio["Año"].astype(int)
    else:
        df_delito_anio = pd.DataFrame(columns=["Año", "Delito_Top"])

    return df_hist, df_ciudad, df_delito_anio


@st.cache_data(show_spinner=False, ttl=300)
def cargar_datos_api():
    df_depto, df_delito_depto = cargar_datos_departamentos_api()
    df_muni, df_delito_muni = cargar_datos_municipios_api()
    df_hist, df_ciudad, df_delito_anio = cargar_datos_historicos_api()
    return df_depto, df_delito_depto, df_muni, df_delito_muni, df_hist, df_ciudad, df_delito_anio


@st.cache_data(show_spinner=False, ttl=300)
def cargar_metrica_total_casos_nacional():
    params = {
        "$select": "count(*) as casos",
    }
    data = consultar_api(params)
    df = pd.DataFrame(data)
    if df.empty:
        raise ValueError("La API no devolvió el total nacional de casos.")

    return {"casos": int(pd.to_numeric(df.iloc[0]["casos"], errors="coerce") or 0)}


@st.cache_data(show_spinner=False, ttl=300)
def cargar_metrica_delito_comun_top():
    params = {
        "$select": "descripcion_conducta, count(*) as casos",
        "$where": "descripcion_conducta IS NOT NULL",
        "$group": "descripcion_conducta",
        "$order": "count(*) DESC, descripcion_conducta ASC",
        "$limit": 1,
    }
    data = consultar_api(params)
    df = pd.DataFrame(data)
    if df.empty:
        raise ValueError("La API no devolvió el delito más frecuente.")

    delito = str(df.iloc[0]["descripcion_conducta"]).strip() or "Sin dato"
    casos = int(pd.to_numeric(df.iloc[0]["casos"], errors="coerce") or 0)
    return {"delito": delito, "casos": casos}


@st.cache_data(show_spinner=False, ttl=300)
def cargar_metrica_delito_comun_participacion():
    params_top = {
        "$select": "descripcion_conducta, count(*) as casos",
        "$where": "descripcion_conducta IS NOT NULL",
        "$group": "descripcion_conducta",
        "$order": "count(*) DESC, descripcion_conducta ASC",
        "$limit": 1,
    }
    params_total = {
        "$select": "count(*) as casos",
    }
    data_top = consultar_api(params_top)
    data_total = consultar_api(params_total)
    df_top = pd.DataFrame(data_top)
    df_total = pd.DataFrame(data_total)
    if df_top.empty or df_total.empty:
        raise ValueError("La API no devolvió la participación del delito líder.")

    casos_top = int(pd.to_numeric(df_top.iloc[0]["casos"], errors="coerce") or 0)
    casos_total = int(pd.to_numeric(df_total.iloc[0]["casos"], errors="coerce") or 0)
    pct = (casos_top / casos_total * 100) if casos_total else 0
    return {"pct": pct}


@st.cache_data(show_spinner=False, ttl=300)
def cargar_metrica_delito_comun_tipos():
    params = {
        "$select": "count(distinct descripcion_conducta) as total",
        "$where": "descripcion_conducta IS NOT NULL",
    }
    data = consultar_api(params)
    df = pd.DataFrame(data)
    if df.empty:
        raise ValueError("La API no devolvió el total de tipos de delito.")

    total = int(pd.to_numeric(df.iloc[0]["total"], errors="coerce") or 0)
    return {"total": total}


def adaptar_ranking_delitos(df_raw: pd.DataFrame) -> pd.DataFrame:
    if df_raw.empty:
        return pd.DataFrame(columns=["Delito_Principal", "Casos"])

    df = df_raw.copy()
    df["Delito_Principal"] = df["descripcion_conducta"].astype(str).str.strip()
    df["Casos"] = pd.to_numeric(df["casos"], errors="coerce").fillna(0).astype(int)
    return (
        df.loc[df["Delito_Principal"].ne(""), ["Delito_Principal", "Casos"]]
        .sort_values(["Casos", "Delito_Principal"], ascending=[False, True])
        .reset_index(drop=True)
    )


@st.cache_data(show_spinner=False, ttl=300)
def cargar_chart_delito_comun_rank():
    params = {
        "$select": "descripcion_conducta, count(*) as casos",
        "$where": "descripcion_conducta IS NOT NULL",
        "$group": "descripcion_conducta",
        "$order": "count(*) DESC, descripcion_conducta ASC",
    }
    data = consultar_api_todas_paginas(params)
    return adaptar_ranking_delitos(pd.DataFrame(data))


def construir_df_colombia_base(df_depto: pd.DataFrame, df_delito_depto: pd.DataFrame) -> pd.DataFrame:
    df_colombia = df_depto.merge(df_delito_depto, on="Codigo_DANE", how="left")
    df_colombia["Delito_Principal"] = df_colombia["Delito_Principal"].fillna("Sin dato")
    return df_colombia


def construir_df_ciudades_base(df_muni: pd.DataFrame, df_delito_muni: pd.DataFrame) -> pd.DataFrame:
    df_ciudades = df_muni.merge(df_delito_muni, on="Codigo_Municipio", how="left")
    df_ciudades["Delito_Principal_Ciudad"] = df_ciudades["Delito_Principal_Ciudad"].fillna("Sin dato")
    return df_ciudades


def construir_contexto_historico(
    df_hist: pd.DataFrame,
    df_ciudad: pd.DataFrame,
    df_delito_anio: pd.DataFrame,
):
    df_hist = (
        df_hist
        .merge(df_ciudad, on="Año", how="left")
        .merge(df_delito_anio, on="Año", how="left")
    )
    df_hist["Ciudad_Top"] = df_hist["Ciudad_Top"].fillna("Sin dato")
    df_hist["Delito_Top"] = df_hist["Delito_Top"].fillna("Sin dato")
    df_hist_linea = (
        df_hist[
            df_hist["Año"].between(HISTORICAL_YEAR_START, HISTORICAL_YEAR_END)
        ][["Año", "Casos", "Ciudad_Top", "Delito_Top"]]
        .set_index("Año")
        .reindex(range(HISTORICAL_YEAR_START, HISTORICAL_YEAR_END + 1))
        .rename_axis("Año")
        .reset_index()
    )
    df_hist_linea["Casos"] = df_hist_linea["Casos"].fillna(0).astype(int)
    df_hist_linea["Ciudad_Top"] = df_hist_linea["Ciudad_Top"].fillna("Sin dato")
    df_hist_linea["Delito_Top"] = df_hist_linea["Delito_Top"].fillna("Sin dato")
    return df_hist, df_hist_linea


def construir_contexto_principal_desde_base(
    df_colombia_base: pd.DataFrame,
    df_ciudades_base: pd.DataFrame,
    geojson_col,
    geojson_municipios,
):
    df_centroides = construir_centroides_por_departamento(geojson_col)
    df_centroides_municipios = construir_centroides_por_municipio(geojson_municipios)

    df_colombia = (
        df_colombia_base
        .merge(df_centroides[["Codigo_DANE", "Lat", "Lon"]], on="Codigo_DANE", how="left")
    )
    df_colombia["Lat"] = df_colombia["Lat"].fillna(4.5709)
    df_colombia["Lon"] = df_colombia["Lon"].fillna(-74.2973)

    df_ciudades_mapa = (
        df_ciudades_base
        .merge(df_centroides_municipios, on="Codigo_Municipio", how="left")
        .merge(
            df_centroides[["Codigo_DANE", "Lat", "Lon"]].rename(columns={"Lat": "Lat_Depto", "Lon": "Lon_Depto"}),
            on="Codigo_DANE",
            how="left",
        )
    )
    df_ciudades_mapa["Lat_Ciudad"] = df_ciudades_mapa["Lat_Ciudad"].fillna(df_ciudades_mapa["Lat_Depto"]).fillna(4.5709)
    df_ciudades_mapa["Lon_Ciudad"] = df_ciudades_mapa["Lon_Ciudad"].fillna(df_ciudades_mapa["Lon_Depto"]).fillna(-74.2973)
    df_ciudades_mapa = df_ciudades_mapa.drop(columns=["Lat_Depto", "Lon_Depto"])

    df_opciones_ciudad = (
        df_ciudades_mapa[["Ciudad", "Departamento"]]
        .dropna()
        .drop_duplicates()
        .sort_values(["Ciudad", "Departamento"])
        .copy()
    )
    df_opciones_ciudad["Etiqueta_Ciudad"] = (
        df_opciones_ciudad["Ciudad"] + " - " + df_opciones_ciudad["Departamento"]
    )

    return {
        "df_colombia": df_colombia,
        "df_ciudades_mapa": df_ciudades_mapa,
        "lista_deptos": ["TOTAL NACIONAL"] + sorted(df_colombia["Departamento"].dropna().unique().tolist()),
        "lista_ciudades": ["TODAS LAS CIUDADES"] + df_opciones_ciudad["Etiqueta_Ciudad"].tolist(),
    }


@st.cache_data(show_spinner=False, ttl=300)
def cargar_contexto_metricas_globales():
    return {
        "total_nacional": cargar_metrica_total_casos_nacional()["casos"],
        "metrica_delito_top_global": cargar_metrica_delito_comun_top(),
    }


@st.cache_data(show_spinner=False, ttl=300)
def cargar_contexto_total_casos():
    df_depto, df_delito_depto = cargar_datos_departamentos_api()
    df_muni, df_delito_muni = cargar_datos_municipios_api()
    df_hist_raw, df_ciudad, df_delito_anio = cargar_datos_historicos_api()

    df_colombia = construir_df_colombia_base(df_depto, df_delito_depto)
    df_ciudades_mapa = construir_df_ciudades_base(df_muni, df_delito_muni)
    df_hist, _ = construir_contexto_historico(df_hist_raw, df_ciudad, df_delito_anio)

    depto_top = df_colombia.loc[df_colombia["Casos"].idxmax()].to_dict() if not df_colombia.empty else {}
    anio_top = df_hist.loc[df_hist["Casos"].idxmax()].to_dict() if not df_hist.empty else None

    return {
        "df_colombia": df_colombia,
        "df_ciudades_mapa": df_ciudades_mapa,
        "df_hist": df_hist,
        "depto_top": depto_top,
        "anio_top": anio_top,
    }


@st.cache_data(show_spinner=False, ttl=300)
def cargar_contexto_depto_top():
    df_depto, df_delito_depto = cargar_datos_departamentos_api()
    df_muni, df_delito_muni = cargar_datos_municipios_api()

    df_colombia = construir_df_colombia_base(df_depto, df_delito_depto)
    df_ciudades_mapa = construir_df_ciudades_base(df_muni, df_delito_muni)
    depto_top = df_colombia.loc[df_colombia["Casos"].idxmax()].to_dict() if not df_colombia.empty else {}

    return {
        "df_ciudades_mapa": df_ciudades_mapa,
        "depto_top": depto_top,
    }


@st.cache_data(show_spinner=False, ttl=300)
def cargar_contexto_anio_pico():
    df_hist_raw, df_ciudad, df_delito_anio = cargar_datos_historicos_api()
    df_hist, df_hist_linea = construir_contexto_historico(df_hist_raw, df_ciudad, df_delito_anio)
    anio_top = df_hist.loc[df_hist["Casos"].idxmax()].to_dict() if not df_hist.empty else None

    return {
        "df_hist": df_hist,
        "df_hist_linea": df_hist_linea,
        "anio_top": anio_top,
    }


@st.cache_data(show_spinner=False, ttl=300)
def cargar_contexto_dashboard_principal():
    df_depto, df_delito_depto = cargar_datos_departamentos_api()
    df_muni, df_delito_muni = cargar_datos_municipios_api()
    df_hist_raw, df_ciudad, df_delito_anio = cargar_datos_historicos_api()

    df_colombia_base = construir_df_colombia_base(df_depto, df_delito_depto)
    df_ciudades_base = construir_df_ciudades_base(df_muni, df_delito_muni)
    df_hist, df_hist_linea = construir_contexto_historico(df_hist_raw, df_ciudad, df_delito_anio)

    geojson_col = cargar_geojson()
    geojson_municipios = cargar_geojson_municipios()
    geo_context = construir_contexto_principal_desde_base(
        df_colombia_base=df_colombia_base,
        df_ciudades_base=df_ciudades_base,
        geojson_col=geojson_col,
        geojson_municipios=geojson_municipios,
    )

    return {
        "geojson_col": geojson_col,
        "geojson_municipios": geojson_municipios,
        "df_colombia": geo_context["df_colombia"],
        "df_ciudades_mapa": geo_context["df_ciudades_mapa"],
        "df_hist": df_hist,
        "df_hist_linea": df_hist_linea,
        "lista_deptos": geo_context["lista_deptos"],
        "lista_ciudades": geo_context["lista_ciudades"],
        "depto_top": df_colombia_base.loc[df_colombia_base["Casos"].idxmax()].to_dict() if not df_colombia_base.empty else {},
        "anio_top": df_hist.loc[df_hist["Casos"].idxmax()].to_dict() if not df_hist.empty else None,
    }


# ============================================================================
# CARGA DATOS
# ============================================================================

geojson_col = None
geojson_municipios = None
df_colombia = pd.DataFrame()
df_ciudades_mapa = pd.DataFrame()
df_hist = pd.DataFrame()
df_hist_linea = pd.DataFrame()
lista_deptos = ["TOTAL NACIONAL"]
lista_ciudades = ["TODAS LAS CIUDADES"]
total_nacional = 0
metrica_delito_top_global = {"delito": "—", "casos": 0}
depto_top = {}
delito_top_global = "—"
casos_delito_top_global = 0
anio_top = None

if st.session_state.active_view in {None, "total_casos", "depto_top", "delito_top"}:
    try:
        metricas_contexto = cargar_contexto_metricas_globales()
        total_nacional = int(metricas_contexto["total_nacional"])
        metrica_delito_top_global = metricas_contexto["metrica_delito_top_global"]
    except Exception:
        metricas_contexto = {"total_nacional": 0, "metrica_delito_top_global": {"delito": "—", "casos": 0}}

try:
    if st.session_state.active_view is None:
        dashboard_contexto = ejecutar_con_texto_temporal(
            "Cargando dashboard...",
            cargar_contexto_dashboard_principal,
        )
        geojson_col = dashboard_contexto["geojson_col"]
        geojson_municipios = dashboard_contexto["geojson_municipios"]
        df_colombia = dashboard_contexto["df_colombia"]
        df_ciudades_mapa = dashboard_contexto["df_ciudades_mapa"]
        df_hist = dashboard_contexto["df_hist"]
        df_hist_linea = dashboard_contexto["df_hist_linea"]
        lista_deptos = dashboard_contexto["lista_deptos"]
        lista_ciudades = dashboard_contexto["lista_ciudades"]
        depto_top = dashboard_contexto["depto_top"]
        anio_top = dashboard_contexto["anio_top"]
    elif st.session_state.active_view == "total_casos":
        total_contexto = ejecutar_con_texto_temporal(
            API_LOADING_TEXT,
            cargar_contexto_total_casos,
        )
        df_colombia = total_contexto["df_colombia"]
        df_ciudades_mapa = total_contexto["df_ciudades_mapa"]
        df_hist = total_contexto["df_hist"]
        depto_top = total_contexto["depto_top"]
        anio_top = total_contexto["anio_top"]
        if not total_nacional:
            total_nacional = int(df_colombia["Casos"].sum())
    elif st.session_state.active_view == "depto_top":
        depto_contexto = ejecutar_con_texto_temporal(
            API_LOADING_TEXT,
            cargar_contexto_depto_top,
        )
        df_ciudades_mapa = depto_contexto["df_ciudades_mapa"]
        depto_top = depto_contexto["depto_top"]
    elif st.session_state.active_view == "anio_pico":
        historial_contexto = ejecutar_con_texto_temporal(
            API_LOADING_TEXT,
            cargar_contexto_anio_pico,
        )
        df_hist = historial_contexto["df_hist"]
        df_hist_linea = historial_contexto["df_hist_linea"]
        anio_top = historial_contexto["anio_top"]
except Exception as e:
    if str(e) == API_DEPTO_EMPTY_TEXT:
        st.markdown(render_target_text(API_DEPTO_EMPTY_TEXT), unsafe_allow_html=True)
    else:
        st.error(f"No se pudieron cargar los datos desde la API: {e}")
    st.stop()

if not total_nacional and not df_colombia.empty:
    total_nacional = int(df_colombia["Casos"].sum())

delito_top_global = str(metrica_delito_top_global["delito"]).strip() or "—"
casos_delito_top_global = int(metrica_delito_top_global["casos"])

# ============================================================================
# VISTA DE DETALLE – renderiza el panel expandido para un KPI
# ============================================================================

def render_detail_view(view_key: str):
    """
    Renderiza la vista de detalle correspondiente a `view_key`.
    La navegación funciona 100% via st.session_state: no se recarga la página
    completa, Streamlit sólo re-ejecuta el script y este bloque es el que se
    muestra en lugar del dashboard principal.
    """


    # ── Despacha a la función correcta ───────────────────────────────────
    try:
        if view_key == "total_casos":
            _detail_total_casos()
        elif view_key == "depto_top":
            _detail_depto_top()
        elif view_key == "delito_top":
            _detail_delito_top()
        elif view_key == "anio_pico":
            _detail_anio_pico()
        else:
            st.warning("Vista no reconocida.")
    except Exception as exc:
        st.error(f"No se pudo abrir la sub-vista seleccionada: {exc}")

    # ── Botón Volver al final de la página ───────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Volver al Dashboard", key="btn_back_bottom"):
        navigate_home()
        st.rerun()


def _detail_title(key: str) -> str:
    return {
        "total_casos": "Total de Denuncias",
        "depto_top":   "Departamento Más Afectado",
        "delito_top":  "Delito Más Común",
        "anio_pico":   "Año Pico",
    }.get(key, "Detalle")


# ── Sub-vistas individuales ───────────────────────────────────────────────────

def _render_detail_chart(fig: go.Figure, margin=None):
    """Renderiza charts de sub-vistas con comportamiento responsive consistente."""
    fig.update_layout(
        autosize=True,
        margin=margin or dict(t=16, b=48, l=16, r=16),
    )
    fig.update_xaxes(automargin=True)
    fig.update_yaxes(automargin=True)
    st.markdown('<div class="detail-chart-anchor"></div>', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config={"responsive": True})


def _detail_stat_card_html(label: str, value: str, note: str) -> str:
    return f"""
    <div class="detail-stat-card">
        <div class="dsc-label">{label}</div>
        <div class="dsc-value">{value}</div>
        <div class="dsc-note">{note}</div>
    </div>
    """


def _render_delito_comun_stat_card(column, label: str, loader, value_formatter, note_formatter):
    with column:
        placeholder = st.empty()
        placeholder.markdown(
            _detail_stat_card_html(label, "Cargando...", "Consultando API..."),
            unsafe_allow_html=True,
        )
        try:
            data = loader()
            placeholder.markdown(
                _detail_stat_card_html(label, value_formatter(data), note_formatter(data)),
                unsafe_allow_html=True,
            )
        except Exception as exc:
            placeholder.markdown(
                _detail_stat_card_html(label, "Error", f"No se pudo cargar: {exc}"),
                unsafe_allow_html=True,
            )


def _detail_total_casos():
    """Vista de detalle: Total de casos nacionales."""

    st.markdown(
        f"""
        <div class="detail-hero">
            <div class="dh-eyebrow">📊 Indicador · Total acumulado nacional</div>
            <div class="dh-title">Total de Denuncias por Cibercrimen</div>
            <div class="dh-value">{total_nacional:,}</div>
            <div class="dh-sub">Registros acumulados en la base de datos de la Policía Nacional</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Stats secundarios
    num_deptos = df_colombia["Departamento"].nunique()
    num_ciudades = df_ciudades_mapa["Ciudad"].nunique()
    promedio_depto = int(total_nacional / num_deptos) if num_deptos else 0
    años_con_datos = df_hist[df_hist["Casos"] > 0]["Año"].nunique()

    st.markdown(
        f"""
        <div class="detail-stats-grid">
            <div class="detail-stat-card">
                <div class="dsc-label">Departamentos registrados</div>
                <div class="dsc-value">{num_deptos}</div>
                <div class="dsc-note">Con al menos 1 denuncia</div>
            </div>
            <div class="detail-stat-card">
                <div class="dsc-label">Municipios / Ciudades</div>
                <div class="dsc-value">{num_ciudades:,}</div>
                <div class="dsc-note">Con presencia en el dataset</div>
            </div>
            <div class="detail-stat-card">
                <div class="dsc-label">Promedio por departamento</div>
                <div class="dsc-value">{promedio_depto:,}</div>
                <div class="dsc-note">Casos / dpto. (media simple)</div>
            </div>
            <div class="detail-stat-card">
                <div class="dsc-label">Años con datos</div>
                <div class="dsc-value">{años_con_datos}</div>
                <div class="dsc-note">Serie histórica disponible</div>
            </div>
            <div class="detail-stat-card">
                <div class="dsc-label">Depto. más afectado</div>
                <div class="dsc-value">{str(depto_top['Departamento']).title()}</div>
                <div class="dsc-note">{int(depto_top['Casos']):,} casos</div>
            </div>
            <div class="detail-stat-card">
                <div class="dsc-label">Año pico</div>
                <div class="dsc-value">{int(anio_top['Año']) if anio_top is not None else '—'}</div>
                <div class="dsc-note">{int(anio_top['Casos']):,} denuncias ese año</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Insight contextual
    pct_top5 = df_colombia.nlargest(5, "Casos")["Casos"].sum() / total_nacional * 100 if total_nacional else 0
    st.markdown(
        f"""
        <div class="detail-insight">
            <div class="di-icon">🔍</div>
            <div class="di-body">
                <strong>Concentración geográfica</strong>
                <p>Los 5 departamentos con mayor incidencia acumulan el <b>{pct_top5:.1f}%</b>
                del total nacional de denuncias. Esta concentración sugiere que las campañas de
                prevención y respuesta deberían priorizar estas jurisdicciones para mayor impacto.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Gráfico: top 10 departamentos
    st.markdown(
        '<div class="section-title"><div class="icon purple">📊</div><h3>Top 10 Departamentos con Mayor Incidencia</h3></div>',
        unsafe_allow_html=True,
    )
    df_top10 = df_colombia.nlargest(10, "Casos").sort_values("Casos", ascending=True)
    fig = px.bar(
        df_top10, y="Departamento", x="Casos", orientation="h",
        text="Casos", color="Casos",
        color_continuous_scale=[[0, "#a8dce7"], [0.5, "#00b4d8"], [1, "#1e3a5f"]],
    )
    fig.update_traces(
        texttemplate="%{text:,}", textposition="outside",
        textfont=dict(size=12, color="#FFFFFF"),
        marker_line_width=0,
        hovertemplate="<b>%{y}</b><br>Casos: %{x:,}<extra></extra>",
    )
    fig.update_layout(**{
        **PLOTLY_LAYOUT,
        "font": dict(family="Inter, sans-serif", color="#FFFFFF"),
        "yaxis": dict(title="", tickfont=dict(size=11, color="#FFFFFF")),
        "xaxis": dict(title="", showgrid=True, gridcolor="rgba(30,58,95,0.08)",
                      zeroline=False, tickfont=dict(size=11, color="#FFFFFF")),
        "showlegend": False, "coloraxis_showscale": False, "height": 420,
    })
    _render_detail_chart(fig)

    # Gráfico: distribución porcentual top 10 vs resto
    st.markdown(
        '<div class="section-title"><div class="icon cyan">🥧</div><h3>Distribución: Top 10 vs. Resto del País</h3></div>',
        unsafe_allow_html=True,
    )
    casos_top10 = int(df_top10["Casos"].sum())
    casos_resto = total_nacional - casos_top10
    fig_pie = px.pie(
        values=[casos_top10, casos_resto],
        names=["Top 10 Departamentos", "Resto del País"],
        color_discrete_sequence=["#1e3a5f", "#00b4d8"],
        hole=0.55,
    )
    fig_pie.update_traces(
        textinfo="percent+label",
        textfont=dict(size=13, color="#FFFFFF"),
        hovertemplate="<b>%{label}</b><br>Casos: %{value:,}<br>(%{percent})<extra></extra>",
    )
    fig_pie.update_layout(**{
        **PLOTLY_LAYOUT,
        "height": 360,
        "showlegend": True,
        "legend": dict(
            orientation="h",
            yanchor="top",
            y=-0.12,
            xanchor="center",
            x=0.5,
            font=dict(size=11, color="#FFFFFF"),
        ),
    })
    _render_detail_chart(fig_pie, margin=dict(t=16, b=84, l=16, r=16))


def _detail_depto_top():
    """Vista de detalle: Departamento más afectado."""

    nombre_depto = str(depto_top["Departamento"]).title()
    casos_depto = int(depto_top["Casos"])
    delito_depto = truncateArticle(str(depto_top.get("Delito_Principal", "Sin dato")))
    pct_depto = casos_depto / total_nacional * 100 if total_nacional else 0

    st.markdown(
        f"""
        <div class="detail-hero cyan">
            <div class="dh-eyebrow">🏙️ Indicador · Departamento más afectado</div>
            <div class="dh-title">{nombre_depto}</div>
            <div class="dh-value">{casos_depto:,}</div>
            <div class="dh-sub">{pct_depto:.1f}% del total nacional de denuncias</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Municipios de ese departamento
    df_muni_depto = df_ciudades_mapa[
        df_ciudades_mapa["Departamento"] == depto_top["Departamento"]
    ].copy()
    num_muni = df_muni_depto["Ciudad"].nunique()
    ciudad_top_depto = (
        df_muni_depto.loc[df_muni_depto["Casos"].idxmax(), "Ciudad"]
        if not df_muni_depto.empty else "Sin dato"
    )
    casos_ciudad_top = (
        int(df_muni_depto["Casos"].max()) if not df_muni_depto.empty else 0
    )

    st.markdown(
        f"""
        <div class="detail-stats-grid">
            <div class="detail-stat-card">
                <div class="dsc-label">Total denuncias</div>
                <div class="dsc-value">{casos_depto:,}</div>
                <div class="dsc-note">Acumulado del departamento</div>
            </div>
            <div class="detail-stat-card">
                <div class="dsc-label">Participación nacional</div>
                <div class="dsc-value">{pct_depto:.1f}%</div>
                <div class="dsc-note">Del total de Colombia</div>
            </div>
            <div class="detail-stat-card">
                <div class="dsc-label">Municipios registrados</div>
                <div class="dsc-value">{num_muni}</div>
                <div class="dsc-note">Con al menos 1 denuncia</div>
            </div>
            <div class="detail-stat-card">
                <div class="dsc-label">Ciudad más afectada</div>
                <div class="dsc-value">{str(ciudad_top_depto).title()}</div>
                <div class="dsc-note">{casos_ciudad_top:,} casos</div>
            </div>
            <div class="detail-stat-card">
                <div class="dsc-label">Delito principal</div>
                <div class="dsc-value" style="font-size:1rem; line-height:1.3;">{delito_depto}</div>
                <div class="dsc-note">Conducta más denunciada</div>
            </div>
            <div class="detail-stat-card">
                <div class="dsc-label">Ranking nacional</div>
                <div class="dsc-value">#1</div>
                <div class="dsc-note">Por volumen de denuncias</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="detail-insight">
            <div class="di-icon">⚠️</div>
            <div class="di-body">
                <strong>Concentración interna</strong>
                <p><b>{nombre_depto}</b> concentra el <b>{pct_depto:.1f}%</b> de todas las denuncias del país.
                Su ciudad más reportada, <b>{str(ciudad_top_depto).title()}</b>, acumula
                <b>{casos_ciudad_top:,}</b> casos individuales, lo que apunta a una dinámica urbana
                que demanda atención prioritaria.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not df_muni_depto.empty:
        st.markdown(
            '<div class="section-title"><div class="icon cyan">📊</div>'
            f'<h3>Top 10 Municipios – {nombre_depto}</h3></div>',
            unsafe_allow_html=True,
        )
        df_top_muni = df_muni_depto.nlargest(10, "Casos").sort_values("Casos", ascending=True)
        fig = px.bar(
            df_top_muni, y="Ciudad", x="Casos", orientation="h",
            text="Casos", color="Casos",
            color_continuous_scale=[[0, "#a8dce7"], [0.5, "#00b4d8"], [1, "#1e3a5f"]],
        )
        fig.update_traces(
            texttemplate="%{text:,}", textposition="outside",
            textfont=dict(size=12, color="#FFFFFF"), marker_line_width=0,
            hovertemplate="<b>%{y}</b><br>Casos: %{x:,}<extra></extra>",
        )
        fig.update_layout(**{
            **PLOTLY_LAYOUT,
            "font": dict(family="Inter, sans-serif", color="#FFFFFF"),
            "yaxis": dict(title="", tickfont=dict(size=11, color="#FFFFFF")),
            "xaxis": dict(title="", showgrid=True, gridcolor="rgba(30,58,95,0.08)",
                          zeroline=False, tickfont=dict(size=11, color="#FFFFFF")),
            "showlegend": False, "coloraxis_showscale": False, "height": 400,
        })
        _render_detail_chart(fig)


def _detail_delito_top():
    """Vista de detalle: Delito más común a nivel nacional."""

    try:
        hero_data = cargar_metrica_delito_comun_top()
        hero_pct = cargar_metrica_delito_comun_participacion()
        delito_nombre = str(hero_data["delito"]).title()
        delito_titulo = truncateArticle(str(hero_data["delito"]))
        casos_delito = int(hero_data["casos"])
        pct_delito = float(hero_pct["pct"])
    except Exception:
        delito_nombre = str(delito_top_global).title()
        delito_titulo = truncateArticle(str(delito_top_global))
        casos_delito = int(casos_delito_top_global)
        pct_delito = casos_delito / total_nacional * 100 if total_nacional else 0

    st.markdown(
        f"""
        <div class="detail-hero violet">
            <div class="dh-eyebrow">⚠️ Indicador · Delito más frecuente a nivel nacional</div>
            <div class="dh-title">{delito_titulo}</div>
            <div class="dh-value">{casos_delito:,}</div>
            <div class="dh-sub">{pct_delito:.1f}% del total de denuncias nacionales</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    stat_cols = st.columns(3)
    _render_delito_comun_stat_card(
        stat_cols[0],
        "Casos del delito #1",
        cargar_metrica_delito_comun_top,
        lambda data: f"{int(data['casos']):,}",
        lambda _data: "Denuncias acumuladas",
    )
    _render_delito_comun_stat_card(
        stat_cols[1],
        "Participación en total",
        cargar_metrica_delito_comun_participacion,
        lambda data: f"{float(data['pct']):.1f}%",
        lambda _data: "Del total nacional",
    )
    _render_delito_comun_stat_card(
        stat_cols[2],
        "Tipos de delito distintos",
        cargar_metrica_delito_comun_tipos,
        lambda data: f"{int(data['total'])}",
        lambda _data: "Conductas registradas",
    )

    st.markdown(
        f"""
        <div class="detail-insight">
            <div class="di-icon">🎯</div>
            <div class="di-body">
                <strong>Análisis de la conducta líder</strong>
                <p>El delito <b>"{delito_titulo}"</b> representa el <b>{pct_delito:.1f}%</b> de todos los
                casos registrados en el país. Entender sus patrones de ocurrencia por región y año
                es clave para diseñar estrategias de prevención focalizadas.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Gráfico: ranking de todos los delitos
    st.markdown(
        '<div class="section-title"><div class="icon violet">📊</div>'
        '<h3>Ranking de Delitos por Volumen de Denuncias</h3></div>',
        unsafe_allow_html=True,
    )
    chart_placeholder = st.empty()
    chart_placeholder.info("Cargando ranking de delitos desde la API...")
    try:
        df_plot = cargar_chart_delito_comun_rank()
        chart_placeholder.empty()

        if df_plot.empty:
            chart_placeholder.info("Sin datos disponibles")
        else:
            df_plot_display = df_plot.copy()
            df_plot_display["Delito_Principal"] = df_plot_display["Delito_Principal"].map(truncateArticle)
            chart_height = max(320, len(df_plot) * 44)
            chart_max_height = 640
            chart_placeholder.markdown(
                f"""
                <style>
                    div[data-testid="element-container"]:has(.delito-rank-chart-anchor) + div[data-testid="element-container"] {{
                        max-height: {chart_max_height}px;
                        overflow-y: auto;
                        overflow-x: hidden;
                        padding-right: 0.25rem;
                    }}
                </style>
                <div class="delito-rank-chart-anchor"></div>
                """,
                unsafe_allow_html=True,
            )

            fig = px.bar(
                df_plot_display, y="Delito_Principal", x="Casos", orientation="h",
                text="Casos", color="Casos",
                color_continuous_scale=[[0, "#c4b5fd"], [0.5, "#6c63ff"], [1, "#1e3a5f"]],
            )
            fig.update_traces(
                texttemplate="%{text:,}", textposition="outside",
                textfont=dict(size=11, color="#FFFFFF"), marker_line_width=0,
                hovertemplate="<b>%{y}</b><br>Casos: %{x:,}<extra></extra>",
            )
            fig.update_layout(**{
                **PLOTLY_LAYOUT,
                "font": dict(family="Inter, sans-serif", color="#FFFFFF"),
                "yaxis": dict(title="", tickfont=dict(size=10, color="#FFFFFF")),
                "xaxis": dict(title="", showgrid=True, gridcolor="rgba(108,99,255,0.08)",
                              zeroline=False, tickfont=dict(size=10, color="#FFFFFF")),
                "showlegend": False, "coloraxis_showscale": False,
                "height": chart_height,
                "margin": dict(t=10, b=40, l=200, r=60),
            })
            st.plotly_chart(fig, use_container_width=True, config={"responsive": True})
    except Exception as exc:
        chart_placeholder.error(f"No se pudo cargar el ranking de delitos: {exc}")


def _detail_anio_pico():
    """Vista de detalle: Año con más denuncias."""

    if anio_top is None:
        st.warning("No hay datos de serie histórica disponibles.")
        return

    año_valor = int(anio_top["Año"])
    casos_valor = int(anio_top["Casos"])
    ciudad_ese_año = str(anio_top.get("Ciudad_Top", "Sin dato")).title()
    delito_ese_año = str(anio_top.get("Delito_Top", "Sin dato")).title()
    delito_ese_año_titulo = truncateArticle(str(anio_top.get("Delito_Top", "Sin dato")))

    # Año anterior / posterior para comparativa
    df_hist_ord = df_hist.sort_values("Año")
    idx_pico = df_hist_ord[df_hist_ord["Año"] == año_valor].index
    casos_anterior, año_anterior = None, None
    casos_siguiente, año_siguiente = None, None
    if len(idx_pico):
        pos = df_hist_ord.index.get_loc(idx_pico[0])
        if pos > 0:
            row_ant = df_hist_ord.iloc[pos - 1]
            año_anterior = int(row_ant["Año"])
            casos_anterior = int(row_ant["Casos"])
        if pos < len(df_hist_ord) - 1:
            row_sig = df_hist_ord.iloc[pos + 1]
            año_siguiente = int(row_sig["Año"])
            casos_siguiente = int(row_sig["Casos"])

    var_anterior = (
        f"+{((casos_valor - casos_anterior) / casos_anterior * 100):.1f}% vs {año_anterior}"
        if casos_anterior and casos_anterior > 0 else "—"
    )

    st.markdown(
        f"""
        <div class="detail-hero green">
            <div class="dh-eyebrow">📅 Indicador · Año con mayor número de denuncias</div>
            <div class="dh-title">Año Pico: {año_valor}</div>
            <div class="dh-value">{casos_valor:,}</div>
            <div class="dh-sub">{var_anterior}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    promedio_historico = int(df_hist[df_hist["Casos"] > 0]["Casos"].mean())
    pct_sobre_promedio = (casos_valor - promedio_historico) / promedio_historico * 100 if promedio_historico else 0

    st.markdown(
        f"""
        <div class="detail-stats-grid">
            <div class="detail-stat-card">
                <div class="dsc-label">Denuncias en {año_valor}</div>
                <div class="dsc-value">{casos_valor:,}</div>
                <div class="dsc-note">Máximo histórico registrado</div>
            </div>
            <div class="detail-stat-card">
                <div class="dsc-label">Promedio histórico anual</div>
                <div class="dsc-value">{promedio_historico:,}</div>
                <div class="dsc-note">Media de todos los años con datos</div>
            </div>
            <div class="detail-stat-card">
                <div class="dsc-label">% sobre el promedio</div>
                <div class="dsc-value">+{pct_sobre_promedio:.1f}%</div>
                <div class="dsc-note">Por encima de la media histórica</div>
            </div>
            <div class="detail-stat-card">
                <div class="dsc-label">Ciudad más afectada ese año</div>
                <div class="dsc-value">{ciudad_ese_año}</div>
                <div class="dsc-note">Mayor volumen de denuncias</div>
            </div>
            <div class="detail-stat-card">
                <div class="dsc-label">Delito más frecuente ese año</div>
                <div class="dsc-value" style="font-size:0.95rem; line-height:1.3;">{delito_ese_año_titulo}</div>
                <div class="dsc-note">Conducta dominante en {año_valor}</div>
            </div>
            <div class="detail-stat-card">
                <div class="dsc-label">Año siguiente ({año_siguiente or '—'})</div>
                <div class="dsc-value">{f"{casos_siguiente:,}" if casos_siguiente else "—"}</div>
                <div class="dsc-note">{'↓ Disminución post-pico' if casos_siguiente and casos_siguiente < casos_valor else '↑ Continuó en alza'}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="detail-insight">
            <div class="di-icon">📈</div>
            <div class="di-body">
                <strong>Contexto del año pico</strong>
                <p>En <b>{año_valor}</b> se registró el máximo histórico de denuncias con <b>{casos_valor:,}</b> casos,
                un <b>{pct_sobre_promedio:.1f}%</b> por encima del promedio histórico anual.
                La ciudad más activa fue <b>{ciudad_ese_año}</b> y el delito preponderante fue
                <b>"{delito_ese_año_titulo}"</b>.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Línea histórica completa con el año pico resaltado
    st.markdown(
        '<div class="section-title"><div class="icon pink">📈</div>'
        '<h3>Serie Histórica Nacional (año pico resaltado)</h3></div>',
        unsafe_allow_html=True,
    )

    fig_hist = go.Figure()
    fig_hist.add_trace(go.Scatter(
        x=df_hist_linea["Año"], y=df_hist_linea["Casos"],
        fill="tozeroy", fillcolor="rgba(99, 102, 241, 0.08)",
        line=dict(width=0), showlegend=False, hoverinfo="skip",
    ))
    fig_hist.add_trace(go.Scatter(
        x=df_hist_linea["Año"], y=df_hist_linea["Casos"],
        mode="lines+markers",
        line=dict(width=3, color="#818cf8", shape="spline", smoothing=0.8),
        marker=dict(size=9, color="#6366f1", line=dict(width=2, color="#c7d2fe")),
        customdata=list(zip(df_hist_linea["Ciudad_Top"], df_hist_linea["Delito_Top"].map(truncateArticle))),
        hovertemplate=(
            "<b>Año:</b> %{x}<br>"
            "<b>Denuncias:</b> %{y:,}<br>"
            "<b>Ciudad top:</b> %{customdata[0]}<br>"
            "<b>Delito top:</b> %{customdata[1]}<extra></extra>"
        ),
        showlegend=False,
    ))
    # Marcador especial para el año pico
    df_pico_point = df_hist_linea[df_hist_linea["Año"] == año_valor]
    if not df_pico_point.empty:
        fig_hist.add_trace(go.Scatter(
            x=df_pico_point["Año"], y=df_pico_point["Casos"],
            mode="markers+text",
            marker=dict(size=16, color="#f59e0b", symbol="star",
                        line=dict(width=2, color="#ffffff")),
            text=[f"  Máximo {año_valor}"],
            textposition="top right",
            textfont=dict(size=12, color="#f59e0b"),
            showlegend=False,
            hovertemplate=f"<b>Año pico: {año_valor}</b><br>Casos: {casos_valor:,}<extra></extra>",
        ))

    fig_hist.update_layout(**{
        **PLOTLY_LAYOUT,
        "font": dict(family="Inter, sans-serif", color="#FFFFFF"),
        "xaxis": dict(
            tickmode="linear", dtick=1,
            range=[HISTORICAL_YEAR_START - 0.5, HISTORICAL_YEAR_END + 0.5],
            showgrid=False, tickfont=dict(size=11, color="#FFFFFF"), title="",
        ),
        "yaxis": dict(
            title=dict(text="Denuncias Registradas", font=dict(size=12, color="#FFFFFF")),
            showgrid=True, gridcolor="rgba(99,102,241,0.06)",
            zeroline=False, tickfont=dict(size=11, color="#FFFFFF"),
        ),
        "hovermode": "x unified",
        "height": 360,
    })
    _render_detail_chart(fig_hist)


# ============================================================================
# RENDERIZADO PRINCIPAL – controla qué vista se muestra
# ============================================================================

if st.session_state.active_view is not None:
    _render_pending_scroll_reset()
    # ── VISTA DE DETALLE ──────────────────────────────────────────────────
    render_detail_view(st.session_state.active_view)

else:
    _render_pending_scroll_reset()
    # ── VISTA PRINCIPAL (dashboard completo sin modificaciones) ───────────

    # ── HERO HEADER ───────────────────────────────────────────────────────
    st.markdown(
        '<div class="hero">'
        '<h1>Cibercrimen en Colombia</h1>'
        '<p>Análisis interactivo de denuncias por delitos informáticos registrados '
        'ante la Policía Nacional. Explora la distribución geográfica, tendencias '
        'históricas y los delitos más frecuentes en cada departamento.</p>'
        '<span class="tag">🔄 Datos en tiempo real · API Datos Abiertos</span>'
        '</div>',
        unsafe_allow_html=True,
    )

    # ── KPI METRIC CARDS (ahora con botones de navegación) ────────────────
    #
    # Estrategia: cada KPI se divide en dos columnas Streamlit:
    #   • columna izquierda  → HTML decorativo (tarjeta visual)
    #   • columna derecha    → botón st.button invisible pero funcional
    # El botón actualiza session_state y llama a st.rerun() para cambiar la vista.

    kpi_html = f"""
    <div class="kpi-container">
        <div class="kpi-card">
            <div class="kpi-icon">📊</div>
            <div class="kpi-label">Total Denuncias</div>
            <div class="kpi-value">{total_nacional:,}</div>
            <div class="kpi-sub">acumulado nacional</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-icon">🏙️</div>
            <div class="kpi-label">Depto. Más Afectado</div>
            <div class="kpi-value">{str(depto_top['Departamento']).title()}</div>
            <div class="kpi-sub">{int(depto_top['Casos']):,} casos</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-icon">⚠️</div>
            <div class="kpi-label">Delito Más Común</div>
            <div class="kpi-value" style="font-size:0.95rem; line-height:1.3;">{truncateArticle(str(delito_top_global))}</div>
            <div class="kpi-sub">a nivel nacional</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-icon">📅</div>
            <div class="kpi-label">Año Pico</div>
            <div class="kpi-value">{int(anio_top['Año']) if anio_top is not None else '—'}</div>
            <div class="kpi-sub">{int(anio_top['Casos']):,} denuncias</div>
        </div>
    </div>
    """
    st.markdown(kpi_html, unsafe_allow_html=True)

    # Botones Streamlit alineados bajo las tarjetas KPI
    # Usamos columnas para alinearlos visualmente con las 4 tarjetas
    btn_cols = st.columns(4)
    kpi_keys = ["total_casos", "depto_top", "delito_top", "anio_pico"]
    kpi_labels = ["📊 Total de Casos", "🏙️ Depto. Afectado", "⚠️ Delito Común", "📅 Año Pico"]

    for col, key, label in zip(btn_cols, kpi_keys, kpi_labels):
        with col:
            if st.button(label, key=f"kpi_btn_{key}", use_container_width=True):
                navigate_to(key)
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── GLOSARIO ──────────────────────────────────────────────────────────
    st.markdown(
        '<div class="section-title"><div class="icon yellow">📚</div>'
        '<a href="https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=34492" '
        'target="_blank" rel="noopener noreferrer" '
        'style="color: inherit; text-decoration: none; display: inline-flex; align-items: center;"><h3 style="margin: 0;">Glosario de Delitos (Ley 1273 de 2009)</h3></a></div>',
        unsafe_allow_html=True,
    )

    st.markdown("""
    <div class="glossary-grid">
        <div class="glossary-card"><h4>🛡️ Art. 269I – Robo Cibernético (Cybertheft)</h4><p>Hurtar dinero o bienes manipulando sistemas informáticos o suplantando identidades ante sistemas de autenticación, como el clonado de tarjetas o el fraude en cajeros.</p></div>
        <div class="glossary-card"><h4>🔓 Art. 269A – Acceso No Autorizado / Hackeo (Unauthorized Access)</h4><p>Ingresar a un sistema informático sin permiso, ya sea saltando medidas de seguridad o permaneciendo en él contra la voluntad del propietario.</p></div>
        <div class="glossary-card"><h4>🗃️ Art. 269F – Violación de Privacidad / Fuga de Datos (Data Breach)</h4><p>Obtener, vender, intercambiar o divulgar datos personales de terceros sin autorización, con fines de lucro propio o ajeno.</p></div>
        <div class="glossary-card"><h4>🎣 Art. 269G – Phishing / Suplantación de Identidad Digital (Phishing)</h4><p>Crear páginas web o enlaces falsos que imitan sitios legítimos (bancos, redes sociales) para engañar a usuarios y robarles sus credenciales o datos.</p></div>
        <div class="glossary-card"><h4>💸 Art. 269J – Fraude Bancario Electrónico (Wire Fraud)</h4><p>Transferir activos de una víctima sin su consentimiento mediante manipulación de sistemas financieros. Es el delito con la pena más alta de la ley: hasta 10 años de prisión.</p></div>
        <div class="glossary-card"><h4>🎧 Art. 269C – Interceptación de Comunicaciones / Espionaje Digital (Wiretapping / Sniffing)</h4><p>Capturar o "escuchar" datos mientras viajan por una red sin autorización judicial, como espiar correos, mensajes o tráfico web en tiempo real.</p></div>
        <div class="glossary-card"><h4>💥 Art. 269D – Sabotaje Informático (Cyber Sabotage)</h4><p>Destruir, borrar, alterar o dañar datos o sistemas de forma intencional, inutilizándolos total o parcialmente.</p></div>
        <div class="glossary-card"><h4>🦠 Art. 269E – Uso de Malware (Malware Deployment)</h4><p>Crear, distribuir o introducir software diseñado para causar daño: virus, ransomware, spyware, troyanos, entre otros.</p></div>
        <div class="glossary-card"><h4>⛔ Art. 269B – Ataque de Denegación de Servicio (DoS / DDoS Attack)</h4><p>Bloquear o interrumpir deliberadamente el funcionamiento de un sistema, red o servicio para que usuarios legítimos no puedan acceder a él.</p></div>
    </div>

    <div style="margin-top: 1.5rem; padding: 1.2rem; background-color: rgba(245, 158, 11, 0.08); border-left: 4px solid #f59e0b; border-radius: 8px; width: 100%; box-sizing: border-box; display: flex; align-items: flex-start; gap: 0.8rem;">
        <span style="font-size: 1.5rem; flex-shrink: 0; line-height: 1;">⚠️</span>
        <div>
            <h4 style="margin: 0 0 0.5rem 0; font-size: 0.95rem; color: #111111; font-weight: 700;">Nota – Art. 269H | Circunstancias Agravantes Cibernéticas (Cybercrime Aggravating Factors)</h4>
            <p style="margin: 0; font-size: 0.85rem; color: #334155; line-height: 1.5;">No es un delito en sí, sino un conjunto de condiciones que aumentan la pena entre un 50% y un 75% cuando el crimen afecta al Estado, involucra funcionarios públicos o tiene fines terroristas, entre otros.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── TIP ───────────────────────────────────────────────────────────────
    st.markdown(
        '<div class="tip-box">'
        '<span class="tip-icon">💡</span>'
        'Pasa el cursor o haz clic sobre un departamento o ciudad para ver su detalle y la concentración relativa frente al resto del mapa.'
        '</div>',
        unsafe_allow_html=True,
    )

    # ── SECCIÓN 1: CONCENTRACIÓN GEOGRÁFICA ──────────────────────────────
    col_map1_title, col_map1_filter = st.columns([3, 1])
    with col_map1_title:
        st.markdown(
            '<div class="section-title">'
            '<div class="icon purple">🗺️</div>'
            '<h3>Concentración Geográfica</h3>'
            '</div>',
            unsafe_allow_html=True,
        )
    with col_map1_filter:
        seleccion = st.selectbox("Filtrar por región", lista_deptos)

    if seleccion == "TOTAL NACIONAL":
        df_mapa = df_colombia.copy()
        df_barras = df_mapa
        zoom_mapa = 4.5
        centro_lat, centro_lon = 4.5709, -74.2973
        titulo_barras = "Departamentos con Mayor Incidencia"
    else:
        df_mapa = df_colombia[df_colombia["Departamento"] == seleccion].copy()
        df_barras = df_mapa
        zoom_mapa = 6.0
        centro_lat = float(df_mapa["Lat"].iloc[0])
        centro_lon = float(df_mapa["Lon"].iloc[0])
        titulo_barras = f"Detalle — {seleccion.title()}"

    df_mapa = preparar_participacion_geografica(df_mapa)

    fig_mapa = px.choropleth_mapbox(
        df_mapa,
        geojson=geojson_col,
        locations="Codigo_DANE",
        featureidkey="properties.codigo_departamento_n",
        color="Casos",
        hover_name="Departamento",
        custom_data=["Casos", "Delito_Principal", "Pct_Seleccionado", "Pct_Resto"],
        color_continuous_scale=[
            [0, "#f4f6f9"], [0.5, "#00b4d8"], [1, "#1e3a5f"],
        ],
        range_color=(df_colombia["Casos"].min(), df_colombia["Casos"].max()),
        mapbox_style="carto-darkmatter",
        zoom=zoom_mapa,
        center={"lat": centro_lat, "lon": centro_lon},
        opacity=0.82,
    )
    customdata_departamentos = list(
        zip(
            df_mapa["Casos"],
            df_mapa["Delito_Principal"].map(formatear_delito_principal_popup),
            df_mapa["Pct_Seleccionado"],
            df_mapa["Pct_Resto"],
        )
    )
    fig_mapa.update_traces(
        customdata=customdata_departamentos,
        hovertemplate=(
            "<b>%{hovertext}</b><br>"
            "<b>Casos:</b> %{customdata[0]:,}<br>"
            "<b>Delito principal:</b> %{customdata[1]}<br>"
            "<b>Participación:</b> %{customdata[2]:.1f}%<extra></extra>"
        ),
    )
    fig_mapa.update_traces(hoverinfo="none", hovertemplate=None)
    layout_mapa = {
        **PLOTLY_LAYOUT,
        "coloraxis_colorbar": dict(
            title=dict(text="Casos", font=dict(size=12, color="#1a1a1a")),
            tickfont=dict(size=10, color="#111111"),
            bgcolor="rgba(255,255,255,0.7)",
            borderwidth=0, len=0.6, thickness=12, x=0.02, xanchor="left",
        ),
        "hoverlabel": dict(
            bgcolor="#ffffff", font_size=13, font_family="Inter, sans-serif",
            font_color="#111111", bordercolor="#cbd5e1",
        ),
        "height": 480,
    }
    fig_mapa.update_layout(**layout_mapa)
    construir_mapa_con_panel(
        fig=fig_mapa, component_id="departamentos", height=480,
        panel_title="Detalle interactivo",
        placeholder_text="Pasa el cursor o haz clic sobre un departamento para ver su participación frente al resto del país.",
        selected_label="Departamento", other_label="Otros departamentos",
        selected_color="#00b4d8", other_color="#1e3a5f",
        cases_idx=0, crime_idx=1, selected_pct_idx=2, other_pct_idx=3,
    )
    st.markdown("<br>", unsafe_allow_html=True)

    # ── SECCIÓN 2: CIUDADES ───────────────────────────────────────────────
    col_map2_title, col_map2_filter = st.columns([3, 1])
    with col_map2_title:
        st.markdown(
            '<div class="section-title">'
            '<div class="icon cyan">📍</div>'
            '<h3>Las 30 Ciudades con Mayor Incidencia de Ataques</h3>'
            '</div>',
            unsafe_allow_html=True,
        )
    with col_map2_filter:
        seleccion_ciudad = st.selectbox("Filtrar mapa de ciudades", lista_ciudades)

    df_ciudades_base = df_ciudades_mapa.copy()
    zoom_ciudades = 4.5
    centro_lat_ciudades, centro_lon_ciudades = 4.5709, -74.2973

    if seleccion_ciudad == "TODAS LAS CIUDADES":
        limite_ciudades = 30
        df_ciudades = df_ciudades_base.nlargest(limite_ciudades, "Casos").copy()
    else:
        ciudad_filtrada, departamento_filtrado = seleccion_ciudad.rsplit(" - ", 1)
        df_ciudades = df_ciudades_base[
            (df_ciudades_base["Ciudad"] == ciudad_filtrada)
            & (df_ciudades_base["Departamento"] == departamento_filtrado)
        ].copy()
        if not df_ciudades.empty:
            centro_lat_ciudades = float(df_ciudades["Lat_Ciudad"].iloc[0])
            centro_lon_ciudades = float(df_ciudades["Lon_Ciudad"].iloc[0])
            zoom_ciudades = 8.5

    df_ciudades = preparar_participacion_geografica(df_ciudades)

    fig_mapa_ciudades = px.scatter_mapbox(
        df_ciudades, lat="Lat_Ciudad", lon="Lon_Ciudad",
        size="Casos", color="Casos", hover_name="Ciudad",
        custom_data=["Departamento", "Casos", "Delito_Principal_Ciudad", "Pct_Seleccionado", "Pct_Resto"],
        color_continuous_scale=[[0, "#f4f6f9"], [0.5, "#6c63ff"], [1, "#1e3a5f"]],
        range_color=(0, max(int(df_ciudades_mapa["Casos"].max()), 1)),
        size_max=34, zoom=zoom_ciudades,
        center={"lat": centro_lat_ciudades, "lon": centro_lon_ciudades},
        opacity=0.88, mapbox_style="carto-darkmatter",
    )
    customdata_ciudades = list(
        zip(
            df_ciudades["Departamento"],
            df_ciudades["Casos"],
            df_ciudades["Delito_Principal_Ciudad"].map(formatear_delito_principal_popup),
            df_ciudades["Pct_Seleccionado"],
            df_ciudades["Pct_Resto"],
        )
    )
    fig_mapa_ciudades.update_traces(
        customdata=customdata_ciudades,
        hovertemplate=(
            "<b>%{hovertext}</b><br>"
            "<b>Departamento:</b> %{customdata[0]}<br>"
            "<b>Casos:</b> %{customdata[1]:,}<br>"
            "<b>Delito principal:</b> %{customdata[2]}<br>"
            "<b>Participación:</b> %{customdata[3]:.1f}%<extra></extra>"
        ),
    )
    fig_mapa_ciudades.update_traces(hoverinfo="none", hovertemplate=None)
    layout_ciudades = {
        **PLOTLY_LAYOUT,
        "coloraxis_colorbar": dict(
            title=dict(text="Casos", font=dict(size=12, color="#1a1a1a")),
            tickfont=dict(size=10, color="#111111"),
            bgcolor="rgba(255,255,255,0.7)",
            borderwidth=0, len=0.6, thickness=12, x=0.02, xanchor="left",
        ),
        "hoverlabel": dict(
            bgcolor="#ffffff", font_size=13, font_family="Inter, sans-serif",
            font_color="#111111", bordercolor="#cbd5e1",
        ),
        "height": 420,
    }
    fig_mapa_ciudades.update_layout(**layout_ciudades)
    construir_mapa_con_panel(
        fig=fig_mapa_ciudades, component_id="ciudades", height=420,
        panel_title="Detalle interactivo",
        placeholder_text="Pasa el cursor sobre una ciudad para ver su participación frente al resto de ciudades visibles.",
        selected_label="Ciudad", other_label="Otras ciudades",
        selected_color="#6c63ff", other_color="#1e3a5f",
        cases_idx=1, crime_idx=2, selected_pct_idx=3, other_pct_idx=4,
        subtitle_idx=0, subtitle_prefix="Departamento: ",
    )
    st.markdown("<br>", unsafe_allow_html=True)

    # ── SECCIÓN 3: BARRAS ─────────────────────────────────────────────────
    st.markdown(
        '<div class="section-title">'
        '<div class="icon cyan">📊</div>'
        f'<h3>{titulo_barras}</h3>'
        f'<span class="badge">{seleccion.title()}</span>'
        '</div>',
        unsafe_allow_html=True,
    )

    df_top = df_barras.nlargest(5, "Casos").sort_values("Casos", ascending=True)
    df_top_display = df_top.copy()
    df_top_display["Delito_Principal_Display"] = df_top_display["Delito_Principal"].map(truncateArticle)
    fig_barras = px.bar(
        df_top_display, y="Departamento", x="Casos", text="Casos", orientation="h",
        color="Casos",
        color_continuous_scale=[[0, "#a8dce7"], [0.5, "#00b4d8"], [1, "#1e3a5f"]],
        custom_data=["Delito_Principal_Display"],
    )
    fig_barras.update_traces(
        texttemplate="%{text:,}", textposition="outside",
        textfont=dict(size=12, color="#FFFFFF", family="Inter"),
        marker_line_width=0,
        hovertemplate=(
            "<b>%{y}</b><br>"
            "<b>Casos:</b> %{x:,}<br>"
            "<b>Delito Principal:</b> %{customdata[0]}<extra></extra>"
        ),
    )
    layout_barras = {
        **PLOTLY_LAYOUT,
        "font": dict(family="Inter, sans-serif", color="#FFFFFF"),
        "yaxis": dict(title="", tickfont=dict(size=11, color="#FFFFFF")),
        "xaxis": dict(
            title="", showgrid=True, gridcolor="rgba(30,58,95,0.08)",
            zeroline=False, tickfont=dict(size=11, color="#FFFFFF"),
        ),
        "hoverlabel": dict(
            bgcolor="#ffffff", font_size=13, font_family="Inter, sans-serif",
            font_color="#111111", bordercolor="#cbd5e1",
        ),
        "showlegend": False, "coloraxis_showscale": False, "height": 360,
    }
    fig_barras.update_layout(**layout_barras)
    st.plotly_chart(fig_barras, use_container_width=True)

    # ── DIVIDER ───────────────────────────────────────────────────────────
    st.markdown("<hr>", unsafe_allow_html=True)

    # ── LÍNEA HISTÓRICA ───────────────────────────────────────────────────
    st.markdown(
        '<div class="section-title">'
        '<div class="icon pink">📈</div>'
        '<h3>Evolución Histórica Nacional</h3>'
        '<span class="badge">Serie temporal</span>'
        '</div>',
        unsafe_allow_html=True,
    )

    fig_linea = go.Figure()
    fig_linea.add_trace(go.Scatter(
        x=df_hist_linea["Año"], y=df_hist_linea["Casos"],
        fill="tozeroy", fillcolor="rgba(99, 102, 241, 0.08)",
        line=dict(width=0), showlegend=False, hoverinfo="skip",
    ))
    fig_linea.add_trace(go.Scatter(
        x=df_hist_linea["Año"], y=df_hist_linea["Casos"],
        mode="lines+markers",
        line=dict(width=3, color="#818cf8", shape="spline", smoothing=0.8),
        marker=dict(size=10, color="#6366f1", line=dict(width=2, color="#c7d2fe"), symbol="circle"),
        customdata=list(zip(df_hist_linea["Ciudad_Top"], df_hist_linea["Delito_Top"].map(truncateArticle))),
        hovertemplate=(
            "<b>Año:</b> %{x}<br>"
            "<b>Denuncias:</b> %{y:,}<br>"
            "<b>Ciudad más afectada:</b> %{customdata[0]}<br>"
            "<b>Delito más frecuente:</b> %{customdata[1]}<extra></extra>"
        ),
        showlegend=False,
    ))
    layout_linea = {
        **PLOTLY_LAYOUT,
        "font": dict(family="Inter, sans-serif", color="#FFFFFF"),
        "xaxis": dict(
            tickmode="linear", dtick=1,
            range=[HISTORICAL_YEAR_START - 0.5, HISTORICAL_YEAR_END + 0.5],
            showgrid=False, tickfont=dict(size=11, color="#FFFFFF"), title="",
        ),
        "yaxis": dict(
            title=dict(text="Denuncias Registradas", font=dict(size=12, color="#FFFFFF")),
            showgrid=True, gridcolor="rgba(99,102,241,0.06)",
            zeroline=False, tickfont=dict(size=11, color="#FFFFFF"),
        ),
        "hovermode": "x unified",
        "height": 340,
    }
    fig_linea.update_layout(**layout_linea)
    st.plotly_chart(fig_linea, use_container_width=True)

    st.divider()

    # ── FOOTER ────────────────────────────────────────────────────────────
    st.markdown(
        '<div class="dashboard-footer">'
        'Dashboard Cibercrimen Colombia · Datos: '
        '<a href="https://www.datos.gov.co/" target="_blank">datos.gov.co</a> · '
        'Policía Nacional de Colombia'
        '</div>',
        unsafe_allow_html=True,
    )
