import streamlit as st
import pandas as pd
import math
from datetime import datetime

st.set_page_config(page_title="Midori Inventory Lab", page_icon="🍵", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #fcfaf5; }
    .stMetric { border: 1px solid #e6e6e6; padding: 10px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🍵 Midori Puree Runway")
st.subheader("Smart Weekly Inventory Forecast")

# --- CONSTANTS ---
GRAMS_PER_DRINK = 40 
YIELD_PER_BATCH = 535 
WASTE_BUFFER = 1.10
BOTTLE_WEIGHT = 680 

# --- SIDEBAR: SHOP SETTINGS ---
with st.sidebar:
    st.header("📍 Current Shop Stock")
    input_mode = st.radio("Counting Method:", ["By Grams", "By 24oz Bottles"])
    
    if input_mode == "By Grams":
        s_stock = st.number_input("Strawberry (g)", value=1500, step=100)
        m_stock = st.number_input("Mango (g)", value=800, step=100)
        b_stock = st.number_input("Blueberry (g)", value=2000, step=100)
    else:
        s_bot = st.number_input("Strawberry (Bottles)", value=2.0, step=0.5)
        m_bot = st.number_input("Mango (Bottles)", value=1.5, step=0.5)
        b_bot = st.number_input("Blueberry (Bottles)", value=3.0, step=0.5)
        s_stock, m_stock, b_stock = s_bot * BOTTLE_WEIGHT, m_bot * BOTTLE_WEIGHT, b_bot * BOTTLE_WEIGHT

    st.divider()
    st.header("📈 Sales Velocity")
    
    st.subheader("🍓 Strawberry")
    s_wd = st.slider("Strawberry: Weekday", 0, 100, 20)
    s_we = st.slider("Strawberry: Weekend", 0, 150, 40)
    s_tue = st.slider("Strawberry: Tuesday", 0, 50, 10)
    
    st.subheader("🥭 Mango")
    m_wd = st.slider("Mango: Weekday", 0, 100, 15)
    m_we = st.slider("Mango: Weekend", 0, 150, 30)
    m_tue = st.slider("Mango: Tuesday", 0, 50, 8)
    
    st.subheader("🫐 Blueberry")
    b_wd = st.slider("Blueberry: Weekday", 0, 100, 10)
    b_we = st.slider("Blueberry: Weekend", 0, 150, 25)
    b_tue = st.slider("Blueberry: Tuesday", 0, 50, 5)

# --- CALCULATION ENGINE ---
def get_7_day_demand(wd, we, tue):
    today = datetime.now().weekday()
    total_drinks = 0
    for i in range(7):
        day_to_check = (today + i) % 7
        if day_to_check == 1: total_drinks += tue
        elif day_to_check >= 5: total_drinks += we
        else: total_drinks += wd
    return total_drinks * GRAMS_PER_DRINK * WASTE_BUFFER

# --- DATA PROCESSING ---
inventory_data = {
    "Strawberry": {"stock": s_stock, "params": (s_wd, s_we, s_tue)},
    "Mango": {"stock": m_stock, "params": (m_wd, m_we, m_tue)},
    "Blueberry": {"stock": b_stock, "params": (b_wd, b_we, b_tue)}
}

st.write(f"### 🗓️ Forecast for the next 7 days")
cols = st.columns(3)

for i, (name, data) in enumerate(inventory_data.items()):
    demand_7_days = get_7_day_demand(*data['params'])
    stock = data['stock']
    shortfall = max(0, demand_7_days - stock)
    batches = math.ceil(shortfall / YIELD_PER_BATCH)
    
    with cols[i]:
        if shortfall == 0:
            st.success(f"**{name}**")
            st.metric("Status", "SAFE", delta="Fully Stocked")
        else:
            st.error(f"**{name}**")
            st.metric("Shortfall", f"-{int(shortfall)}g", delta=f"Make {batches} batches")
            st.caption(f"Target: {int(demand_7_days)}g")

st.divider()
st.info("Each fruit now has its own unique weekday/weekend velocity. Adjust the sidebar to match your shop's actual trends.")
