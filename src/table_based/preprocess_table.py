# src/table_based/preprocess_table.py
import pandas as pd
import re
from src.common.io_sources import read_customers_csv, read_orders_xml
from src.common.tz_utils import to_utc

def normalize_mobile_column(df: pd.DataFrame, column: str = "mobile_number") -> pd.DataFrame:
    df[column] = (
        df[column]
        .astype(str)
        .str.replace(r"\D", "", regex=True)
        .str[-10:]
    )
    df = df[df[column].str.len() == 10]
    df[column] = df[column].astype("int64")
    return df

def preprocess_customers_for_db(path: str) -> pd.DataFrame:
    df = read_customers_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]
    df["customer_name"] = df["customer_name"].str.strip()
    df["region"] = df["region"].fillna("Unknown")

    # normalize mobile numbers
    df = normalize_mobile_column(df, "mobile_number")

    df = df.drop_duplicates(subset=["mobile_number"])
    return df

def preprocess_orders_for_db(path: str):
    raw_df = read_orders_xml(path)
    raw_df = normalize_mobile_column(raw_df, "mobile_number")
    raw_df = to_utc(raw_df, col="order_date_time")

    fact_df = raw_df.drop_duplicates(subset=["order_id"]).reset_index(drop=True)
    fact_df["order_date_time_utc"] = fact_df["order_date_time_utc"].dt.tz_convert("UTC").dt.tz_localize(None)
    return raw_df, fact_df
