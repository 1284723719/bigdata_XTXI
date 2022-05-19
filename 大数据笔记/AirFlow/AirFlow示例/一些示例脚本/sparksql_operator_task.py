# -*- coding:utf-8 -*-
#__author__ = 'laowei'
from datetime import date

from airflow import DAG
from airflow.providers.apache.spark.operators.spark_sql import SparkSqlOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner':'airflow',
    #'email': ['m137@163.com','5233@qq.com','itcast@itcast.cn'],
    #'email_on_failure': True,
    #'email_on_retry': True,
    #'retries': 1
}

dag = DAG(
    'sparksql_task',
    default_args=default_args,
    schedule_interval="@daily",
    start_date=days_ago(1),
    tags=['itcast']
)

spark_sql_job = SparkSqlOperator(
    sql="select task_id, task_name, create_time,dt from spark_airflow_task;",
    master="local",
    conn_id="sparksql-airflow-connection",
    task_id="sql_job",
    dag=dag
)

spark_sql_job
