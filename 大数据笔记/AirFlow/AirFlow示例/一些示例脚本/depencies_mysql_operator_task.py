#_*_coding:UTF-8_*_
#__author__ = 'laowei'
from airflow import DAG
from airflow.providers.mysql.operators.mysql import MySqlOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
}

dag = DAG(
    'depencies_mysql_operator_dag',
    default_args=default_args,
    schedule_interval=None,
    start_date=days_ago(1),
    tags=['itcast'],
)

insert_sql = r"""
INSERT INTO `test`.`test_airflow_mysql_task`(`task_name`) VALUES ( 'test airflow mysql task6');
INSERT INTO `test`.`test_airflow_mysql_task`(`task_name`) VALUES ( 'test airflow mysql task7');
INSERT INTO `test`.`test_airflow_mysql_task`(`task_name`) VALUES ( 'test airflow mysql task8');
"""

update_sql = r"""
update `test`.`test_airflow_mysql_task` set `task_name` = 'test1',`update_time` = CURRENT_TIMESTAMP  where id = 1;
"""

query_sql=r"""
select * from test.test_airflow_mysql_task;
"""

insert_table_mysql_task = MySqlOperator(
    task_id='mysql_operator_insert_task', 
    mysql_conn_id='mysql-airflow-connection', 
    sql=insert_sql,
    dag=dag
)

update_table_mysql_task = MySqlOperator(
    task_id='mysql_operator_update_task', 
    mysql_conn_id='mysql-airflow-connection', 
    sql=update_sql,
    dag=dag
)

query_table_mysql_task = MySqlOperator(
    task_id='mysql_operator_query_task', 
    mysql_conn_id='mysql-airflow-connection', 
    sql=query_sql,
    dag=dag
)

insert_table_mysql_task << update_table_mysql_task << query_table_mysql_task
