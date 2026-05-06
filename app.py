import streamlit as st
import pandas as pd
import math
from datetime import datetime

st.set_page_config(page_title="Midori Inventory Lab", page_icon="🍵", layout="wide")

# --- CUSTOM CSS ---
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
    st.caption("Average drinks sold per day:")
    
    # Weekday vs Weekend Logic
    wd_sales = st.slider("Typical Weekday (M/W/Th/F)", 5, 100, 20)
    we_sales = st.slider("Typical Weekend (Sa/Su)", 5, 150, 45)
    tue_sales = st.slider("Tuesday (7am-12pm)", 5, 50, 10)

# --- CALCULATION ENGINE ---
# We calculate the NEXT 7 DAYS specifically based on today's day of the week
def get_7_day_demand(daily_avg_wd, daily_avg_we, daily_avg_tue):
    today = datetime.now().weekday() # 0=Mon, 1=Tue...
    total_demand_drinks = 0
    
    for i in range(7):
        day_to_check = (today + i) % 7
        if day_to_check == 1: # Tuesday
            total_demand_drinks += daily_avg_tue
        elif day_to_check >= 5: # Sat/Sun
            total_demand_drinks += daily_avg_we
        else: # M/W/Th/F
            total_demand_drinks += daily_avg_wd
            
    return total_demand_drinks * GRAMS_PER_DRINK * WASTE_BUFFER

# --- DATA PROCESSING ---
inventory_names = ["Strawberry", "Mango", "Blueberry"]
current_stocks = [s_stock, m_stock, b_stock]

st.write(f"### 🗓️ Forecast for: {datetime.now().strftime('%A, %b %d')}")
cols = st.columns(3)

for i, name in enumerate(inventory_names):
    demand_7_days = get_7_day_demand(wd_sales, we_sales, tue_sales)
    stock = current_stocks[i]
    shortfall = max(0, demand_7_days - stock)
    batches = math.ceil(shortfall / YIELD_PER_BATCH)
    
    with cols[i]:
        if shortfall == 0:
            st.success(f"**{name}**")
            st.metric("Status", "SAFE", delta="Fully Stocked")
        else:
            st.error(f"**{name}**")
            st.metric("Shortfall", f"-{int(shortfall)}g", delta=f"Make {batches} batches")
            st.caption(f"Need {int(demand_7_days)}g for next 7 days")

st.divider()
st.info("The AI is now calculating a custom 'Runway' based on your Tuesday half-day and higher weekend volume.")
