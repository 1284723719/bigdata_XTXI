# -*- coding:utf-8 -*-
#__author__ = 'laowei'
from airflow import DAG
from airflow.providers.apache.sqoop.operators.sqoop import SqoopOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
}

dag = DAG(
    'sqoop_operator_import_hdfs',
    default_args=default_args,
    schedule_interval=None,
    start_date=days_ago(1),
    tags=['itcast']
)

sqoop_import_hdfs_task = SqoopOperator(
    task_id='sqoop_operator_import_hdfs_task',
    conn_id='sqoop-airflow-connection',
    cmd_type='import',
    target_dir='/data/sqoop/airflow/CISS_BASE_AREAS',
    table='CISS4.CISS_BASE_AREAS',
    num_mappers=1,
    dag=dag)

sqoop_import_hdfs_task
