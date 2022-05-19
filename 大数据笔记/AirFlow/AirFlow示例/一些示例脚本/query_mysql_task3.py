# -*- coding:utf-8 -*-
#__author__ = 'laowei'
from airflow import DAG
from airflow.providers.mysql.operators.mysql import MySqlOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
}

dag = DAG(
    'query_mysql_use_sql3',
    default_args=default_args,
    start_date=days_ago(1),
    template_searchpath=['/root/airflow/dags/query_mysql_task3'],
    tags=['itcast'],
)

query_table_mysql_task = MySqlOperator(
    task_id='query_table_mysql_third', 
    mysql_conn_id='mysql-airflow-connection', 
    sql='test_airflow_mysql_task.sql',
    dag=dag
)
query_table_mysql_task
