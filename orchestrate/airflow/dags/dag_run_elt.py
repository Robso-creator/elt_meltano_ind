import os
import subprocess
from datetime import datetime
from datetime import timedelta

import pytz
from airflow import DAG
from airflow.operators.python import PythonOperator


def get_current_local_time():
    return datetime.now(pytz.timezone('America/Sao_Paulo')).replace(tzinfo=None)


def extract_postgres_to_jsonl(run_date=get_current_local_time().strftime('%Y-%m-%d')):
    run_date = datetime.strptime(run_date, '%Y-%m-%d')

    env = os.environ.copy()
    env['SOURCE'] = 'postgres'
    env['YEAR'] = run_date.strftime('%Y')
    env['MONTH'] = run_date.strftime('%m')
    env['DAY'] = run_date.strftime('%d')

    subprocess.run(
        [
            'meltano',
            'run',
            'extract-postgres-to-jsonl',
        ],
        env=env,
        check=True,
    )


def extract_csv_to_jsonl(run_date=get_current_local_time().strftime('%Y-%m-%d')):
    run_date = datetime.strptime(run_date, '%Y-%m-%d')

    env = os.environ.copy()
    env['SOURCE'] = 'csv'
    env['YEAR'] = run_date.strftime('%Y')
    env['MONTH'] = run_date.strftime('%m')
    env['DAY'] = run_date.strftime('%d')

    subprocess.run(
        [
            'meltano',
            'run',
            'extract-csv-to-jsonl',
        ],
        env=env,
        check=True,
    )


def load_jsonl_to_postgres(run_date=get_current_local_time().strftime('%Y-%m-%d')):
    run_date = datetime.strptime(run_date, '%Y-%m-%d')

    env = os.environ.copy()
    env['YEAR'] = run_date.strftime('%Y')
    env['MONTH'] = run_date.strftime('%m')
    env['DAY'] = run_date.strftime('%d')

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
    render_template_as_native_obj=True,
    params={'run_date': get_current_local_time().strftime('%Y-%m-%d')},
) as dag:
    extract_postgres = PythonOperator(
        task_id='extract_postgres',
        python_callable=extract_postgres_to_jsonl,
        op_kwargs={'run_date': '{{ params.run_date }}'},
    )
    extract_csv = PythonOperator(
        task_id='extract_csv',
        python_callable=extract_csv_to_jsonl,
        op_kwargs={'run_date': '{{ params.run_date }}'},
    )
    load_jsonl = PythonOperator(
        task_id='load_jsonl',
        python_callable=load_jsonl_to_postgres,
        op_kwargs={'run_date': '{{ params.run_date }}'},
        trigger_rule='all_success',
    )

    [extract_csv, extract_postgres] >> load_jsonl
