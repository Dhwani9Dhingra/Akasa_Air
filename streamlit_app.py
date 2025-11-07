# src/dashboard/streamlit_app.py
"""
Simple Streamlit Dashboard for Akasa Air Data Engineering Task

- Uses only the in-memory approach for demonstration.
- Displays all 4 KPIs as blue bar charts.
- Easy to showcase in an interview or presentation.
"""

import streamlit as st
import plotly.express as px
from src.in_memory.preprocess_inmem import (
    clean_customers_inmem,
    clean_orders_inmem,
    build_unified_inmem,
)
from src.in_memory.kpi_inmem import (
    kpi_repeat_customers,
    kpi_monthly_trends,
    kpi_regional_revenue,
    kpi_top_customers_last_30_days,
)

# ---------------------------
# PAGE SETUP
# ---------------------------
st.set_page_config(page_title="Akasa Air - KPI Dashboard", layout="wide")

st.title("📊 Akasa Air - Data Engineering Dashboard")
st.markdown("A simple showcase of KPIs and insights using **blue bar charts** (In-Memory Approach).")

# ---------------------------
# LOAD & PREPROCESS DATA
# ---------------------------
customers_df = clean_customers_inmem("data/task_DE_new_customers.csv")
orders_raw_df, orders_order_level_df = clean_orders_inmem("data/task_DE_new_orders.xml")
unified_df = build_unified_inmem(customers_df, orders_order_level_df)

# ---------------------------
# COMPUTE KPIs
# ---------------------------
repeat_df = kpi_repeat_customers(unified_df)
monthly_df = kpi_monthly_trends(unified_df)
regional_df = kpi_regional_revenue(unified_df)
top_df = kpi_top_customers_last_30_days(unified_df)

# ---------------------------
# VISUALIZATIONS
# ---------------------------

st.subheader("1️⃣ Repeat Customers")
fig_repeat = px.bar(
    repeat_df,
    x="customer_name",
    y="order_count",
    color_discrete_sequence=["#007BFF"],  # blue
    title="Repeat Customers by Order Count"
)
st.plotly_chart(fig_repeat, use_container_width=True)


st.subheader("2️⃣ Monthly Order Trends")
fig_month = px.bar(
    monthly_df,
    x="order_month",
    y="total_orders",
    color_discrete_sequence=["#007BFF"],
    title="Monthly Order Count"
)
st.plotly_chart(fig_month, use_container_width=True)


st.subheader("3️⃣ Regional Revenue Distribution")
fig_region = px.bar(
    regional_df,
    x="region",
    y="regional_revenue",
    color_discrete_sequence=["#007BFF"],
    title="Revenue by Region"
)
st.plotly_chart(fig_region, use_container_width=True)


st.subheader("4️⃣ Top Customers by Spend (Last 30 Days)")
fig_top = px.bar(
    top_df,
    x="customer_name",
    y="total_spend",
    color_discrete_sequence=["#007BFF"],
    title="Top Customers (Last 30 Days)"
)
st.plotly_chart(fig_top, use_container_width=True)


st.markdown("---")
st.markdown("✅ *All charts are generated from in-memory processed data using Pandas.*")
