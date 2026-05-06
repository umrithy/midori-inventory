import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="Midori Inventory Lab", page_icon="🍵", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #fcfaf5; }
    </style>
    """, unsafe_allow_html=True)

st.title("🍵 Midori Puree Runway")
st.subheader("7-Day Inventory Forecast & Prep Guide")

# --- RECIPE & WASTE CONSTANTS ---
GRAMS_PER_DRINK = 40 
YIELD_PER_BATCH = 535 
WASTE_BUFFER = 1.10 # Adds 10% for spills/residue
GRAMS_PER_24OZ_BOTTLE = 680 

# --- SIDEBAR: LIVE INPUTS ---
with st.sidebar:
    st.header("📍 Current Shop Stock")
    input_mode = st.radio("How are you counting?", ["By Grams", "By 24oz Bottles"])
    
    if input_mode == "By Grams":
        s_stock = st.number_input("Strawberry (g)", value=1500, step=100)
        m_stock = st.number_input("Mango (g)", value=800, step=100)
        b_stock = st.number_input("Blueberry (g)", value=2000, step=100)
    else:
        s_bot = st.number_input("Strawberry (Bottles)", value=2.0, step=0.5)
        m_bot = st.number_input("Mango (Bottles)", value=1.0, step=0.5)
        b_bot = st.number_input("Blueberry (Bottles)", value=3.0, step=0.5)
        s_stock = s_bot * GRAMS_PER_24OZ_BOTTLE
        m_stock = m_bot * GRAMS_PER_24OZ_BOTTLE
        b_stock = b_bot * GRAMS_PER_24OZ_BOTTLE
    
    st.divider()
    st.header("📈 Daily Sales Velocity")
    s_sales = st.slider("Strawberry Matchas", 0, 100, 20)
    m_sales = st.slider("Mango Matchas", 0, 100, 15)
    b_sales = st.slider("Blueberry Matchas", 0, 100, 10)

# --- LOGIC ENGINE ---
# We multiply the daily usage by the WASTE_BUFFER to account for that 10% loss
inventory = {
    "Strawberry": {"stock": s_stock, "daily": (s_sales * GRAMS_PER_DRINK) * WASTE_BUFFER},
    "Mango": {"stock": m_stock, "daily": (m_sales * GRAMS_PER_DRINK) * WASTE_BUFFER},
    "Blueberry": {"stock": b_stock, "daily": (b_sales * GRAMS_PER_DRINK) * WASTE_BUFFER}
}

# --- DASHBOARD ---
cols = st.columns(3)
for i, (fruit, data) in enumerate(inventory.items()):
    daily_usage = data['daily']
    runway = data['stock'] / daily_usage if daily_usage > 0 else 99
    
    with cols[i]:
        if runway >= 7:
            status_text = "✅ STOCKED"
        elif runway >= 3:
            status_text = "⚠️ WATCHING"
        else:
            status_text = "🚨 PREP NOW"
            
        st.metric(label=f"{fruit} ({status_text})", value=f"{round(runway, 1)} Days", delta=f"{int(data['stock'])}g net stock")

st.divider()

# --- PREP GUIDE SECTION ---
st.write("### 👨‍🍳 Production Plan (7-Day Target + 10% Buffer)")
prep_cols = st.columns(3)
for i, (fruit, data) in enumerate(inventory.items()):
    target_7_day = data['daily'] * 7 # Already includes the 10% waste buffer
    shortfall = max(0, target_7_day - data['stock'])
    batches_needed = math.ceil(shortfall / YIELD_PER_BATCH) if shortfall > 0 else 0
    
    with prep_cols[i]:
        if batches_needed > 0:
            st.error(f"Make **{batches_needed} batch(es)**")
            st.caption(f"Required for 7 days: {int(target_7_day)}g")
        else:
            st.success(f"{fruit} is fully prepped!")
