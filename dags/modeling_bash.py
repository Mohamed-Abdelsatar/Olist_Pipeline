from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime


DBT_PROJECT_DIR = "/path/to/abdelsatar"

with DAG(
    dag_id="abdelsatar_modeling_bash",
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:
 
    
    run_fact_orders = BashOperator(
        task_id="run_fact_orders",
        bash_command=f"dbt run --project-dir {DBT_PROJECT_DIR} --profiles-dir {DBT_PROJECT_DIR} --models Olist.olist_satar_fact",
    )

   
    run_dim_top_customers = BashOperator(
        task_id="run_dim_top_customers",
        bash_command=f"dbt run --project-dir {DBT_PROJECT_DIR} --profiles-dir {DBT_PROJECT_DIR} --models Olist.olist_satar_cust",
    )

    run_dim_top_products = BashOperator(
        task_id="run_dim_top_products",
        bash_command=f"dbt run --project-dir {DBT_PROJECT_DIR} --profiles-dir {DBT_PROJECT_DIR} --models Olist.olist_satar_prod",
    )

    run_dim_monthly_orders = BashOperator(
        task_id="run_dim_monthly_orders",
        bash_command=f"dbt run --project-dir {DBT_PROJECT_DIR} --profiles-dir {DBT_PROJECT_DIR} --models Olist.olist_satar_ord",
    )

    run_dim_payment_distribution = BashOperator(
        task_id="run_dim_payment_distribution",
        bash_command=f"dbt run --project-dir {DBT_PROJECT_DIR} --profiles-dir {DBT_PROJECT_DIR} --models Olist.olist_satar_pay",
    )

    run_dim_avg_orders_per_customer = BashOperator(
        task_id="run_dim_avg_orders_per_customer",
        bash_command=f"dbt run --project-dir {DBT_PROJECT_DIR} --profiles-dir {DBT_PROJECT_DIR} --models Olist.olist_satar_ord_cast",
    )

    run_dim_category_revenue = BashOperator(
        task_id="run_dim_category_revenue",
        bash_command=f"dbt run --project-dir {DBT_PROJECT_DIR} --profiles-dir {DBT_PROJECT_DIR} --models Olist.olist_satar_cat",
    )

   
    run_fact_orders >> [
        run_dim_top_customers,
        run_dim_top_products,
        run_dim_monthly_orders,
        run_dim_payment_distribution,
        run_dim_avg_orders_per_customer,
        run_dim_category_revenue,
    ]
