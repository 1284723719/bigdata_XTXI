# -*- coding:utf-8 -*-
#__author__ = 'laowei'
from airflow import DAG
from airflow.operators.bash import BashOperator
#from airflow.providers.apache.sqoop.operators.sqoop import SqoopOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
}

dag = DAG(
    'sqoop_list_databases',
    default_args=default_args,
    schedule_interval=None,
    start_date=days_ago(1),
    tags=['itcast']
)

bash_cmd=r'''
/opt/sqoop/bin/sqoop list-databases \
--connect jdbc:oracle:thin:@oracle.bigdata.cn:1521:helowin \
--username ciss \
--password 123456
'''
sqoop_test_task = BashOperator(
    task_id='sqoop_list_database_task',
    bash_command=bash_cmd,
    dag=dag)
#sqoop_test_task = SqoopOperator(
#    task_id='sqoop_test', 
#    conn_id='sqoop-airflow-connection',
#    cmd_type="list-databases" 
#    dag=dag
#)
sqoop_test_task
