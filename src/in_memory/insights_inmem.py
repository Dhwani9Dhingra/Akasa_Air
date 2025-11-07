import plotly.express as px
import pandas as pd

def monthly_trend_chart(monthly_df: pd.DataFrame):
    return px.bar(
        monthly_df, x="order_month", y="total_orders",
        title="Monthly Order Trends", text_auto=True
    )

def regional_revenue_chart(regional_df: pd.DataFrame):
    return px.bar(
        regional_df, x="region", y="regional_revenue",
        title="Regional Revenue", text_auto=True
    )

def top_customers_chart(top_df: pd.DataFrame):
    # Works for both table-based (SQL) and in-memory (pandas)
    return px.bar(
        top_df, x="customer_name", y="total_spend",
        title="Top Customers by Spend (Last 30 Days)", text_auto=True
    )
