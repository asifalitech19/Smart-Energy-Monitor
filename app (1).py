import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import pytz # Library for Timezones

# --- 1. Page Config ---
st.set_page_config(
    page_title="Smart Energy Monitor",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. Load Model ---
@st.cache_resource
def load_model():
    try:
        return joblib.load('ecohome_model.pkl')
    except:
        return None

model = load_model()

# --- 3. CUSTOM CSS (Professional Dark Theme) ---
st.markdown("""
    <style>
    /* MAIN BACKGROUND */
    .stApp { background-color: #0b1120; color: white; }
    
    /* CARDS & METRICS */
    div[data-testid="stMetric"] {
        background-color: #161d33;
        border: 1px solid #2b365e;
        border-radius: 10px;
        padding: 10px;
    }
    div[data-testid="stMetricLabel"] { color: #8b9bb4 !important; }
    div[data-testid="stMetricValue"] { color: #00d4ff !important; }
    
    /* SIDEBAR */
    section[data-testid="stSidebar"] { background-color: #0f152e; border-right: 1px solid #1f294f; }
    
    /* HEADERS */
    h1, h2, h3, p, label, span { color: #e0e6ed !important; font-family: 'Segoe UI', sans-serif; }
    
    /* BUTTONS */
    .stButton > button {
        background: linear-gradient(90deg, #2ECC40, #00d4ff);
        color: white; font-weight: bold; border-radius: 5px; height: 3em; width: 100%;
    }
    
    /* SLIDERS */
    div.stSlider > div[data-baseweb = "slider"] > div > div > div[role="slider"]{
        background-color: #00d4ff; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. HELPER: REAL-TIME CLOCK ---
# Fetch Pakistan Time
tz_PK = pytz.timezone('Asia/Karachi') 
datetime_PK = datetime.now(tz_PK)
current_hour = datetime_PK.hour
current_time_str = datetime_PK.strftime('%I:%M %p') # e.g., 08:30 PM

# --- 5. HELPER: CHART STYLE ---
card_bg_color = "#161d33"
text_color = "white"

def make_chart_transparent(fig):
    fig.update_layout(
        paper_bgcolor=card_bg_color,
        plot_bgcolor=card_bg_color,
        font=dict(color=text_color),
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="#2b365e")
    )
    return fig

# --- 6. SIDEBAR: CONTROLS ---
with st.sidebar:
    st.title("⚡ Smart Energy Monitor")
    st.caption("AI-Powered Optimization System")
    st.markdown("---")

    # Section 1: Weather (AI Input)
    with st.expander("🌦️ Weather Conditions", expanded=True):
        st.write("AI Base Load Prediction")
        
        # Real-time Time Sync
        st.info(f"🕒 System Time: {current_time_str}")
        
        # The slider defaults to 'current_hour' automatically
        hour = st.slider("Hour of Day", 0, 23, current_hour) 
        
        T_out = st.slider("Outside Temp (°C)", 10, 45, 30)
        T1 = st.slider("Indoor Temp (°C)", 16, 35, 26)

    # Section 2: Appliances (Manual Add-on)
    st.subheader("🔌 Household Appliances")
    st.caption("Select active devices to calculate total load.")
    
    # Typical Wattages in Pakistan
    ac_count = st.number_input("Air Conditioner (1.5 Ton)", 0, 5, 1)
    fans = st.slider("Ceiling Fans", 0, 10, 3)
    lights = st.slider("LED Lights", 0, 20, 5)
    
    st.markdown("---")
    st.write("👇 **Heavy Load Appliances**")
    motor_on = st.checkbox("Water Pump (Motor)")
    iron_on = st.checkbox("Iron (Istri)")
    fridge_on = st.checkbox("Refrigerator / Freezer", value=True)
    ups_charging = st.checkbox("UPS Charging Mode")

    # Calculation Logic for Appliances (Watts)
    # AC Inverter ~1200W, Non-Inverter ~1800W. Taking avg 1500W
    appliance_load = (ac_count * 1500) + (fans * 80) + (lights * 20)
    if motor_on: appliance_load += 1000 # 1 HP Motor
    if iron_on: appliance_load += 1000  # Heavy iron
    if fridge_on: appliance_load += 250
    if ups_charging: appliance_load += 300 

    # AI Prediction (Base Load based on weather)
    if model:
        # Dummy inputs matching model shape
        dummy_input = pd.DataFrame([[T1, 50, T1-2, 40, T1+2, 55, T_out, 760, 60, 5, hour]], 
                                  columns=['T1', 'RH_1', 'T2', 'RH_2', 'T3', 'RH_3', 'T_out', 'Press_mm_hg', 'RH_out', 'Windspeed', 'Hour'])
        base_load_ai = model.predict(dummy_input)[0]
    else:
        base_load_ai = 50.0 # Default fallback

    # TOTAL LOAD
    total_load_watts = base_load_ai + appliance_load
    
    st.markdown("---")
    st.info(f"⚡ Live Load: {total_load_watts:.0f} Watts")


# --- 7. MAIN DASHBOARD ---

# Header
c1, c2 = st.columns([3, 1])
with c1:
    st.title("Home Energy Dashboard")
    st.markdown(f"**Current Time:** {current_time_str} (PKT) | Tariff Rate: **Rs. 45/unit**")
with c2:
    st.metric("Total Active Load", f"{total_load_watts/1000:.2f} kW")

st.markdown("<br>", unsafe_allow_html=True)

# --- CALCULATIONS (PKR) ---
unit_rate = 45.0 # PKR
hourly_cost = (total_load_watts / 1000) * unit_rate
monthly_cost = hourly_cost * 6 * 30 # Projection

# --- ROW 1: METRICS ---
col1, col2, col3 = st.columns(3)

# CARD 1: HOURLY COST
with col1:
    st.markdown(f"<div style='background-color: {card_bg_color}; padding: 10px; border-radius: 10px; border: 1px solid #2b365e;'>", unsafe_allow_html=True)
    st.markdown("##### 🕐 Hourly Cost Estimate")
    
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = hourly_cost,
        number = {'prefix': "Rs. ", 'font': {'size': 40, 'color': "#00d4ff"}},
        gauge = {
            'axis': {'range': [0, 500]},
            'bar': {'color': "#00d4ff"},
            'bgcolor': "#0b1120",
            'steps': [
                {'range': [0, 100], 'color': "#2ECC40"},
                {'range': [100, 300], 'color': "#FFDC00"},
                {'range': [300, 500], 'color': "#FF4136"}]
        }
    ))
    make_chart_transparent(fig_gauge)
    fig_gauge.update_layout(height=150, margin=dict(t=0,b=0,l=20,r=20))
    st.plotly_chart(fig_gauge, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# CARD 2: MONTHLY ESTIMATE
with col2:
    st.markdown(f"<div style='background-color: {card_bg_color}; padding: 10px; border-radius: 10px; border: 1px solid #2b365e;'>", unsafe_allow_html=True)
    st.markdown("##### 📅 Monthly Bill Projection")
    
    st.markdown(f"""
    <div style="text-align: center; margin-top: 20px;">
        <h1 style="color: #FFDC00 !important; font-size: 50px;">Rs. {monthly_cost:,.0f}</h1>
        <p style="color: gray;">*Based on avg 6hr peak usage</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# CARD 3: APPLIANCE BREAKDOWN
with col3:
    st.markdown(f"<div style='background-color: {card_bg_color}; padding: 10px; border-radius: 10px; border: 1px solid #2b365e;'>", unsafe_allow_html=True)
    st.markdown("##### 🔌 Load Breakdown")
    
    # Pie Chart Data
    labels = ['ACs', 'Iron/Pump', 'Fridge/UPS', 'Fans/Lights', 'Others (AI)']
    values = [
        ac_count * 1500,
        (1000 if motor_on else 0) + (1000 if iron_on else 0),
        (250 if fridge_on else 0) + (300 if ups_charging else 0),
        (fans * 80) + (lights * 20),
        base_load_ai
    ]
    
    fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5)])
    make_chart_transparent(fig_pie)
    fig_pie.update_layout(height=180, margin=dict(t=0,b=0,l=0,r=0), showlegend=False)
    st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- ROW 2: ANALYSIS & TIPS ---
