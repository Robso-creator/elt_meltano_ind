import os
import subprocess
from datetime import datetime
from datetime import timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator


def extract_postgres_to_jsonl():
    env = os.environ.copy()
    env['SOURCE'] = 'postgres'
    env['YEAR'] = '2025'
    env['MONTH'] = '01'
    env['DAY'] = '01'

    subprocess.run(
        [
            'meltano',
            'run',
            'extract-postgres-to-jsonl',
        ],
        env=env,
        check=True,
    )


def extract_csv_to_jsonl():
    env = os.environ.copy()
    env['SOURCE'] = 'csv'
    env['YEAR'] = '2025'
    env['MONTH'] = '01'
    env['DAY'] = '01'

    subprocess.run(
        [
            'meltano',
            'run',
            'extract-csv-to-jsonl',
        ],
        env=env,
        check=True,
    )


def load_jsonl_to_postgres():
    env = os.environ.copy()
    env['SOURCE'] = 'csv'
    env['YEAR'] = '2025'
    env['MONTH'] = '01'
    env['DAY'] = '01'

    subprocess.run(
        [
            'meltano',
            'run',
            'load-jsonl-to-postgres',
        ],
        env=env,
        check=True,
    )


cron = '0 6 * * *'
description = """Executa script do ETL de multiplas fontes de dados para o banco de dados"""
start = datetime(2024, 1, 1)

with DAG(
    'dag_elt_meltano_pipeline',
    default_args={
        'owner': 'airflow',
        'catchup': True,
        'retries': 3,
        'retry_delay': timedelta(minutes=5),
        'concurrency': 1,
    },
    start_date=start,
    schedule=cron,
    description=description,
) as dag:
    extract_postgres = PythonOperator(
        task_id='extract_postgres',
        python_callable=extract_postgres_to_jsonl,
    )
    extract_csv = PythonOperator(
        task_id='extract_csv',
        python_callable=extract_csv_to_jsonl,
    )
    load_jsonl = PythonOperator(
        task_id='load_jsonl',
        python_callable=load_jsonl_to_postgres,
        trigger_rule='all_success',
    )

    [extract_csv, extract_postgres] >> load_jsonl
