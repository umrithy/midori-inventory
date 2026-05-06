import streamlit as st
import pandas as pd

st.set_page_config(page_title="Midori Inventory Lab", page_icon="🍵", layout="wide")

# Custom Midori Styling
st.markdown("""
    <style>
    .main { background-color: #fcfaf5; }
    stMetric { background-color: #ffffff; border-radius: 10px; padding: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_content_safe=True)

st.title("🍵 Midori Puree Runway")
st.subheader("7-Day Inventory Forecast & Prep Guide")

# --- SETTINGS ---
GRAMS_PER_DRINK = 40  # Updated per your instruction

# --- SIDEBAR: LIVE INPUTS ---
with st.sidebar:
    st.header("📍 Current Shop Stock")
    st.info("Enter the total grams currently in the fridge.")
    s_stock = st.number_input("Strawberry (g)", value=1500, step=100)
    m_stock = st.number_input("Mango (g)", value=800, step=100)
    b_stock = st.number_input("Blueberry (g)", value=2000, step=100)
    
    st.divider()
    st.header("📈 Daily Sales Velocity")
    st.caption("How many of each drink are you selling per day?")
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
            color = "inverse" # Green
            status_text = "✅ STOCKED"
        elif runway >= 3:
            color = "normal" # Yellow/Orange
            status_text = "⚠️ WATCHING"
        else:
            color = "off" # Red
            status_text = "🚨 PREP NOW"
            
        st.metric(label=f"{fruit} ({status_text})", value=f"{round(runway, 1)} Days", delta=f"{data['stock']}g left", delta_color=color)

st.divider()

# --- PREP GUIDE SECTION ---
st.write("### 📝 Next 7-Day Prep Guide")
st.caption("To maintain a 7-day safety buffer, you need the following total stock:")

prep_cols = st.columns(3)
for i, (fruit, data) in enumerate(inventory.items()):
    target_7_day = data['daily'] * 7
    shortfall = max(0, target_7_day - data['stock'])
    
    with prep_cols[i]:
        if shortfall > 0:
            st.error(f"Make **{shortfall}g** of {fruit}")
        else:
            st.success(f"{fruit} is fully prepped!")

st.info("Tip: If you are seeing 'PREP NOW', check your raw fruit supply in the freezer.")
