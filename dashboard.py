"""
Streamlit dashboard for Wind Turbine Digital Twin (PoC).
Clean, simple, industrial-style layout.
"""

import time
from datetime import datetime

import streamlit as st
import pandas as pd

import scada_simulator as sim
import dt_engine as dt


# -------------------- PAGE CONFIG (MUST BE FIRST STREAMLIT CALL) --------------------
st.set_page_config(
    page_title="Wind Turbine Digital Twin",
    layout="wide",
)


# -------------------- GLOBAL STYLES --------------------
st.markdown(
    """
    <style>
    /* Background */
    .stApp { background-color: #f7f9fb; }

    /* Section title */
    .section-title {
        font-size: 28px;
        font-weight: 700;
        color: #111827;
        margin-top: 20px;
        margin-bottom: 4px;
    }
    .subtle-line {
        border-top: 1px solid #e5e7eb;
        margin: 12px 0 18px 0;
    }

    /* Big KPI cards */
    .metric-card {
        background-color: #ffffff;
        padding: 22px;
        border-radius: 12px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
    }
    .metric-label {
        font-size: 15px;
        color: #6b7280;
        margin-bottom: 8px;
        font-weight: 500;
    }
    .big-metric {
        font-size: 42px;
        font-weight: 800;
        color: #1f77b4; /* blue */
        margin-bottom: 0;
        line-height: 1.05;
    }

    /* Health cards (already white, subtle shadow) */
    .health-card {
        background-color: white;
        padding: 14px;
        border-radius: 12px;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.05);
        text-align: left;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# -------------------- UI HELPERS --------------------
def section_header(title: str):
    st.markdown(f"<div class='section-title'>{title}</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtle-line'></div>", unsafe_allow_html=True)


def health_card(title: str, value: str, status: str):
    """Render a clean diagnostic health card."""
    color_map = {
        "OK": "#16a34a",        # green
        "WARN": "#f59e0b",      # amber
        "CRITICAL": "#dc2626"   # red
    }
    color = color_map.get(status, "#6b7280")

    st.markdown(
        f"""
        <div class="health-card">
            <div style="font-weight:600; margin-bottom:6px;">{title}</div>
            <div style="font-size:1.1rem; margin-bottom:4px;">{value}</div>
            <div style="color:{color}; font-weight:700;">● {status}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# -------------------- HEADER --------------------
header_col1, header_col2 = st.columns([1, 5])

with header_col1:
    st.image("assets/experiqs_logo.png", width=110)

with header_col2:
    st.markdown(
        """
        <h1 style="color:#1f2937; font-size:44px; margin-bottom:4px;">
            Wind Turbine Digital Twin
        </h1>
        <h3 style="color:#2563eb; font-weight:700; margin-top:0; margin-bottom:6px;">
            Real-Time Asset Monitoring
        </h3>
        <p style="color:#6b7280; margin-top:0;">
            Experiqs | Physics-based performance and health monitoring (PoC)
        </p>
        """,
        unsafe_allow_html=True
    )


# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.markdown("## Controls")
    run_live = st.toggle("Run live simulation", value=True)
    step_once = st.button("Step once (1s)")
    refresh_sec = st.slider("Refresh interval (seconds)", 0.5, 5.0, 1.0)

    st.markdown("---")

    st.markdown("## How this Digital Twin Works")
    st.markdown(
        """
        **Digital Object**
        - Physics-based wind turbine model  
        - Uses first-principles equations  

        **SCADA Signals**
        - Wind speed, RPM, power  
        - Temperatures & vibration  

        **Digital Twin Logic**
        - Computes TSR, Cp, torque  
        - Compares actual vs available wind power  

        **Health Monitoring**
        - Threshold-based diagnostics  
        - Trend-ready structure (PoC → AI next)  
        """
    )


# -------------------- SESSION STATE INIT --------------------
if "state" not in st.session_state:
    st.session_state.state = sim.initialize_state()

if "history" not in st.session_state:
    st.session_state.history = []


# -------------------- STEP SIMULATOR (IF REQUESTED) --------------------
if step_once:
    st.session_state.state = sim.step(st.session_state.state)


# -------------------- COMPUTE CURRENT DT OUTPUTS --------------------
current_scada = st.session_state.state
current_physics = dt.compute_physics(current_scada)
current_health = dt.evaluate_health(current_scada, current_physics)

# Store history for plots
st.session_state.history.append({
    "time": datetime.now(),
    **current_scada,
    **current_physics
})

df_hist = pd.DataFrame(st.session_state.history)


# -------------------- KEY OPERATING METRICS --------------------
section_header("Key Operating Metrics")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Wind Speed</div>
            <div class="big-metric">{current_scada['wind_speed']:.2f} m/s</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Rotor Speed</div>
            <div class="big-metric">{current_scada['rpm']:.2f} RPM</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Power Output</div>
            <div class="big-metric">{current_scada['power']/1000:.0f} kW</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c4:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Power Coefficient (Cp)</div>
            <div class="big-metric">{current_physics['cp']:.3f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# -------------------- HEALTH STATUS --------------------
section_header("Asset Health Status")

h1, h2, h3, h4 = st.columns(4)

with h1:
    health_card(
        title="Generator Temperature",
        value=f"{current_scada['gen_temp']:.1f} °C",
        status=current_health["generator_temp"]
    )

with h2:
    health_card(
        title="Gearbox Temperature",
        value=f"{current_scada['gb_temp']:.1f} °C",
        status=current_health["gearbox_temp"]
    )

with h3:
    health_card(
        title="Vibration (RMS)",
        value=f"{current_scada['vibration']:.2f} mm/s",
        status=current_health["vibration"]
    )

with h4:
    health_card(
        title="Performance",
        value=f"TSR: {current_physics['tsr']:.2f} | Torque: {current_physics['torque']:.0f} Nm",
        status=current_health["performance"]
    )


# -------------------- DIGITAL TWIN CONCEPT IMAGE --------------------
section_header("Digital Twin Concept")

st.image(
    "assets/digital_twin_concept.png",
    caption="Relationship between physical asset, digital shadow, and digital twin",
    use_container_width=True
)


# -------------------- LIVE OPERATING TRENDS --------------------
section_header("Live Operating Trends")

p1, p2 = st.columns(2)

with p1:
    st.write("Wind Speed & Rotor Speed")
    if len(df_hist) > 2:
        st.line_chart(
            df_hist.set_index("time")[["wind_speed", "rpm"]],
            height=320
        )
    else:
        st.info("Waiting for more samples...")

with p2:
    st.write("Power Output vs Available Wind Power")
    if len(df_hist) > 2:
        st.line_chart(
            df_hist.set_index("time")[["power", "p_wind"]],
            height=320
        )
    else:
        st.info("Waiting for more samples...")


# -------------------- LIVE LOOP --------------------
if run_live:
    time.sleep(refresh_sec)
    st.session_state.state = sim.step(st.session_state.state)
    st.rerun()
