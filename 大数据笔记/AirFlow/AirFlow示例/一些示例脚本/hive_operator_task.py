# -*- coding:utf-8 -*-
#__author__ = 'laowei'
from datetime import date, timedelta

from airflow import DAG
from airflow.providers.apache.hive.operators.hive import HiveOperator
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
    'hive_operator_task',
    default_args=default_args,
    schedule_interval="@daily",
    start_date=days_ago(1),
    tags=['itcast']
)

create_db_hive=r'''
create database hive_airflow_task2;
'''

create_table_hive=r'''
create table hive_airflow_task.hive_airflow_task2(
    task_id string comment 'task id'
    , task_name string comment 'task name'
    , create_time timestamp comment 'task create time'
) comment 'airflow hive test table'
    partitioned by (dt string)
row format delimited
fields terminated by '/001'
location '/data/test/airflow/hive_airflow_task'
;
'''

#hive_create_db_task = HiveOperator(
#    task_id='hive_create_db_task',
#    hql=create_db_hive,
#    hive_cli_conn_id='hive-airflow-connection',
#    dag=dag)

hive_create_table_task = HiveOperator(
    task_id='hive_create_table_task',
    hql='select * from hive_airflow_task.hive_airflow_task',
    hive_cli_conn_id='hive-airflow-connection',
    mapred_job_name='hive_create_table_job',
    mapred_queue_priority='NORMAL',
    #hiveconfs={'fs.defaultFS':'hdfs://hadoop.bigdata.cn:9000','hive.server2.thrift.bind.host':'hive.bigdata.cn'},
    dag=dag)

hive_create_table_task
