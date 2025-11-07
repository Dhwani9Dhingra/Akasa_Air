# src/in_memory/preprocess_inmem.py
"""
In-memory cleaning/preprocessing with proper mobile number normalization.
"""
import pandas as pd
import re
from src.common.io_sources import read_customers_csv, read_orders_xml
from src.common.tz_utils import to_utc

def normalize_mobile_column(df: pd.DataFrame, column: str = "mobile_number") -> pd.DataFrame:
    """
    Normalize mobile numbers:
    - Convert to string
    - Remove non-digit characters
    - Keep last 10 digits (Indian phone number)
    - Convert to int64
    """
    df[column] = (
        df[column]
        .astype(str)
        .str.replace(r"\D", "", regex=True)  # remove non-digits
        .str[-10:]  # keep last 10 digits
    )
    # drop rows with invalid or missing numbers
    df = df[df[column].str.len() == 10]
    df[column] = df[column].astype("int64")
    return df


def clean_customers_inmem(path: str) -> pd.DataFrame:
    df = read_customers_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]
    df["customer_name"] = df["customer_name"].str.strip()
    df["region"] = df["region"].fillna("Unknown")

    # normalize mobile numbers here
    df = normalize_mobile_column(df, "mobile_number")

    df = df.drop_duplicates(subset=["mobile_number"])
    return df


def clean_orders_inmem(path: str):
    df = read_orders_xml(path)

    # normalize mobile numbers from XML
    df = normalize_mobile_column(df, "mobile_number")

    # normalize timestamps to UTC (mandatory)
    df = to_utc(df, col="order_date_time")

    # deduplicate to order-level
    order_level = df.drop_duplicates(subset=["order_id"]).reset_index(drop=True)
    return df, order_level


def build_unified_inmem(customers_df: pd.DataFrame,
                        orders_order_level_df: pd.DataFrame) -> pd.DataFrame:
    """
    Join on mobile_number (now uniform int64)
    """
    unified = orders_order_level_df.merge(
        customers_df,
        on="mobile_number",
        how="left"
    )
    return unified
