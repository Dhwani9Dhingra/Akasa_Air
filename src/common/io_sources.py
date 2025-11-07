import pandas as pd
from lxml import etree

def read_customers_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def read_orders_xml(path: str) -> pd.DataFrame:
    tree = etree.parse(path)
    root = tree.getroot()
    rows = []
    for order in root.findall("order"):
        rows.append({
            "order_id": order.findtext("order_id"),
            "mobile_number": order.findtext("mobile_number"),
            "order_date_time": order.findtext("order_date_time"),
            "sku_id": order.findtext("sku_id"),
            "sku_count": int(order.findtext("sku_count") or 0),
            "total_amount": float(order.findtext("total_amount") or 0.0),
        })
    return pd.DataFrame(rows)
