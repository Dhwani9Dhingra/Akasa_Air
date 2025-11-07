from src.in_memory.preprocess_inmem import (
    clean_customers_inmem,
    clean_orders_inmem,
    build_unified_inmem,
)
from src.table_based.preprocess_table import (
    preprocess_customers_for_db,
    preprocess_orders_for_db,
)
from src.table_based.load_table import (
    create_tables,
    load_customers,
    load_orders,
)

def main():
    # in-memory branch
    customers_df = clean_customers_inmem("data/task_DE_new_customers.csv")
    orders_raw_df, orders_order_level_df = clean_orders_inmem("data/task_DE_new_orders.xml")
    unified_df = build_unified_inmem(customers_df, orders_order_level_df)
    print("In-memory unified view:")
    print(unified_df.head())

    # table-based branch
    customers_db_df = preprocess_customers_for_db("data/task_DE_new_customers.csv")
    orders_raw_db_df, orders_fact_db_df = preprocess_orders_for_db("data/task_DE_new_orders.xml")

    create_tables()
    load_customers(customers_db_df)
    load_orders(orders_fact_db_df, orders_raw_db_df)

    print("Table-based load completed.")

if __name__ == "__main__":
    main()
