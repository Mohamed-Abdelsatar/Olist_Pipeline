from airflow import DAG
from airflow.providers.dbt.cloud.operators.dbt import DbtRunOperator
from datetime import datetime

with DAG(
    dag_id="abdelsatar_modeling",
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:

    run_fact_orders = DbtRunOperator(
        task_id="run_fact_orders",
        models="Olist.olist_satar_fact"  
    )

    run_dim_top_customers = DbtRunOperator(
        task_id="run_dim_top_customers",
        models="Olist.olist_satar_cust",
    )

    run_dim_top_products = DbtRunOperator(
        task_id="run_dim_top_products",
        models="Olist.olist_satar_prod",
    )

    run_dim_monthly_orders = DbtRunOperator(
        task_id="run_dim_monthly_orders",
        models="Olist.olist_satar_ord",
    )

    run_dim_payment_distribution = DbtRunOperator(
        task_id="run_dim_payment_distribution",
        models="Olist.olist_satar_pay",
    )

    run_dim_avg_orders_per_customer = DbtRunOperator(
        task_id="run_dim_avg_orders_per_customer",
        models="Olist.olist_satar_ord_cast",
    )

    run_dim_category_revenue = DbtRunOperator(
        task_id="run_dim_category_revenue",
        models="Olist.olist_satar_cat",
    )

    run_fact_orders >> [
        run_dim_top_customers,
        run_dim_top_products,
        run_dim_monthly_orders,
        run_dim_payment_distribution,
        run_dim_avg_orders_per_customer,
        run_dim_category_revenue,
    ]
