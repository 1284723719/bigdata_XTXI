from datetime import timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

args = {
    'owner': 'airflow',
    'email': ['5233@qq.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    dag_id='first_bash_operator_new',
    default_args=args,
    start_date=days_ago(2),
    dagrun_timeout=timedelta(minutes=5),
    tags=['itcast']
)

# [START howto_operator_bash]
run_this = BashOperator(
    task_id='echo_first_bash',
    bash_command=echo 'hello airflow!!!',
    dag=dag,
)
run_this