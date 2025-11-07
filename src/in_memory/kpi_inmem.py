import pandas as pd
from datetime import datetime, timedelta
import pytz

def kpi_repeat_customers(unified_df: pd.DataFrame) -> pd.DataFrame:
    grp = (unified_df
           .groupby(["mobile_number", "customer_id", "customer_name"], dropna=False)
           .agg(order_count=("order_id", "nunique"))
           .reset_index())
    return grp[grp["order_count"] > 1].sort_values("order_count", ascending=False)

def kpi_monthly_trends(unified_df: pd.DataFrame) -> pd.DataFrame:
    unified_df["order_month"] = (
        unified_df["order_date_time_utc"].dt.tz_convert(None).dt.to_period("M")
    )
    res = (
        unified_df
        .groupby("order_month")
        .agg(total_orders=("order_id", "nunique"),
             total_revenue=("total_amount", "sum"))
        .reset_index()
        .sort_values("order_month")
    )
    res["order_month"] = res["order_month"].astype(str)
    return res

def kpi_regional_revenue(unified_df: pd.DataFrame) -> pd.DataFrame:
    return (unified_df
            .groupby("region")
            .agg(regional_revenue=("total_amount", "sum"))
            .reset_index()
            .sort_values("regional_revenue", ascending=False))

def kpi_top_customers_last_30_days(unified_df: pd.DataFrame) -> pd.DataFrame:
    now_utc = datetime.now(pytz.utc)
    cutoff = now_utc - timedelta(days=30)
    last_30 = unified_df[unified_df["order_date_time_utc"] >= cutoff]
    return (last_30
            .groupby(["customer_id", "customer_name", "mobile_number"], dropna=False)
            .agg(total_spend=("total_amount", "sum"))
            .reset_index()
            .sort_values("total_spend", ascending=False)
            .head(10))
