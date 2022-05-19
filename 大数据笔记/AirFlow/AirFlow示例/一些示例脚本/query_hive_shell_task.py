# -*- coding:utf-8 -*-
#__author__ = 'laowei'
from datetime import date, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    # 'depends_on_past': False,
    # 'email': ['airflow@example.com'],
    # 'email_on_failure': False,
    # 'email_on_retry': False,
    # 'retries': 1,
    # 'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2020, 12, 31),
}

dag = DAG(
    dag_id='hive_shell_task',
    default_args=default_args,
    schedule_interval="@daily",
    start_date=days_ago(1),
    tags=['itcast']
)

bash_db_cmd=r'''
hive -e 'create database hive_airflow_task'
'''

bash_table_cmd=r'''
hive -e 
'create table hive_airflow_task.hive_airflow_task(
    task_id string comment 'task id'
    , task_name string comment 'task name'
    , create_time timestamp comment 'task create time'
) comment 'airflow hive test table'
    partitioned by (dt string)
row format delimited
fields terminated by '/001'
location '/data/test/airflow/hive_airflow_task'
;'
'''

hive_create_db_task = BashOperator(
    task_id='hive_create_db_task',
    bash_command=bash_db_cmd,
    dag=dag)

hive_create_table_task = BashOperator(
    task_id='hive_create_table_task',
    bash_command=bash_table_cmd,
    dag=dag)

hive_create_db_task >>  hive_create_table_task