c_left, c_right = st.columns([2, 1])

with c_left:
    st.markdown(f"<div style='background-color: {card_bg_color}; padding: 15px; border-radius: 10px; border: 1px solid #2b365e;'>", unsafe_allow_html=True)
    st.markdown("##### 📉 Unit Consumption Trend (Last 5 Hours)")
    
    # Fake Trend Data
    hours_x = ['-4 hr', '-3 hr', '-2 hr', '-1 hr', 'Now']
    units_y = [total_load_watts*0.8, total_load_watts*0.9, total_load_watts*1.1, total_load_watts*0.95, total_load_watts]
    
    fig_line = px.area(x=hours_x, y=units_y, color_discrete_sequence=['#00d4ff'])
    make_chart_transparent(fig_line)
    fig_line.update_layout(height=250, yaxis_title="Watts")
    st.plotly_chart(fig_line, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with c_right:
    st.markdown(f"<div style='background-color: {card_bg_color}; padding: 15px; border-radius: 10px; border: 1px solid #2b365e; height: 100%;'>", unsafe_allow_html=True)
    st.markdown("##### 💡 AI Savings Advice")
    
    if iron_on and ac_count > 0:
        st.error("⚠️ Peak Load Alert!")
        st.write("Running Iron (Istri) and AC together drastically increases peak costs.")
    elif motor_on:
        st.warning("💧 Water Pump Active")
        st.write("Ensure the pump is turned off immediately after the tank is full.")
    elif ups_charging:
        st.info("🔋 UPS Charging Mode")
        st.write("UPS charging consumes significant power. Ensure batteries are efficient.")
    else:
        st.success("✅ Optimized Usage")
        st.write("Your system is running efficiently. Keep maintaining this load balance.")
        
    st.markdown("</div>", unsafe_allow_html=True)
