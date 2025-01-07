from airflow import DAG
from airflow.providers.google.cloud.operators.gcs import GCSDeleteObjectsOperator
from airflow.providers.google.cloud.transfers.postgres_to_gcs import PostgresToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from datetime import datetime
import requests
from airflow.operators.python import PythonOperator
from google.cloud import storage


# DAG configuration
DEFAULT_ARGS = {
    'owner': 'abdelsatar',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1
}

BUCKET_NAME='ready-d25-postgres-to-gcs'
PROJECT_ID='ready-de-25'
DATASET_ID='olist_abdelsatar'



with DAG(
    dag_id='abdelsatar_transfer',
    default_args=DEFAULT_ARGS,
    description='Transfer data from PostgreSQL and API to BigQuery - Ready Talent Data Engineering Project (D25)',
    schedule=None,
    start_date=datetime(2025, 1, 1),
    catchup=False
) as dag:


    postgres_tables = {
        "customers": "SELECT * FROM customers",
        "geolocation": "SELECT * FROM geolocation",
        "order_items": "SELECT * FROM order_items",
        "order_reviews": "SELECT review_id, order_id, review_score FROM order_reviews",
        "orders": "SELECT * FROM orders",
        "products": "SELECT * FROM products",
        "product_category_name_translation": "SELECT * FROM product_category_name_translation"
    }

    for table_name, query in postgres_tables.items():
        export_to_gcs = PostgresToGCSOperator(
            task_id=f'export_{table_name}_to_gcs',
            postgres_conn_id='postgres_z',
            sql=query,
            bucket=BUCKET_NAME,
            filename=f'abdelsatar/Olist_Project/{table_name}.csv',
            export_format='csv',
        )

        load_to_bq = GCSToBigQueryOperator(
            task_id=f'load_{table_name}_to_bq',
            bucket=BUCKET_NAME,
            source_objects=[f'abdelsatar/Olist_Project/{table_name}.csv'],
            destination_project_dataset_table=f'{PROJECT_ID}.{DATASET_ID}.{table_name}',
            source_format='csv',
            skip_leading_rows=1,
            autodetect=True,
            write_disposition='WRITE_TRUNCATE'
        )

        export_to_gcs >> load_to_bq

    # Fetch API data and load to BigQuery
    api_endpoints = {
        "order_payments": "https://us-central1-ready-de-25.cloudfunctions.net/order_payments_table",
        "sellers": "https://us-central1-ready-de-25.cloudfunctions.net/sellers_table"
    }

    def fetch_and_upload_to_gcs(endpoint, bucket_name, destination_blob_name):
        response = requests.get(endpoint)
        response.raise_for_status()
        data = response.text
        client = storage.Client()
        bucket = client.get_bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_string(data)


    for table_name, endpoint in api_endpoints.items():
        fetch_api_data = PythonOperator(
            task_id=f'fetch_{table_name}_data',
            python_callable=fetch_and_upload_to_gcs,
            op_args=[endpoint, BUCKET_NAME, f'abdelsatar/Olist_Project/{table_name}.csv']
        )

        load_api_to_bq = GCSToBigQueryOperator(
            task_id=f'load_{table_name}_to_bq',
            bucket=BUCKET_NAME,
            source_objects=[f'abdelsatar/Olist_Project/{table_name}.csv'],
            destination_project_dataset_table=f'{PROJECT_ID}.{DATASET_ID}.{table_name}',
            source_format='csv',
            write_disposition='WRITE_TRUNCATE'
        )

        fetch_api_data >> load_api_to_bq