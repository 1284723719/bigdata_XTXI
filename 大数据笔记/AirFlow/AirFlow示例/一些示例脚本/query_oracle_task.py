# -*- coding:utf-8 -*-
#__author__ = 'laowei'
from datetime import timedelta

from airflow import DAG

from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from airflow.providers.oracle.operators.oracle import OracleOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=30)
}

dag = DAG(
    'oracle_operator_dag',
    default_args=default_args,
    description='query one oracle table task of dag',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(1),
    tags=['itcast'],
)

query_oracle_task = OracleOperator(
    task_id = 'oracle_operator_task',
    sql = 'select * from ciss4.ciss_base_areas',
    oracle_conn_id = 'oracle-airflow-connection',
    autocommit = True,
    dag=dag)
    
query_oracle_task
