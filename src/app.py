import sys
from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.express as px

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data_loader import load_data
from services.risk_engine import score_shipments, dashboard_metrics
from services.route_optimizer import rank_routes
from services.fleet_optimizer import idle_assets, recommend_redeployment
from services.cold_chain import classify_excursions, cold_chain_summary
from services.ai_copilot import watsonx_answer

st.set_page_config(
    page_title="RouteGuard AI",
    page_icon="🚚",
    layout="wide",
)

st.title("🚚 RouteGuard AI")
st.caption("Supply Chain Disruption & Fleet Utilisation Optimizer")

shipments, fleet, routes, disruptions, cold_chain = load_data()
scored = score_shipments(shipments, disruptions)
metrics = dashboard_metrics(scored)
cold_summary, cold_checked = cold_chain_summary(cold_chain)

with st.sidebar:
    st.header("Scenario Controls")
    selected_priority = st.multiselect(
        "Shipment priority",
        options=["Standard", "Priority", "Critical"],
        default=["Standard", "Priority", "Critical"],
    )
    min_risk = st.slider("Minimum risk score", 0, 100, 0)
    st.divider()
    st.info(
        "All included datasets are synthetic. "
        "Use this prototype for operational decision support, not autonomous dispatch."
    )

view = scored[
    scored["priority"].isin(selected_priority) & (scored["risk_score"] >= min_risk)
].copy()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Active shipments", metrics["shipments"])
c2.metric("High/Critical risk", metrics["high_risk"])
c3.metric("Affected by disruption", metrics["affected"])
c4.metric("Critical shipments", metrics["critical"])

tabs = st.tabs([
    "📊 Command Dashboard",
    "🧭 Route Optimizer",
    "🚛 Fleet Optimizer",
    "🌡️ Cold Chain",
    "🤖 AI Copilot",
])

with tabs[0]:
    left, right = st.columns([1.5, 1])
    with left:
        st.subheader("Shipment risk prioritisation")
        chart = px.bar(
            view.head(15).sort_values("risk_score"),
            x="risk_score",
            y="shipment_id",
            color="risk_level",
            orientation="h",
            hover_data=["origin", "destination", "risk_reason"],
        )
        chart.update_layout(height=560, xaxis_title="Risk score", yaxis_title="")
        st.plotly_chart(chart, use_container_width=True)

    with right:
        st.subheader("Active disruptions")
        st.dataframe(
            disruptions[["disruption_id", "type", "location", "severity", "affected_route"]],
            use_container_width=True,
            hide_index=True,
        )
        st.subheader("Top interventions")
        st.dataframe(
            view.head(8)[
                ["shipment_id", "origin", "destination", "risk_score", "risk_level", "risk_reason"]
            ],
            use_container_width=True,
            hide_index=True,
        )

with tabs[1]:
    st.subheader("Alternative route recommendation")
    origins = sorted(routes["origin"].unique())
    origin = st.selectbox("Origin", origins, index=0)
    destinations = sorted(routes[routes["origin"] == origin]["destination"].unique())
    destination = st.selectbox("Destination", destinations, index=0)

    ranked = rank_routes(routes, disruptions, origin, destination)
    if ranked.empty:
        st.warning("No route alternatives are available for this origin/destination pair.")
    else:
        best = ranked.iloc[0]
        st.success(
            f"Recommended: {best['route_id']} — optimizer score {best['optimizer_score']:.3f}"
        )
        st.dataframe(
            ranked[
                [
                    "route_id", "distance_km", "estimated_hours", "base_cost_inr",
                    "effective_risk", "optimizer_score", "recommendation"
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )
        st.caption(
            "The optimizer prioritises disruption risk, then travel time and cost. "
            "This is a transparent heuristic suitable for a proof of concept."
        )

with tabs[2]:
    st.subheader("Idle fleet and redeployment")
    idle = idle_assets(fleet)
    st.metric("Available assets below 35% utilisation", len(idle))
    st.dataframe(
        idle[
            ["vehicle_id", "vehicle_type", "capacity_tons", "current_location", "utilization"]
        ],
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Redeployment recommendations")
    redeploy = recommend_redeployment(fleet, scored)
    if redeploy.empty:
        st.info("No idle assets are available.")
    else:
        st.dataframe(
            redeploy[
                [
                    "vehicle_id", "vehicle_type", "current_location", "utilization",
                    "recommended_for", "shipment_risk", "origin", "destination"
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )

with tabs[3]:
    st.subheader("Cold-chain IoT monitoring")
    a, b, c, d = st.columns(4)
    a.metric("Sensor readings", cold_summary["sensor_readings"])
    b.metric("Excursions", cold_summary["excursions"])
    c.metric("Major", cold_summary["major"])
    d.metric("Critical", cold_summary["critical"])

    excursions = cold_checked[cold_checked["outside_range"]].copy()
    if excursions.empty:
        st.success("No temperature excursions detected.")
    else:
        st.dataframe(
            excursions[
                [
                    "sensor_id", "shipment_id", "timestamp", "temperature_c",
                    "allowed_min_c", "allowed_max_c", "deviation_c", "severity"
                ]
            ].head(30),
            use_container_width=True,
            hide_index=True,
        )
        st.warning(
            "Severity is a prototype classification based on deviation from the configured "
            "2–8°C range. Regulatory decisions should use the applicable product-specific SOP."
        )

with tabs[4]:
    st.subheader("Ask RouteGuard AI")
    context = (
        f"Top risky shipments:\n{view.head(10).to_string(index=False)}\n\n"
        f"Disruptions:\n{disruptions.to_string(index=False)}\n\n"
        f"Idle fleet:\n{idle_assets(fleet).head(10).to_string(index=False)}\n\n"
        f"Cold-chain critical excursions:\n"
        f"{cold_checked[cold_checked['severity']=='Critical'].head(10).to_string(index=False)}"
    )

    question = st.text_area(
        "Example: Which shipments need immediate intervention and why?",
        value="Which shipments need immediate intervention and why?",
        height=100,
    )
    if st.button("Analyse with RouteGuard AI", type="primary"):
        with st.spinner("Analysing operational context..."):
            answer, used_watsonx = watsonx_answer(question, context)
        if used_watsonx:
            st.success("Response generated with IBM watsonx.ai")
        else:
            st.info("Local deterministic fallback used. Enable watsonx.ai in .env for the IBM-backed response.")
        st.markdown(answer)

st.divider()
st.caption(
    "RouteGuard AI is a hackathon proof of concept. Recommendations require human validation "
    "before real-world dispatch or regulatory action."
)
