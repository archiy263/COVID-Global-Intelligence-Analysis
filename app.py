import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from textwrap import dedent


# Page configuration

st.set_page_config(
    page_title="COVID-19 Global Intelligence",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)


# Render dashboard HTML reliably
_original_markdown = st.markdown

def _render_markdown(body, *args, **kwargs):
    if isinstance(body, str):
        body = dedent(body).strip()

        # Streamlit can display custom HTML as literal text in some
        # markdown contexts. Use st.html for dashboard components so
        # the hero, cards, labels and information panels render as HTML.
        if kwargs.get("unsafe_allow_html", False) and "<style" not in body.lower():
            if hasattr(st, "html"):
                kwargs = dict(kwargs)
                kwargs.pop("unsafe_allow_html", None)
                return st.html(body)

    return _original_markdown(body, *args, **kwargs)

st.markdown = _render_markdown


# Visual theme

PRIMARY = "#6366F1"
SECONDARY = "#14B8A6"
ACCENT = "#C026D3"
DANGER = "#F43F5E"
TEXT = "#F8FAFC"
MUTED = "#94A3B8"
GRID = "rgba(148,163,184,0.12)"
CARD = "rgba(15,23,42,0.72)"
CARD_BORDER = "rgba(148,163,184,0.14)"

# Notebook color palettes — kept identical to the original notebook
MAP_GRADIENT = [
    "#111827",
    "#312E81",
    "#4F46E5",
    "#7C3AED",
    "#C026D3",
    "#F43F5E",
]

IMPACT_GRADIENT = [
    "#312E81",
    "#6366F1",
    "#8B5CF6",
    "#C026D3",
    "#F43F5E",
]

REGIONAL_GRADIENT = [
    [0, "#312E81"],
    [0.45, "#6366F1"],
    [0.75, "#8B5CF6"],
    [1, "#14B8A6"],
]

# Backward-compatible default for charts that use the project's main scale.
GRADIENT = [
    [0.00, "#111827"],
    [0.20, "#312E81"],
    [0.42, "#4F46E5"],
    [0.64, "#7C3AED"],
    [0.82, "#C026D3"],
    [1.00, "#F43F5E"],
]

IMPACT_COLORS = {
    "Low": "#14B8A6",
    "Moderate": "#38BDF8",
    "High": "#8B5CF6",
    "Critical": "#F43F5E",
    "Insufficient Data": "#475569",
}


