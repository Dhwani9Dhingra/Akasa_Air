import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import text
from src.table_based.db import get_engine
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

# -------------------- 🌈 Streamlit Page Config --------------------
st.set_page_config(
    page_title="Akasa Air Insights Dashboard",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------- 🎨 Custom CSS Styling --------------------
st.markdown(
    """
    <style>
        body {
            background-color: #ffffff;
        }
        .main {
            background-color: #ffffff;
            color: #0A2647;
        }
        h1, h2, h3, h4 {
            color: #F97316;  /* Akasa Orange */
            font-weight: 700;
        }
        .stDataFrame {
            border: 1px solid #0A2647;
            border-radius: 8px;
        }
        div[data-testid="stSidebar"] {
            background-color: #0A2647;
            color: white;
        }
        div[data-testid="stSidebar"] * {
            color: white !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------- ✈️ App Header --------------------
st.title("🧭 Akasa Air - Customer & Order Insights Dashboard")
st.markdown("##### A data-driven view of customer behaviour, orders, and revenue insights")

mode = st.sidebar.radio("Select Processing Mode", ["In-Memory", "Table-Based (MySQL)"])

# -------------------- 🧠 Helper Chart Functions --------------------
def line_chart_monthly(df):
    """Monthly Order Trends (Line Chart)"""
    df['month'] = pd.to_datetime(df.iloc[:, 0]).dt.strftime('%b')
    fig = px.line(
        df,
        x='month',
        y=df.columns[1],
        markers=True,
        line_shape="spline",
        title="📈 Monthly Order Trends",
        color_discrete_sequence=["#F97316"],
    )
    fig.update_traces(line=dict(width=5))
    fig.update_layout(
        xaxis_title="<b>Month</b>",
        yaxis_title=f"<b>{df.columns[1].replace('_',' ').title()}</b>",
        template="plotly_white",
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        width=700, height=400,
        xaxis=dict(
            showgrid=False,
            tickfont=dict(color="black", size=13, family="Arial"),
            title=dict(font=dict(color="black", size=15))
        ),
        yaxis=dict(
            showgrid=False,
            tickfont=dict(color="black", size=13, family="Arial"),
            title=dict(font=dict(color="black", size=15))
        ),
        title_font=dict(size=18, color="black", family="Arial"),
    )
    return fig


def funnel_chart_region(df):
    """Regional Revenue (Funnel Chart)"""
    fig = px.funnel(
        df,
        x=df.columns[1],
        y=df.columns[0],
        color_discrete_sequence=["#0A2647"],
        title="💰 Regional Revenue Funnel"
    )
    fig.update_layout(
        xaxis_title=f"<b>{df.columns[1].replace('_',' ').title()}</b>",
        yaxis_title=f"<b>{df.columns[0].replace('_',' ').title()}</b>",
        template="plotly_white",
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        width=700, height=400,
        xaxis=dict(
            showgrid=False,
            tickfont=dict(color="black", size=13, family="Arial"),
            title=dict(font=dict(color="black", size=15))
        ),
        yaxis=dict(
            showgrid=False,
            tickfont=dict(color="black", size=13, family="Arial"),
            title=dict(font=dict(color="black", size=15))
        ),
        title_font=dict(size=18, color="black", family="Arial"),
    )
    return fig


def horizontal_bar_top_customers(df):
    """Top Performing Customers (Horizontal Bar Chart)"""
    fig = px.bar(
        df.sort_values(df.columns[-1], ascending=True),
        x=df.columns[-1],
        y=df.columns[1],
        orientation='h',
        text_auto='.2s',
        color_discrete_sequence=["#F97316"],
        title="🏆 Top Performing Customers (Last 30 Days)"
    )
    fig.update_layout(
        xaxis_title=f"<b>{df.columns[-1].replace('_',' ').title()}</b>",
        yaxis_title=f"<b>{df.columns[1].replace('_',' ').title()}</b>",
        template="plotly_white",
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        width=700, height=400,
        xaxis=dict(
            showgrid=False,
            tickfont=dict(color="black", size=13, family="Arial"),
            title=dict(font=dict(color="black", size=15))
        ),
        yaxis=dict(
            showgrid=False,
            tickfont=dict(color="black", size=13, family="Arial"),
            title=dict(font=dict(color="black", size=15))
        ),
        title_font=dict(size=18, color="black", family="Arial"),
    )
    return fig

# -------------------- 🧾 In-Memory Mode --------------------
if mode == "In-Memory":
    customers_df = clean_customers_inmem("data/task_DE_new_customers.csv")
    orders_raw_df, orders_order_level_df = clean_orders_inmem("data/task_DE_new_orders.xml")
    unified_df = build_unified_inmem(customers_df, orders_order_level_df)

    rep = kpi_repeat_customers(unified_df)
    mon = kpi_monthly_trends(unified_df)
    reg = kpi_regional_revenue(unified_df)
    top = kpi_top_customers_last_30_days(unified_df)

    st.subheader("👥 Repeat Customers")
    st.dataframe(rep, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📅 Monthly Trends")
        st.plotly_chart(line_chart_monthly(mon), use_container_width=True)
    with col2:
        st.subheader("🌍 Revenue by Region")
        st.plotly_chart(funnel_chart_region(reg), use_container_width=True)

    st.subheader("🏅 Top Customers (Last 30 Days)")
    st.plotly_chart(horizontal_bar_top_customers(top), use_container_width=True)

# -------------------- 🗃️ Table-Based Mode --------------------
else:
    engine = get_engine()
    with engine.begin() as conn:
        repeat_df = pd.read_sql(text("""
            SELECT c.customer_id, c.customer_name, c.mobile_number,
                   COUNT(DISTINCT o.order_id) AS order_count
            FROM customers c
            JOIN orders_fact o ON c.mobile_number = o.mobile_number
            GROUP BY c.customer_id, c.customer_name, c.mobile_number
            HAVING COUNT(DISTINCT o.order_id) > 1;
        """), conn)

        monthly_df = pd.read_sql(text("""
            SELECT DATE_FORMAT(o.order_date_time_utc, '%Y-%m') AS order_month,
                   COUNT(DISTINCT o.order_id) AS total_orders,
                   SUM(o.total_amount) AS total_revenue
            FROM orders_fact o
            GROUP BY DATE_FORMAT(o.order_date_time_utc, '%Y-%m')
            ORDER BY order_month;
        """), conn)

        regional_df = pd.read_sql(text("""
            SELECT c.region,
                   SUM(o.total_amount) AS regional_revenue
            FROM orders_fact o
            JOIN customers c ON o.mobile_number = c.mobile_number
            GROUP BY c.region
            ORDER BY regional_revenue DESC;
        """), conn)

        top_df = pd.read_sql(text("""
           SELECT c.customer_id, c.customer_name, c.mobile_number,
           SUM(o.total_amount) AS total_spend
           FROM orders_fact o
           JOIN customers c ON o.mobile_number = c.mobile_number
           WHERE o.order_date_time_utc >= (UTC_TIMESTAMP() - INTERVAL 30 DAY)
           GROUP BY c.customer_id, c.customer_name, c.mobile_number
           ORDER BY total_spend DESC
           LIMIT 10;
        """), conn)

    st.subheader("👥 Repeat Customers")
    st.dataframe(repeat_df, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📅 Monthly Trends")
        st.plotly_chart(line_chart_monthly(monthly_df), use_container_width=True)
    with col2:
        st.subheader("🌍 Revenue by Region")
        st.plotly_chart(funnel_chart_region(regional_df), use_container_width=True)

    st.subheader("🏅 Top Customers (Last 30 Days)")
    st.plotly_chart(horizontal_bar_top_customers(top_df), use_container_width=True)
