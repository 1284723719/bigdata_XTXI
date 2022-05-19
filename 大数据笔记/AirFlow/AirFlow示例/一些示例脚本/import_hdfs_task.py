# -*- coding:utf-8 -*-
#__author__ = 'laowei'
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
}

dag = DAG(
    'sqoop_import_hdfs',
    default_args=default_args,
    schedule_interval=None,
    start_date=days_ago(1),
    tags=['itcast']
)

bash_cmd=r'''
/opt/sqoop/bin/sqoop import \
--connect jdbc:oracle:thin:@oracle.bigdata.cn:1521:helowin \
--username ciss \
--password 123456 \
--warehouse-dir /data/test/airflow/CISS_BASE_AREAS \
--table CISS4.CISS_BASE_AREAS -m 1
'''
sqoop_import_hdfs_task = BashOperator(
    task_id='sqoop_import_hdfs_task',
    bash_command=bash_cmd,
    dag=dag)

sqoop_import_hdfs_task
