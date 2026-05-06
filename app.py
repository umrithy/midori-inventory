import streamlit as st
import pandas as pd

st.set_page_config(page_title="Midori Inventory Lab", page_icon="🍵", layout="wide")

# Custom Midori Styling
st.markdown("""
    <style>
    .main { background-color: #fcfaf5; }
    </style>
    """, unsafe_allow_html=True)

st.title("🍵 Midori Puree Runway")
st.subheader("7-Day Inventory Forecast & Prep Guide")

# --- SETTINGS ---
GRAMS_PER_DRINK = 40 

# --- SIDEBAR: LIVE INPUTS ---
with st.sidebar:
    st.header("📍 Current Shop Stock")
    st.info("Enter total grams currently in the fridge.")
    s_stock = st.number_input("Strawberry (g)", value=1500, step=100)
    m_stock = st.number_input("Mango (g)", value=800, step=100)
    b_stock = st.number_input("Blueberry (g)", value=2000, step=100)
    
    st.divider()
    st.header("📈 Daily Sales Velocity")
    st.caption("How many of each drink per day?")
    s_sales = st.slider("Strawberry Matchas", 0, 100, 20)
    m_sales = st.slider("Mango Matchas", 0, 100, 15)
    b_sales = st.slider("Blueberry Matchas", 0, 100, 10)

# --- LOGIC ENGINE ---
inventory = {
    "Strawberry": {"stock": s_stock, "daily": s_sales * GRAMS_PER_DRINK},
    "Mango": {"stock": m_stock, "daily": m_sales * GRAMS_PER_DRINK},
    "Blueberry": {"stock": b_stock, "daily": b_sales * GRAMS_PER_DRINK}
}

# --- DASHBOARD ---
cols = st.columns(3)

for i, (fruit, data) in enumerate(inventory.items()):
    daily_usage = data['daily']
    runway = data['stock'] / daily_usage if daily_usage > 0 else 99
    
    with cols[i]:
        if runway >= 7:
            status_text = "✅ STOCKED"
            color_label = "normal"
        elif runway >= 3:
            status_text = "⚠️ WATCHING"
            color_label = "off"
        else:
            status_text = "🚨 PREP NOW"
            color_label = "inverse"
            
        st.metric(label=f"{fruit} ({status_text})", value=f"{round(runway, 1)} Days", delta=f"{data['stock']}g stock")

st.divider()

# --- PREP GUIDE SECTION ---
st.write("### 📝 Next 7-Day Prep Guide")
st.caption("Target: Maintain a 7-day safety buffer.")

prep_cols = st.columns(3)
for i, (fruit, data) in enumerate(inventory.items()):
    target_7_day = data['daily'] * 7
    shortfall = max(0, target_7_day - data['stock'])
    
    with prep_cols[i]:
        if shortfall > 0:
            st.error(f"Make **{shortfall}g** of {fruit}")
        else:
            st.success(f"{fruit} is fully prepped!")