# Global styling

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at 15% 0%,
                rgba(99,102,241,0.10),
                transparent 28%
            ),
            radial-gradient(
                circle at 90% 18%,
                rgba(20,184,166,0.07),
                transparent 25%
            ),
            #050810;
        color: #F8FAFC;
    }

    .main .block-container {
        max-width: 1500px;
        padding-top: 2.2rem;
        padding-bottom: 4rem;
    }

    [data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #0B1020 0%,
                #080C16 52%,
                #060910 100%
            );
        border-right: 1px solid rgba(148,163,184,0.10);
    }

    [data-testid="stSidebar"] .block-container {
        padding: 1.6rem 1.1rem;
    }

    .hero {
        position: relative;
        overflow: hidden;
        padding: 3.2rem 3.5rem;
        border-radius: 28px;
        border: 1px solid rgba(148,163,184,0.16);
        background:
            radial-gradient(
                circle at 12% 20%,
                rgba(99,102,241,0.28),
                transparent 34%
            ),
            radial-gradient(
                circle at 90% 80%,
                rgba(20,184,166,0.18),
                transparent 34%
            ),
            linear-gradient(
                120deg,
                rgba(30,41,91,0.74),
                rgba(7,35,40,0.74)
            );
        box-shadow:
            0 24px 80px rgba(0,0,0,0.30);
        margin-bottom: 3rem;
    }

    .hero::after {
        content: "";
        position: absolute;
        width: 320px;
        height: 320px;
        right: -130px;
        top: -170px;
        border-radius: 50%;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow:
            0 0 0 35px rgba(255,255,255,0.015),
            0 0 0 70px rgba(255,255,255,0.01);
    }

    .hero-label {
        display: inline-block;
        padding: 0.48rem 0.9rem;
        border-radius: 999px;
        border: 1px solid rgba(129,140,248,0.42);
        background: rgba(79,70,229,0.12);
        color: #A5B4FC;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        margin-bottom: 1.2rem;
    }

    .hero-title {
        font-size: clamp(2.5rem, 5vw, 4.8rem);
        line-height: 0.98;
        font-weight: 800;
        letter-spacing: -0.055em;
        color: #FFFFFF;
        margin-bottom: 1.2rem;
        position: relative;
        z-index: 2;
    }

    .hero-description {
        max-width: 950px;
        color: #CBD5E1;
        font-size: 1.08rem;
        line-height: 1.8;
        position: relative;
        z-index: 2;
    }

    .hero-meta {
        display: flex;
        flex-wrap: wrap;
        gap: 0.6rem;
        margin-top: 1.7rem;
        position: relative;
        z-index: 2;
    }

    .hero-pill {
        padding: 0.5rem 0.8rem;
        border-radius: 999px;
        background: rgba(255,255,255,0.055);
        border: 1px solid rgba(255,255,255,0.09);
        color: #CBD5E1;
        font-size: 0.72rem;
        font-weight: 600;
    }

    .coverage-box {
        margin-top: 1.8rem;
        padding: 1rem 1.2rem;
        border-left: 3px solid #14B8A6;
        background: rgba(15,23,42,0.42);
        border-radius: 0 12px 12px 0;
        position: relative;
        z-index: 2;
    }

    .coverage-label {
        color: #5EEAD4;
        font-size: 0.68rem;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }

    .coverage-value {
        color: #FFFFFF;
        font-size: 1.05rem;
        font-weight: 700;
    }

    .coverage-note {
        color: #94A3B8;
        font-size: 0.74rem;
        line-height: 1.5;
        margin-top: 0.25rem;
    }

    .section-title {
        color: #F8FAFC;
        font-size: 1.55rem;
        font-weight: 750;
        letter-spacing: -0.025em;
        margin-top: 3.2rem;
        margin-bottom: 0.35rem;
    }

    .section-description {
        color: #94A3B8;
        font-size: 0.88rem;
        line-height: 1.65;
        max-width: 950px;
        margin-bottom: 1.35rem;
    }

    .kpi {
        min-height: 165px;
        padding: 1.35rem 1.4rem;
        border-radius: 20px;
        border: 1px solid rgba(148,163,184,0.13);
        background:
            linear-gradient(
                145deg,
                rgba(30,41,59,0.62),
                rgba(15,23,42,0.48)
            );
        box-shadow:
            inset 0 1px 0 rgba(255,255,255,0.025),
            0 16px 40px rgba(0,0,0,0.16);
        transition: transform 0.2s ease;
    }

    .kpi:hover {
        transform: translateY(-3px);
        border-color: rgba(99,102,241,0.32);
    }

    .kpi-label {
        color: #94A3B8;
        font-size: 0.68rem;
        font-weight: 750;
        letter-spacing: 0.13em;
        text-transform: uppercase;
    }

    .kpi-value {
        color: #FFFFFF;
        font-size: 2rem;
        font-weight: 800;
        letter-spacing: -0.04em;
        margin-top: 0.75rem;
    }

    .kpi-note {
        color: #64748B;
        font-size: 0.72rem;
        margin-top: 0.45rem;
    }

    .purpose-card {
        min-height: 215px;
        padding: 1.45rem;
        border-radius: 20px;
        background: rgba(15,23,42,0.55);
        border: 1px solid rgba(148,163,184,0.11);
        box-shadow: 0 18px 50px rgba(0,0,0,0.12);
    }

    .purpose-number {
        color: #818CF8;
        font-size: 0.66rem;
        letter-spacing: 0.16em;
        font-weight: 800;
        margin-bottom: 0.85rem;
    }

    .purpose-title {
        color: #F8FAFC;
        font-size: 1.05rem;
        font-weight: 700;
        margin-bottom: 0.65rem;
    }

    .purpose-text {
        color: #94A3B8;
        font-size: 0.78rem;
        line-height: 1.7;
    }

    .method-card {
        min-height: 150px;
        padding: 1.15rem;
        border-radius: 18px;
        background: rgba(15,23,42,0.46);
        border: 1px solid rgba(148,163,184,0.10);
    }

    .method-number {
        color: #14B8A6;
        font-size: 0.7rem;
        font-weight: 800;
        margin-bottom: 0.65rem;
    }

    .method-title {
        color: #F8FAFC;
        font-size: 0.92rem;
        font-weight: 700;
        margin-bottom: 0.45rem;
    }

    .method-text {
        color: #64748B;
        font-size: 0.72rem;
        line-height: 1.55;
    }

    .analysis-card {
        padding: 1.35rem;
        border-radius: 20px;
        border: 1px solid rgba(148,163,184,0.12);
        background:
            linear-gradient(
                145deg,
                rgba(15,23,42,0.72),
                rgba(30,41,59,0.38)
            );
        min-height: 150px;
    }

    .analysis-label {
        color: #818CF8;
        font-size: 0.67rem;
        font-weight: 800;
        letter-spacing: 0.13em;
        text-transform: uppercase;
    }

    .analysis-value {
        color: #FFFFFF;
        font-size: 1.5rem;
        font-weight: 800;
        margin-top: 0.6rem;
    }

    .analysis-note {
        color: #64748B;
        font-size: 0.72rem;
        line-height: 1.5;
        margin-top: 0.45rem;
    }

    .explain-card {
        padding: 1.3rem;
        border-radius: 18px;
        border: 1px solid rgba(148,163,184,0.10);
        background: rgba(15,23,42,0.45);
        min-height: 160px;
    }

    .explain-label {
        color: #14B8A6;
        font-size: 0.66rem;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        font-weight: 800;
    }

    .explain-title {
        color: #F8FAFC;
        font-size: 1rem;
        font-weight: 700;
        margin: 0.45rem 0 0.55rem;
    }

    .explain-text {
        color: #94A3B8;
        font-size: 0.76rem;
        line-height: 1.65;
    }

    .finding-card {
        padding: 1.25rem;
        border-radius: 18px;
        border: 1px solid rgba(148,163,184,0.10);
        background: rgba(15,23,42,0.45);
        min-height: 145px;
    }

    .finding-title {
        color: #F8FAFC;
        font-size: 0.9rem;
        font-weight: 700;
        margin-bottom: 0.55rem;
    }

    .finding-text {
        color: #94A3B8;
        font-size: 0.76rem;
        line-height: 1.65;
    }

    .question-card {
        padding: 1.2rem;
        border-radius: 18px;
        border: 1px solid rgba(148,163,184,0.10);
        background: rgba(15,23,42,0.42);
    }

    .question-title {
        color: #CBD5E1;
        font-size: 0.82rem;
        font-weight: 700;
    }

    .question-answer {
        color: #64748B;
        font-size: 0.72rem;
        line-height: 1.6;
        margin-top: 0.45rem;
    }

    .footer {
        text-align: center;
        color: #475569;
        font-size: 0.68rem;
        padding-top: 3rem;
        padding-bottom: 1rem;
    }

    .side-brand {
        padding: 0.6rem 0.3rem 1.25rem;
    }

    .side-kicker {
        color: #818CF8;
        font-size: 0.63rem;
        font-weight: 800;
        letter-spacing: 0.16em;
        text-transform: uppercase;
    }

    .side-title {
        color: #F8FAFC;
        font-size: 1.2rem;
        font-weight: 800;
        margin-top: 0.4rem;
    }

    .side-subtitle {
        color: #64748B;
        font-size: 0.73rem;
        line-height: 1.55;
        margin-top: 0.55rem;
    }

    .side-section {
        color: #CBD5E1;
        font-size: 0.7rem;
        font-weight: 800;
        letter-spacing: 0.13em;
        text-transform: uppercase;
        margin-top: 1.1rem;
        margin-bottom: 0.7rem;
    }

    .side-card {
        padding: 0.9rem;
        border-radius: 14px;
        background: rgba(15,23,42,0.62);
        border: 1px solid rgba(148,163,184,0.09);
        margin-bottom: 0.55rem;
    }

    .side-card-label {
        color: #64748B;
        font-size: 0.62rem;
        font-weight: 800;
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }

    .side-card-value {
        color: #F8FAFC;
        font-size: 0.82rem;
        font-weight: 700;
        margin-top: 0.3rem;
    }

    .side-card-note {
        color: #475569;
        font-size: 0.65rem;
        margin-top: 0.25rem;
        line-height: 1.4;
    }

    div[data-testid="stMetric"] {
        background: transparent;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# Data loading

@st.cache_data
def load_country_data():
    return pd.read_csv(
        "data/processed/covid_dashboard_ready.csv"
    )


@st.cache_data
def load_time_series():
    data = pd.read_csv(
        "data/raw/covid_grouped.csv"
    )

    if "Date" in data.columns:
        data["Date"] = pd.to_datetime(
            data["Date"],
            errors="coerce"
        )

    return data


covid = load_country_data()
time_series = load_time_series()


# Data preparation

if "Country" in covid.columns:
    covid["Country"] = (
        covid["Country"]
        .astype(str)
        .str.strip()
    )

if "Continent" in covid.columns:
    covid["Continent"] = (
        covid["Continent"]
        .astype(str)
        .str.strip()
    )

if "Impact_Category" in covid.columns:
    covid["Impact_Category"] = (
        covid["Impact_Category"]
        .fillna("Insufficient Data")
    )


# Numeric columns

numeric_columns = [
    "Population",
    "TotalCases",
    "TotalDeaths",
    "TotalRecovered",
    "ActiveCases",
    "TotalTests",
    "COVID_Impact_Score",
    "Calculated_Tests_per_1M",
    "Calculated_Cases_per_1M",
    "Calculated_Deaths_per_1M",
]

for column in numeric_columns:
    if column in covid.columns:
        covid[column] = pd.to_numeric(
            covid[column],
            errors="coerce"
        )


# Date coverage

valid_dates = (
    time_series["Date"].dropna()
    if "Date" in time_series.columns
    else pd.Series(dtype="datetime64[ns]")
)

if len(valid_dates) > 0:
    coverage_start = valid_dates.min()
    coverage_end = valid_dates.max()

    coverage_range = (
        f"{coverage_start.strftime('%d %b %Y')} "
        f"— {coverage_end.strftime('%d %b %Y')}"
    )

    date_count = valid_dates.nunique()
else:
    coverage_range = "Coverage unavailable"
    date_count = 0


# Summary metrics

total_countries = (
    covid["Country"].nunique()
    if "Country" in covid.columns
    else 0
)

total_cases = (
    covid["TotalCases"].sum()
    if "TotalCases" in covid.columns
    else 0
)

total_deaths = (
    covid["TotalDeaths"].sum()
    if "TotalDeaths" in covid.columns
    else 0
)

total_recovered = (
    covid["TotalRecovered"].sum()
    if "TotalRecovered" in covid.columns
    else 0
)

total_active = (
    covid["ActiveCases"].sum()
    if "ActiveCases" in covid.columns
    else 0
)


# Sidebar

with st.sidebar:

    st.markdown(
        """
        <div class="side-brand">
            <div class="side-kicker">
                Global Analytics
            </div>

            <div class="side-title">
                COVID-19 Intelligence
            </div>

            <div class="side-subtitle">
                Interactive exploration of reported pandemic
                data across geography, time, impact and
                analytical relationships.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="side-section">Dashboard Controls</div>',
        unsafe_allow_html=True,
    )

    map_metric = st.selectbox(
        "Map metric",
        [
            "TotalCases",
            "TotalDeaths",
            "TotalRecovered",
            "ActiveCases",
        ],
        format_func=lambda value: {
            "TotalCases": "Reported Cases",
            "TotalDeaths": "Reported Deaths",
            "TotalRecovered": "Reported Recoveries",
            "ActiveCases": "Active Cases",
        }[value],
    )

    ranking_metric = st.selectbox(
        "Ranking metric",
        [
            "TotalCases",
            "TotalDeaths",
            "TotalRecovered",
            "ActiveCases",
            "COVID_Impact_Score",
        ],
        format_func=lambda value: {
            "TotalCases": "Reported Cases",
            "TotalDeaths": "Reported Deaths",
            "TotalRecovered": "Reported Recoveries",
            "ActiveCases": "Active Cases",
            "COVID_Impact_Score": "Calculated Impact Score",
        }[value],
    )

    st.markdown(
        '<div class="side-section">Dataset Profile</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="side-card">
            <div class="side-card-label">
                Geographic Coverage
            </div>

            <div class="side-card-value">
                {total_countries:,} countries / regions
            </div>

            <div class="side-card-note">
                Country-level analytical records
            </div>
        </div>

        <div class="side-card">
            <div class="side-card-label">
                Observation Period
            </div>

            <div class="side-card-value">
                {coverage_range}
            </div>

            <div class="side-card-note">
                Available time-series coverage
            </div>
        </div>

        <div class="side-card">
            <div class="side-card-label">
                Time Points
            </div>

            <div class="side-card-value">
                {date_count:,}
            </div>

            <div class="side-card-note">
                Distinct observations in the time series
            </div>
        </div>

        <div class="side-card">
            <div class="side-card-label">
                Analytical Fields
            </div>

            <div class="side-card-value">
                {len(covid.columns):,}
            </div>

            <div class="side-card-note">
                Country-level measures and derived indicators
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="side-section">Project Positioning</div>',
        unsafe_allow_html=True,
    )

    st.caption(
        "This dashboard describes patterns in the available "
        "dataset. It does not establish medical or causal conclusions."
    )


# Hero section

st.markdown(
    f"""
    <div class="hero">

        <div class="hero-label">
            Global Pandemic Analytics
        </div>

        <div class="hero-title">
            COVID-19 Global Intelligence
        </div>

        <div class="hero-description">
            An interactive analytical view of reported COVID-19
            data across geography, time, regional patterns,
            testing relationships and a calculated impact framework.
        </div>

        <div class="hero-meta">
            <div class="hero-pill">
                Country-Level Analysis
            </div>

            <div class="hero-pill">
                Regional Comparison
            </div>

            <div class="hero-pill">
                Time-Series Analysis
            </div>

            <div class="hero-pill">
                Geographic Analysis
            </div>

            <div class="hero-pill">
                Interactive Exploration
            </div>
        </div>

        <div class="coverage-box">

            <div class="coverage-label">
                Data Coverage
            </div>

            <div class="coverage-value">
                {coverage_range}
            </div>

            <div class="coverage-note">
                This dashboard reflects the available observations
                in the source dataset during this period and is not
                intended to represent a complete historical record
                of the COVID-19 pandemic.
            </div>

        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# Why this dashboard was built

st.markdown(
    '<div class="section-title">Why This Dashboard Was Built</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="section-description">
        Raw pandemic records contain large volumes of numbers,
        but analysis becomes more useful when those numbers can
        be compared across time, geography and normalized indicators.
        This project turns the available records into an interactive
        analytical story that can be explored from multiple perspectives.
    </div>
    """,
    unsafe_allow_html=True,
)

purpose1, purpose2, purpose3 = st.columns(
    3,
    gap="large",
)

with purpose1:
    st.markdown(
        """
        <div class="purpose-card">

            <div class="purpose-number">
                01 · UNDERSTAND
            </div>

            <div class="purpose-title">
                Understand the reported burden
            </div>

            <div class="purpose-text">
                Start with the dataset snapshot and timeline
                to understand the reported cases, deaths,
                recoveries and active-case burden represented
                in the available records.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

with purpose2:
    st.markdown(
        """
        <div class="purpose-card">

            <div class="purpose-number">
                02 · COMPARE
            </div>

            <div class="purpose-title">
                Compare countries and regions
            </div>

            <div class="purpose-text">
                Geographic maps, regional aggregation and
                country rankings provide different ways to
                compare the reported metrics represented in
                the analytical dataset.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

with purpose3:
    st.markdown(
        """
        <div class="purpose-card">

            <div class="purpose-number">
                03 · INTERPRET
            </div>

            <div class="purpose-title">
                Move from numbers to analytical insight
            </div>

            <div class="purpose-text">
                Normalized indicators, relationship analysis,
                impact categories and explanatory notes add
                context to the patterns visible in the charts.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# How the analysis works

st.markdown(
    '<div class="section-title">How the Analysis Works</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="section-description">
        The dashboard follows a transparent analytical workflow:
        prepare the data, summarize the reported burden, compare
        geographic groups, examine relationships and interpret
        the resulting patterns.
    </div>
    """,
    unsafe_allow_html=True,
)

method_columns = st.columns(
    5,
    gap="medium",
)

methods = [
    (
        "01",
        "Prepare",
        "Load and organize country-level and time-series records."
    ),
    (
        "02",
        "Summarize",
        "Build high-level metrics for the available dataset."
    ),
    (
        "03",
        "Compare",
        "Compare countries and regions using reported measures."
    ),
    (
        "04",
        "Normalize",
        "Use per-million measures where population differences matter."
    ),
    (
        "05",
        "Interpret",
        "Describe visible patterns without turning association into causation."
    ),
]

for column, method in zip(method_columns, methods):
    with column:
        st.markdown(
            f"""
            <div class="method-card">

                <div class="method-number">
                    {method[0]}
                </div>

                <div class="method-title">
                    {method[1]}
                </div>

                <div class="method-text">
                    {method[2]}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


# Global snapshot

st.markdown(
    '<div class="section-title">Global Snapshot</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="section-description">
        A high-level view of the reported country-level burden
        represented in the available analytical dataset.
    </div>
    """,
    unsafe_allow_html=True,
)

kpi1, kpi2, kpi3, kpi4 = st.columns(
    4,
    gap="medium",
)

with kpi1:
    st.markdown(
        f"""
        <div class="kpi">

            <div class="kpi-label">
                Countries / Regions
            </div>

            <div class="kpi-value">
                {total_countries:,}
            </div>

            <div class="kpi-note">
                Geographic records represented
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi2:
    st.markdown(
        f"""
        <div class="kpi">

            <div class="kpi-label">
                Reported Cases
            </div>

            <div class="kpi-value">
                {total_cases:,.0f}
            </div>

            <div class="kpi-note">
                Cumulative country-level total
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi3:
    st.markdown(
        f"""
        <div class="kpi">

            <div class="kpi-label">
                Reported Deaths
            </div>

            <div class="kpi-value">
                {total_deaths:,.0f}
            </div>

            <div class="kpi-note">
                Cumulative country-level total
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi4:
    st.markdown(
        f"""
        <div class="kpi">

            <div class="kpi-label">
                Reported Active Cases
            </div>

            <div class="kpi-value">
                {total_active:,.0f}
            </div>

            <div class="kpi-note">
                Active-case burden represented
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# Pandemic evolution

if "Date" in time_series.columns:

    st.markdown(
        '<div class="section-title">Pandemic Evolution</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-description">
            The available time series shows how reported cumulative
            cases, deaths, recoveries and active cases changed
            across the observation period.
        </div>
        """,
        unsafe_allow_html=True,
    )

    global_daily = (
        time_series
        .dropna(subset=["Date"])
        .groupby("Date", as_index=False)
        .agg(
            Confirmed=("Confirmed", "sum"),
            Deaths=("Deaths", "sum"),
            Recovered=("Recovered", "sum"),
            Active=("Active", "sum"),
        )
        .sort_values("Date")
    )

    evolution_data = global_daily.melt(
        id_vars="Date",
        value_vars=[
            "Confirmed",
            "Deaths",
            "Recovered",
        ],
        var_name="Metric",
        value_name="Reported Count",
    )

    fig_evolution = px.area(
        evolution_data,
        x="Date",
        y="Reported Count",
        color="Metric",
        color_discrete_map={
            "Confirmed": PRIMARY,
            "Deaths": DANGER,
            "Recovered": SECONDARY,
        },
    )

    fig_evolution.update_traces(
        line=dict(width=2.5),
        hovertemplate=(
            "<b>%{fullData.name}</b><br>"
            "Date: %{x|%d %b %Y}<br>"
            "Reported Count: %{y:,.0f}"
            "<extra></extra>"
        ),
    )

    fig_evolution.update_layout(
        template="plotly_dark",
        height=470,
        margin=dict(
            l=15,
            r=15,
            t=25,
            b=15,
        ),
        hovermode="x unified",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(
            orientation="h",
            y=1.08,
            x=0,
        ),
        xaxis=dict(
            showgrid=False,
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=GRID,
        ),
    )

    st.plotly_chart(
        fig_evolution,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "scrollZoom": False,
        },
    )

    evolution_note1, evolution_note2, evolution_note3 = st.columns(
        3,
        gap="medium",
    )

    with evolution_note1:
        st.markdown(
            """
            <div class="explain-card">

                <div class="explain-label">
                    What it shows
                </div>

                <div class="explain-title">
                    Cumulative trajectory
                </div>

                <div class="explain-text">
                    The chart follows the cumulative reported
                    trajectory across the available dates.
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with evolution_note2:
        st.markdown(
            """
            <div class="explain-card">

                <div class="explain-label">
                    Why it matters
                </div>

                <div class="explain-title">
                    Reveals changes over time
                </div>

                <div class="explain-text">
                    A time-series view adds temporal context
                    that a single country snapshot cannot provide.
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with evolution_note3:
        st.markdown(
            """
            <div class="explain-card">

                <div class="explain-label">
                    Interpretation
                </div>

                <div class="explain-title">
                    Descriptive, not causal
                </div>

                <div class="explain-text">
                    Changes in the reported series describe the
                    dataset and should not be treated as causal
                    explanations for transmission patterns.
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


# Global geographic footprint

st.markdown(
    '<div class="section-title">Global Pandemic Footprint</div>',
    unsafe_allow_html=True,
)

map_labels = {
    "TotalCases": "Reported Cases",
    "TotalDeaths": "Reported Deaths",
    "TotalRecovered": "Reported Recoveries",
    "ActiveCases": "Active Cases",
}

map_description = map_labels[map_metric].lower()

st.markdown(
    f"""
    <div class="section-description">
        Geographic distribution of <b>{map_description}</b>
        across the country-level records.
    </div>
    """,
    unsafe_allow_html=True,
)
map_hover = {
    "TotalCases": ":,.0f",
    "TotalDeaths": ":,.0f",
    "TotalRecovered": ":,.0f",
    "ActiveCases": ":,.0f",
}

fig_map = px.choropleth(
    covid,
    locations="Country",
    locationmode="country names",
    color=map_metric,
    hover_name="Country",
    hover_data={
        "TotalCases": ":,.0f",
        "TotalDeaths": ":,.0f",
        "TotalRecovered": ":,.0f",
        "ActiveCases": ":,.0f",
        **(
            {"COVID_Impact_Score": ":.2f"}
            if "COVID_Impact_Score" in covid.columns
            else {}
        ),
    },
    color_continuous_scale="Turbo",
    labels=map_labels,
)

fig_map.update_layout(
    template="plotly_dark",
    height=650,
    margin=dict(
        l=0,
        r=0,
        t=15,
        b=0,
    ),
    coloraxis_colorbar=dict(
        title=map_labels[map_metric],
        thickness=12,
        len=0.65,
    ),
    geo=dict(
        projection_type="natural earth",
        showframe=False,
        showcountries=True,
        countrycolor="rgba(255,255,255,0.14)",
        showcoastlines=True,
        coastlinecolor="rgba(255,255,255,0.20)",
        showland=True,
        landcolor="#0B0F17",
        showocean=True,
        oceancolor="#050811",
        bgcolor="rgba(0,0,0,0)",
    ),
)

st.plotly_chart(
    fig_map,
    use_container_width=True,
    config={
        "displayModeBar": False,
        "scrollZoom": False,
    },
)

st.markdown(
    f"""
    <div class="explain-card">

        <div class="explain-label">
            Map interpretation
        </div>

        <div class="explain-title">
            {map_labels[map_metric]} by country / region
        </div>

        <div class="explain-text">
            Darker-to-brighter intensity represents higher values
            of the selected reported metric. Use the sidebar to
            switch between cases, deaths, recoveries and active cases.
            The map describes the values represented in the dataset;
            it does not imply that differences are caused by any
            single factor.
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# Impact intelligence

if {
    "Impact_Category",
    "COVID_Impact_Score",
}.issubset(covid.columns):

    st.markdown(
        '<div class="section-title">Impact Intelligence</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-description">
            A country-level view of the project's calculated
            impact framework. The score is an analytical indicator
            created for comparative exploration and should not be
            interpreted as an official measure of pandemic severity.
        </div>
        """,
        unsafe_allow_html=True,
    )

    impact_col, impact_rank_col = st.columns(
        [0.9, 1.1],
        gap="large",
    )

    impact_data = (
        covid["Impact_Category"]
        .value_counts()
        .rename_axis("Impact_Category")
        .reset_index(name="Number_of_Countries")
    )

    impact_order = [
        "Low",
        "Moderate",
        "High",
        "Critical",
        "Insufficient Data",
    ]

    impact_data["Impact_Category"] = pd.Categorical(
        impact_data["Impact_Category"],
        categories=impact_order,
        ordered=True,
    )

    impact_data = (
        impact_data
        .sort_values("Impact_Category")
    )

    with impact_col:

        fig_impact = px.pie(
            impact_data,
            names="Impact_Category",
            values="Number_of_Countries",
            hole=0.66,
            color="Impact_Category",
            color_discrete_map=IMPACT_COLORS,
        )

        fig_impact.update_traces(
            textposition="outside",
            textinfo="percent",
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Countries / regions: %{value:,}<br>"
                "Share: %{percent}"
                "<extra></extra>"
            ),
        )

        fig_impact.update_layout(
            template="plotly_dark",
            height=470,
            margin=dict(
                l=10,
                r=10,
                t=20,
                b=20,
            ),
            showlegend=True,
            legend=dict(
                orientation="h",
                y=-0.05,
                x=0.05,
            ),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
        )

        st.plotly_chart(
            fig_impact,
            use_container_width=True,
            config={"displayModeBar": False},
        )

    with impact_rank_col:

        impact_ranking = (
            covid[
                covid["COVID_Impact_Score"].notna()
            ]
            .sort_values(
                "COVID_Impact_Score",
                ascending=False,
            )
            .head(10)
            .sort_values(
                "COVID_Impact_Score",
            )
        )

        fig_impact_rank = px.bar(
            impact_ranking,
            x="COVID_Impact_Score",
            y="Country",
            orientation="h",
            text="COVID_Impact_Score",
            color="COVID_Impact_Score",
            color_continuous_scale="Turbo",
        )

        fig_impact_rank.update_traces(
            texttemplate="%{text:.1f}",
            textposition="outside",
            marker_line_width=0,
        )

        fig_impact_rank.update_layout(
            template="plotly_dark",
            height=470,
            coloraxis_showscale=False,
            margin=dict(
                l=10,
                r=55,
                t=20,
                b=20,
            ),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(
                title="Calculated Impact Score",
                showgrid=True,
                gridcolor=GRID,
            ),
            yaxis=dict(
                title="",
                showgrid=False,
            ),
        )

        st.plotly_chart(
            fig_impact_rank,
            use_container_width=True,
            config={"displayModeBar": False},
        )

    impact_info1, impact_info2 = st.columns(
        2,
        gap="large",
    )

    with impact_info1:
        st.markdown(
            """
            <div class="explain-card">

                <div class="explain-label">
                    Impact distribution
                </div>

                <div class="explain-title">
                    How the calculated categories are distributed
                </div>

                <div class="explain-text">
                    The donut chart shows the number of country-level
                    records assigned to each category under the
                    project's calculated impact framework.
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with impact_info2:
        st.markdown(
            """
            <div class="explain-card">

                <div class="explain-label">
                    Impact ranking
                </div>

                <div class="explain-title">
                    Comparative analytical indicator
                </div>

                <div class="explain-text">
                    The ranking highlights the highest calculated
                    scores in the dataset. It should be used as a
                    comparative analytical indicator rather than as
                    an official severity ranking.
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


# Regional intelligence

if "Continent" in covid.columns:

    st.markdown(
        '<div class="section-title">Regional Intelligence</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-description">
            Regional aggregation provides another analytical layer:
            instead of examining individual countries, we compare
            broader geographic groups using reported cases, deaths,
            recoveries, active cases and country counts.
        </div>
        """,
        unsafe_allow_html=True,
    )

    regional_data = (
        covid
        .groupby(
            "Continent",
            as_index=False,
        )
        .agg(
            Cases=("TotalCases", "sum"),
            Deaths=("TotalDeaths", "sum"),
            Recovered=("TotalRecovered", "sum"),
            Active=("ActiveCases", "sum"),
            Countries=("Country", "nunique"),
        )
        .dropna(
            subset=["Continent"]
        )
    )

    regional_col1, regional_col2 = st.columns(
        2,
        gap="large",
    )

    with regional_col1:

        regional_plot = (
            regional_data
            .sort_values(
                "Cases",
                ascending=True,
            )
        )

        fig_region = go.Figure()

        fig_region.add_trace(
            go.Bar(
                x=regional_plot["Cases"],
                y=regional_plot["Continent"],
                orientation="h",
                marker=dict(
                    color=regional_plot["Cases"],
                    colorscale="Turbo",
                    line=dict(width=0),
                ),
                text=regional_plot["Cases"],
                texttemplate="%{text:.3s}",
                textposition="outside",
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Reported Cases: %{x:,.0f}"
                    "<extra></extra>"
                ),
            )
        )

        fig_region.update_layout(
            template="plotly_dark",
            height=460,
            coloraxis_showscale=False,
            margin=dict(
                l=10,
                r=55,
                t=20,
                b=20,
            ),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(
                title="Reported Cases",
                showgrid=True,
                gridcolor=GRID,
            ),
            yaxis=dict(
                title="",
                showgrid=False,
            ),
        )

        st.plotly_chart(
            fig_region,
            use_container_width=True,
            config={"displayModeBar": False},
        )

    with regional_col2:

        fig_bubble = px.scatter(
            regional_data,
            x="Cases",
            y="Deaths",
            size="Countries",
            color="Continent",
            hover_name="Continent",
            hover_data={
                "Cases": ":,.0f",
                "Deaths": ":,.0f",
                "Recovered": ":,.0f",
                "Active": ":,.0f",
                "Countries": True,
            },
            size_max=65,
            labels={
                "Cases": "Reported Cases",
                "Deaths": "Reported Deaths",
                "Countries": "Countries",
            },
        )

        fig_bubble.update_traces(
            marker=dict(
                opacity=0.82,
                line=dict(
                    width=1,
                    color="rgba(255,255,255,0.18)",
                ),
            )
        )

        fig_bubble.update_layout(
            template="plotly_dark",
            height=460,
            margin=dict(
                l=20,
                r=20,
                t=20,
                b=20,
            ),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(
                title="Reported Cases",
                showgrid=True,
                gridcolor=GRID,
            ),
            yaxis=dict(
                title="Reported Deaths",
                showgrid=True,
                gridcolor=GRID,
            ),
        )

        st.plotly_chart(
            fig_bubble,
            use_container_width=True,
            config={"displayModeBar": False},
        )

    region_note1, region_note2 = st.columns(
        2,
        gap="large",
    )

    with region_note1:
        st.markdown(
            """
            <div class="explain-card">

                <div class="explain-label">
                    Regional burden
                </div>

                <div class="explain-title">
                    Compare geographic concentration
                </div>

                <div class="explain-text">
                    The bar chart compares the total reported case
                    burden represented by each geographic region.
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with region_note2:
        st.markdown(
            """
            <div class="explain-card">

                <div class="explain-label">
                    Regional relationship
                </div>

                <div class="explain-title">
                    Cases, deaths and representation
                </div>

                <div class="explain-text">
                    Bubble size represents the number of countries
                    or regions contributing to each geographic group,
                    while position compares reported cases and deaths.
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


# Testing intelligence

if {
    "Calculated_Tests_per_1M",
    "Calculated_Cases_per_1M",
}.issubset(covid.columns):

    st.markdown(
        '<div class="section-title">Testing Intelligence</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-description">
            A relationship analysis comparing testing intensity
            with reported cases per million across the available
            country-level records.
        </div>
        """,
        unsafe_allow_html=True,
    )

    testing_columns = [
        "Country",
        "Calculated_Tests_per_1M",
        "Calculated_Cases_per_1M",
    ]

    if "TotalCases" in covid.columns:
        testing_columns.append("TotalCases")

    if "COVID_Impact_Score" in covid.columns:
        testing_columns.append("COVID_Impact_Score")

    testing_data = (
        covid[testing_columns]
        .dropna(
            subset=[
                "Calculated_Tests_per_1M",
                "Calculated_Cases_per_1M",
            ]
        )
        .copy()
    )

    correlation = (
        testing_data[
            [
                "Calculated_Tests_per_1M",
                "Calculated_Cases_per_1M",
            ]
        ]
        .corr()
        .iloc[0, 1]
    )

    testing_col1, testing_col2 = st.columns(
        [1.45, 0.55],
        gap="large",
    )

    with testing_col1:

        scatter_kwargs = {
            "x": "Calculated_Tests_per_1M",
            "y": "Calculated_Cases_per_1M",
            "hover_name": "Country",
            "labels": {
                "Calculated_Tests_per_1M": "Tests per Million",
                "Calculated_Cases_per_1M": "Reported Cases per Million",
            },
        }

        if "TotalCases" in testing_data.columns:
            scatter_kwargs["size"] = "TotalCases"

        if "COVID_Impact_Score" in testing_data.columns:
            scatter_kwargs["color"] = "COVID_Impact_Score"
            scatter_kwargs["color_continuous_scale"] = "Turbo"

        fig_testing = px.scatter(
            testing_data,
            **scatter_kwargs,
        )

        fig_testing.update_traces(
            marker=dict(
                opacity=0.74,
                line=dict(
                    width=0.6,
                    color="rgba(255,255,255,0.18)",
                ),
            )
        )

        fig_testing.add_annotation(
            x=0.98,
            y=0.96,
            xref="paper",
            yref="paper",
            text=f"<b>Correlation: {correlation:.2f}</b>",
            showarrow=False,
            font=dict(
                size=13,
                color="#E2E8F0",
            ),
            bgcolor="rgba(15,23,42,0.78)",
            bordercolor="rgba(255,255,255,0.10)",
            borderwidth=1,
            borderpad=8,
        )

        fig_testing.update_layout(
            template="plotly_dark",
            height=510,
            margin=dict(
                l=20,
                r=20,
                t=20,
                b=20,
            ),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(
                showgrid=True,
                gridcolor=GRID,
                title="Tests per Million",
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor=GRID,
                title="Reported Cases per Million",
            ),
        )

        st.plotly_chart(
            fig_testing,
            use_container_width=True,
            config={"displayModeBar": False},
        )

    with testing_col2:

        if correlation >= 0.7:
            relationship_text = "Strong positive association"
        elif correlation >= 0.4:
            relationship_text = "Moderate positive association"
        elif correlation >= 0.1:
            relationship_text = "Weak positive association"
        elif correlation <= -0.7:
            relationship_text = "Strong negative association"
        elif correlation <= -0.4:
            relationship_text = "Moderate negative association"
        elif correlation <= -0.1:
            relationship_text = "Weak negative association"
        else:
            relationship_text = "Very weak linear association"

        st.markdown(
            f"""
            <div class="analysis-card">

                <div class="analysis-label">
                    Pearson Correlation
                </div>

                <div class="analysis-value">
                    {correlation:.2f}
                </div>

                <div class="analysis-note">
                    Testing rate versus reported case rate.
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        st.markdown(
            f"""
            <div class="analysis-card">

                <div class="analysis-label">
                    Observed Relationship
                </div>

                <div class="analysis-value"
                     style="font-size:1.05rem;">
                    {relationship_text}
                </div>

                <div class="analysis-note">
                    Correlation describes linear association
                    and does not establish causation.
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


# Pandemic burden matrix

if {
    "Calculated_Cases_per_1M",
    "TotalDeaths",
    "COVID_Impact_Score",
}.issubset(covid.columns):

    st.markdown(
        '<div class="section-title">Pandemic Burden Matrix</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-description">
            A normalized comparison of reported cases and deaths
            per million. The visualization highlights different
            combinations of case burden and reported death burden.
        </div>
        """,
        unsafe_allow_html=True,
    )

    matrix_data = covid.copy()

    if "Population" in matrix_data.columns:
        matrix_data["Calculated_Deaths_per_1M"] = (
            matrix_data["TotalDeaths"]
            / matrix_data["Population"].replace(0, np.nan)
            * 1_000_000
        )
    elif "Calculated_Deaths_per_1M" not in matrix_data.columns:
        matrix_data["Calculated_Deaths_per_1M"] = (
            matrix_data["TotalDeaths"]
        )

    matrix_data = matrix_data.dropna(
        subset=[
            "Calculated_Cases_per_1M",
            "Calculated_Deaths_per_1M",
            "COVID_Impact_Score",
        ]
    )

    if len(matrix_data) > 0:

        size_column = (
            "Population"
            if "Population" in matrix_data.columns
            else "TotalCases"
        )

        fig_matrix = px.scatter(
            matrix_data,
            x="Calculated_Cases_per_1M",
            y="Calculated_Deaths_per_1M",
            size=size_column,
            color="COVID_Impact_Score",
            hover_name="Country",
            hover_data={
                "Calculated_Cases_per_1M": ":,.1f",
                "Calculated_Deaths_per_1M": ":,.1f",
                "COVID_Impact_Score": ":.2f",
                "TotalCases": ":,.0f",
                "TotalDeaths": ":,.0f",
            },
            color_continuous_scale="Plasma",
            size_max=42,
            labels={
                "Calculated_Cases_per_1M": "Reported Cases per Million",
                "Calculated_Deaths_per_1M": "Reported Deaths per Million",
                "COVID_Impact_Score": "Calculated Impact Score",
            },
        )

        median_cases = matrix_data[
            "Calculated_Cases_per_1M"
        ].median()

        median_deaths = matrix_data[
            "Calculated_Deaths_per_1M"
        ].median()

        fig_matrix.add_vline(
            x=median_cases,
            line_width=1,
            line_dash="dot",
            line_color="rgba(255,255,255,0.30)",
        )

        fig_matrix.add_hline(
            y=median_deaths,
            line_width=1,
            line_dash="dot",
            line_color="rgba(255,255,255,0.30)",
        )

        fig_matrix.update_traces(
            marker=dict(
                opacity=0.74,
                line=dict(
                    width=0.7,
                    color="rgba(255,255,255,0.18)",
                ),
            )
        )

        fig_matrix.update_layout(
            template="plotly_dark",
            height=570,
            margin=dict(
                l=20,
                r=20,
                t=20,
                b=20,
            ),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(
                showgrid=True,
                gridcolor=GRID,
                title="Reported Cases per Million",
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor=GRID,
                title="Reported Deaths per Million",
            ),
        )

        st.plotly_chart(
            fig_matrix,
            use_container_width=True,
            config={"displayModeBar": False},
        )

        matrix_note1, matrix_note2 = st.columns(
            2,
            gap="large",
        )

        with matrix_note1:
            st.markdown(
                """
                <div class="explain-card">

                    <div class="explain-label">
                        Why normalize?
                    </div>

                    <div class="explain-title">
                        Population differences matter
                    </div>

                    <div class="explain-text">
                        Per-million measures make country comparisons
                        more meaningful when population sizes differ
                        substantially.
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

        with matrix_note2:
            st.markdown(
                """
                <div class="explain-card">

                    <div class="explain-label">
                        How to read
                    </div>

                    <div class="explain-title">
                        Relative position matters
                    </div>

                    <div class="explain-text">
                        Countries farther to the right have higher
                        reported cases per million, while countries
                        higher on the chart have higher reported deaths
                        per million.
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )


# Country intelligence

st.markdown(
    '<div class="section-title">Country Intelligence</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="section-description">
        The ranking dynamically changes according to the selected
        analytical metric in the sidebar.
    </div>
    """,
    unsafe_allow_html=True,
)

ranking_labels = {
    "TotalCases": "Reported Cases",
    "TotalDeaths": "Reported Deaths",
    "TotalRecovered": "Reported Recoveries",
    "ActiveCases": "Active Cases",
    "COVID_Impact_Score": "Calculated Impact Score",
}

ranking_label = ranking_labels[ranking_metric]

ranking_data = (
    covid
    .dropna(
        subset=[ranking_metric]
    )
    .sort_values(
        ranking_metric,
        ascending=False,
    )
    .head(10)
    .sort_values(
        ranking_metric,
        ascending=True,
    )
)

fig_ranking = go.Figure()

fig_ranking.add_trace(
    go.Bar(
        x=ranking_data[ranking_metric],
        y=ranking_data["Country"],
        orientation="h",
        marker=dict(
            color=ranking_data[ranking_metric],
            colorscale="Turbo",
            line=dict(width=0),
        ),
        text=ranking_data[ranking_metric],
        texttemplate=(
            "%{text:.2f}"
            if ranking_metric == "COVID_Impact_Score"
            else "%{text:.3s}"
        ),
        textposition="outside",
        hovertemplate=(
            "<b>%{y}</b><br>"
            f"{ranking_label}: "
            "%{x:,.2f}"
            "<extra></extra>"
        ),
    )
)

fig_ranking.update_layout(
    template="plotly_dark",
    height=510,
    margin=dict(
        l=10,
        r=65,
        t=20,
        b=20,
    ),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(
        title=ranking_label,
        showgrid=True,
        gridcolor=GRID,
    ),
    yaxis=dict(
        title="",
        showgrid=False,
    ),
)

st.plotly_chart(
    fig_ranking,
    use_container_width=True,
    config={"displayModeBar": False},
)

st.markdown(
    f"""
    <div class="explain-card">

        <div class="explain-label">
            Current ranking
        </div>

        <div class="explain-title">
            Top countries by {ranking_label.lower()}
        </div>

        <div class="explain-text">
            This ranking identifies the highest values for the
            selected metric within the available country-level
            dataset. Rankings describe the recorded values and
            should not be interpreted as causal explanations.
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# Key analytical findings

critical_count = 0

if "Impact_Category" in covid.columns:
    critical_count = int(
        covid["Impact_Category"]
        .eq("Critical")
        .sum()
    )

highest_impact_country = "Unavailable"

if (
    "COVID_Impact_Score" in covid.columns
    and covid["COVID_Impact_Score"].notna().any()
):
    highest_impact_country = (
        covid.loc[
            covid["COVID_Impact_Score"].idxmax(),
            "Country",
        ]
    )

highest_case_country = "Unavailable"

if (
    "TotalCases" in covid.columns
    and covid["TotalCases"].notna().any()
):
    highest_case_country = (
        covid.loc[
            covid["TotalCases"].idxmax(),
            "Country",
        ]
    )

highest_death_country = "Unavailable"

if (
    "TotalDeaths" in covid.columns
    and covid["TotalDeaths"].notna().any()
):
    highest_death_country = (
        covid.loc[
            covid["TotalDeaths"].idxmax(),
            "Country",
        ]
    )


st.markdown(
    '<div class="section-title">Key Analytical Findings</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="section-description">
        Selected observations generated directly from the available
        analytical dataset.
    </div>
    """,
    unsafe_allow_html=True,
)

finding1, finding2, finding3 = st.columns(
    3,
    gap="large",
)

with finding1:
    st.markdown(
        f"""
        <div class="finding-card">

            <div class="finding-title">
                Calculated impact concentration
            </div>

            <div class="finding-text">
                {critical_count} country-level records fall into
                the Critical category under the project's calculated
                impact framework.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

with finding2:
    st.markdown(
        f"""
        <div class="finding-card">

            <div class="finding-title">
                Highest calculated impact score
            </div>

            <div class="finding-text">
                {highest_impact_country} records the highest
                calculated impact score in the available
                country-level dataset.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

with finding3:
    st.markdown(
        f"""
        <div class="finding-card">

            <div class="finding-title">
                Highest reported case count
            </div>

            <div class="finding-text">
                {highest_case_country} has the highest reported
                cumulative case count among the country-level
                records represented in the dataset.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# Questions this dashboard answers

st.markdown(
    '<div class="section-title">What Questions Does the Dashboard Answer?</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="section-description">
        The project is designed around practical analytical questions
        rather than simply displaying charts.
    </div>
    """,
    unsafe_allow_html=True,
)

question1, question2, question3 = st.columns(
    3,
    gap="large",
)

with question1:
    st.markdown(
        """
        <div class="question-card">

            <div class="question-title">
                How did the reported burden evolve?
            </div>

            <div class="question-answer">
                Use the pandemic evolution chart to examine
                changes across the available observation period.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

with question2:
    st.markdown(
        """
        <div class="question-card">

            <div class="question-title">
                Which geographic groups differ?
            </div>

            <div class="question-answer">
                Use the map, regional analysis and country rankings
                to compare the reported metrics.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

with question3:
    st.markdown(
        """
        <div class="question-card">

            <div class="question-title">
                How are testing and reported cases related?
            </div>

            <div class="question-answer">
                Use the testing scatter plot and Pearson correlation
                to examine their linear association.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# Interpretation notes

st.markdown(
    '<div class="section-title">Interpretation Notes</div>',
    unsafe_allow_html=True,
)

note1, note2 = st.columns(
    2,
    gap="large",
)

with note1:
    st.markdown(
        """
        <div class="explain-card">

            <div class="explain-label">
                Data limitation
            </div>

            <div class="explain-title">
                Available records define the scope
            </div>

            <div class="explain-text">
                The dashboard reflects the records and observation
                period available in the source dataset. It should
                not be interpreted as a complete historical record
                of the COVID-19 pandemic.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

with note2:
    st.markdown(
        """
        <div class="explain-card">

            <div class="explain-label">
                Analytical limitation
            </div>

            <div class="explain-title">
                Association is not causation
            </div>

            <div class="explain-text">
                Relationships shown by correlation or visual patterns
                describe the available data. They do not establish
                that one variable caused another.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# Final data note

st.markdown(
    f"""
    <div class="coverage-box" style="margin-top:3rem;">

        <div class="coverage-label">
            Data note
        </div>

        <div class="coverage-value">
            Observation period: {coverage_range}
        </div>

        <div class="coverage-note">
            Results reflect the available records in the source
            dataset during this period. Reported figures may not
            represent complete historical pandemic totals.
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# Footer

st.markdown(
    """
    <div class="footer">
        COVID-19 Global Intelligence
        · Interactive Data Analytics Project
    </div>
    """,
    unsafe_allow_html=True,
)