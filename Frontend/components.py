from __future__ import annotations 
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
 
RECOMMENDATION_COLORS = {
    "Buy": "#16a34a",
    "Hold": "#ca8a04",
    "Sell": "#dc2626",
}
 
 
def render_header(memo: dict) -> None:
    """Ticker, recommendation badge, conviction, price / target / confidence."""
    rec = memo.get("recommendation", "N/A")
    color = RECOMMENDATION_COLORS.get(rec, "#6b7280")
    current = memo.get("current_price", 0) or 0
    target = memo.get("price_target", 0) or 0
    upside = ((target - current) / current * 100) if current else 0
 
    col1, col2 = st.columns([3, 5])
    with col1:
        st.write("Stock:")
        st.markdown(
            f"""
            <div style="display: flex; flex-direction: column; align-items: flex-start; gap: 0.5rem;">
                <h2 style="margin: 0; padding: 0;">{memo.get('company_name', '—')}</h2>
                <h4 style="margin: 0; padding: 0;">{memo.get('ticker', '—')} | {memo.get('exchange', '—')}</h4>
                <div style="display: inline-block; padding: 15px 25px; border-radius: 999px;
                        background-color: {color}; color: white; font-weight: 600;
                        font-size: 1.1rem; margin-top: 30px;">
                {rec} &middot; {memo.get('conviction', '—')} conviction
            </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

 
    with col2:
        # First row of metrics
        top_left, top_right = st.columns(2)
        top_left.metric("Time Horizon", str(memo.get('time_horizon', '—'))) 
        top_right.metric("Current Price", f"${current:,.2f}")
        
        # Second row of metrics
        bottom_left, bottom_right = st.columns(2)
        bottom_left.metric("Price Target", f"${target:,.2f}", f"{upside:.1f}%")
        
        conf = memo.get('confidence', 0) or 0
        bottom_right.metric("Confidence", f"{conf * 100:.0f}%")
 
 
def render_summary(memo: dict) -> None:
    st.subheader("Executive Summary")
    st.write(memo.get("executive_summary", ""))
 
 
def render_thesis(memo: dict, expanded: bool = False) -> None:
    with st.expander("Investment Thesis", expanded=expanded):
        st.write(memo.get("investment_thesis", ""))
 
 
def render_section_tabs(memo: dict) -> None:
    """Tabbed view of the five narrative sections."""
    labels = ["Fundamentals", "Valuation", "Sentiment", "Technicals", "Risk"]
    keys = [
        "fundamentals_section",
        "valuation_section",
        "sentiment_section",
        "technicals_section",
        "risk_section",
    ]
    tabs = st.tabs(labels)
    for tab, key in zip(tabs, keys):
        with tab:
            st.write(memo.get(key, "No data available."))
 
 
def render_valuation_chart(memo: dict, valuation_models: dict | None = None) -> None:
    """
    Bar chart comparing valuation model outputs vs. the current price.
 
    Pass `valuation_models` explicitly in production (e.g. {"DCF": 158.65, ...});
    the defaults below reflect the figures cited in this sample memo's
    valuation_section narrative.
    """
    st.subheader("Valuation Comparison")
 
    data = valuation_models or {
        "DCF": 158.65,
        "Graham Number": 36.71,
        "Consensus Target": memo.get("price_target", 0),
        "Comps (peer-based)": 412.47,
    }
    data["Current Price"] = memo.get("current_price", 0)
 
    df = pd.DataFrame({"Model": list(data.keys()), "Value": list(data.values())})
    colors = ["#2563eb"] * (len(df) - 1) + ["#111827"]
 
    fig = go.Figure(
        go.Bar(
            x=df["Model"],
            y=df["Value"],
            marker_color=colors,
            text=[f"${v:,.2f}" for v in df["Value"]],
            textposition="outside",
        )
    )
    fig.update_layout(
        yaxis_title="Price ($)",
        showlegend=False,
        margin=dict(t=10, b=10),
        height=380,
    )
    st.plotly_chart(fig, width='content')
 
 
def render_key_risks(memo: dict) -> None:
    risks = memo.get("key_risks_ranked", [])
    if not risks:
        return
    st.subheader("Key Risks (Ranked)")
    for i, risk in enumerate(risks, start=1):
        st.markdown(f"**{i}.** {risk}")
 
 
def render_conflicting_signals(memo: dict) -> None:
    signals = memo.get("conflicting_signals", [])
    if not signals:
        return
    st.subheader("Conflicting Signals")
    for signal in signals:
        st.warning(signal, icon="⚠️")
 
 
def render_data_gaps(memo: dict) -> None:
    gaps = memo.get("data_gaps", [])
    if not gaps:
        return
    st.subheader("Data Gaps")
    for gap in gaps:
        st.info(gap, icon="ℹ️")
 
 
def render_confidence_gauge(memo: dict) -> None:
    conf = (memo.get("confidence", 0) or 0) * 100
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=conf,
            number={"suffix": "%"},
            title={"text": "Model Confidence"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#2563eb"},
                "steps": [
                    {"range": [0, 40], "color": "#fee2e2"},
                    {"range": [40, 70], "color": "#fef9c3"},
                    {"range": [70, 100], "color": "#dcfce7"},
                ],
            },
        )
    )
    fig.update_layout(height=250, margin=dict(t=40, b=10, l=20, r=20))
    st.plotly_chart(fig, width='content')