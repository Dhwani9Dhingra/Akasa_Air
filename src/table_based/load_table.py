def load_orders(fact_df, raw_df):
    """Idempotent upsert for orders and items using ON DUPLICATE KEY UPDATE."""
    engine = get_engine()
    with engine.begin() as conn:
        # Upsert order-level table
        for _, row in fact_df.iterrows():
            conn.execute(
                text("""
                    INSERT INTO orders_fact (order_id, mobile_number, order_date_time_utc, total_amount)
                    VALUES (:order_id, :mobile_number, :order_date_time_utc, :total_amount)
                    ON DUPLICATE KEY UPDATE
                        mobile_number = VALUES(mobile_number),
                        order_date_time_utc = VALUES(order_date_time_utc),
                        total_amount = VALUES(total_amount);
                """),
                {
                    "order_id": row["order_id"],
                    "mobile_number": row["mobile_number"],
                    "order_date_time_utc": row["order_date_time_utc"],
                    "total_amount": row["total_amount"],
                },
            )

        # Upsert order_items
        for _, row in raw_df.iterrows():
            conn.execute(
                text("""
                    INSERT INTO order_items (order_id, sku_id, sku_count)
                    VALUES (:order_id, :sku_id, :sku_count)
                    ON DUPLICATE KEY UPDATE
                        sku_count = VALUES(sku_count);
                """),
                {
                    "order_id": row["order_id"],
                    "sku_id": row["sku_id"],
                    "sku_count": row["sku_count"],
                },
            )
