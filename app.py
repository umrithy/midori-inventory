import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Midori Inventory Lab", page_icon="🍵")

st.title("🍓 Midori Puree Runway")
st.subheader("7-Day Inventory Forecast")

# Settings - You can adjust these
GRAMS_PER_DRINK = 50 

# --- STEP 1: INPUT CURRENT STOCK ---
st.sidebar.header("Current Stock (Grams)")
s_stock = st.sidebar.number_input("Strawberry", value=1500)
m_stock = st.sidebar.number_input("Mango", value=800)
b_stock = st.sidebar.number_input("Blueberry", value=2000)

# --- STEP 2: DAILY VELOCITY (Until Toast API is linked) ---
st.sidebar.header("Daily Sales (Drinks/Day)")
s_sales = st.sidebar.slider("Strawberry Drinks", 0, 100, 25)
m_sales = st.sidebar.slider("Mango Drinks", 0, 100, 15)
b_sales = st.sidebar.slider("Blueberry Drinks", 0, 100, 10)

# --- STEP 3: CALCULATIONS ---
inventory = {
    "Strawberry": {"stock": s_stock, "daily": s_sales * GRAMS_PER_DRINK},
    "Mango": {"stock": m_stock, "daily": m_sales * GRAMS_PER_DRINK},
    "Blueberry": {"stock": b_stock, "daily": b_sales * GRAMS_PER_DRINK}
}

st.write("### Your Weekly Outlook")
cols = st.columns(3)

for i, (fruit, data) in enumerate(inventory.items()):
    daily_usage = data['daily']
    if daily_usage > 0:
        runway = data['stock'] / daily_usage
    else:
        runway = 99 # Infinite if no sales
        
    with cols[i]:
        if runway >= 7:
            st.success(f"**{fruit}**")
            st.metric("Runway", f"{round(runway, 1)} Days")
        elif runway >= 3:
            st.warning(f"**{fruit}**")
            st.metric("Runway", f"{round(runway, 1)} Days")
        else:
            st.error(f"**{fruit}**")
            st.metric("Runway", f"{round(runway, 1)} Days")
            st.write("🚨 PREP NEEDED")

st.info("Note: Once the Toast API is connected, 'Daily Sales' will update automatically.")
