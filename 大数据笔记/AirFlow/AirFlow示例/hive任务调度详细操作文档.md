# Hive任务调度

## airflow调度shell执行hive任务

-   hive command execute sql

    ```shell
    # 创建库
    hive -e 'create database hive_airflow_task'
    # 创建表
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
    ;
    ```

-   query_hive_shell_task.py

    ```python
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
        'hive_shell_task',
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
    
    hive_create_db_task << hive_create_table_task
    ```

## 使用HiveOperator执行hive任务

-   添加hive connection

    ![](images/配置airflow远程hive连接.png)

-   使用HiveOperator编写hive任务

    -   hive_operator_task.py

        ```python
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
            'hive_operator_task',
            default_args=default_args,
            schedule_interval="@daily",
            start_date=days_ago(1),
            tags=['itcast']
        )
        
        create_db_hive=r'''
        create database hive_airflow_task;
        '''
        
        create_table_hive=r'''
        create table hive_airflow_task.hive_airflow_task(
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
        
        hive_create_db_task = HiveOperator(
            task_id='hive_create_db_task',
            hql=create_db_hive,
            hive_cli_conn_id='hive-airflow-connection',
            dag=dag)
        
        hive_create_table_task = HiveOperator(
            task_id='hive_create_table_task',
            hql=create_table_hive,
            hive_cli_conn_id='hive-airflow-connection',
            dag=dag)
        
        hive_create_db_task << hive_create_table_task
        ```

    -   错误信息

        ```reStructuredText
        [2021-04-30 17:39:18,024] {base.py:74} INFO - Using connection to: id: hive-airflow-connection. Host: hive.bigdata.cn, Port: 10000, Schema: , Login: root, Password: XXXXXXXX, extra: None
        [2021-04-30 17:39:18,024] {hive.py:157} INFO - Passing HiveConf: {'airflow.ctx.dag_owner': 'airflow', 'airflow.ctx.dag_id': 'hive_operator_task', 'airflow.ctx.task_id': 'hive_create_table_task', 'airflow.ctx.execution_date': '2021-04-30T09:34:27.345930+00:00', 'airflow.ctx.dag_run_id': 'manual__2021-04-30T09:34:27.345930+00:00'}
        [2021-04-30 17:39:18,026] {hive.py:244} INFO - hive -hiveconf airflow.ctx.dag_id=hive_operator_task -hiveconf airflow.ctx.task_id=hive_create_table_task -hiveconf airflow.ctx.execution_date=2021-04-30T09:34:27.345930+00:00 -hiveconf airflow.ctx.dag_run_id=manual__2021-04-30T09:34:27.345930+00:00 -hiveconf airflow.ctx.dag_owner=airflow -hiveconf airflow.ctx.dag_email= -hiveconf mapred.job.name=Airflow HiveOperator task for node1.hive_operator_task.hive_create_table_task.2021-04-30T09:34:27.345930+00:00 -f /tmp/airflow_hiveop_dryk5f7u/tmp0z7ocsjb
        [2021-04-30 17:39:18,032] {taskinstance.py:1455} ERROR - [Errno 2] No such file or directory: 'hive': 'hive'
        ```

    -   解决：配置环境变量

        ```shell
        #JAVA_HOME
        export JAVA_HOME=/opt/jdk1.8.0_141
        export CLASSPATH=$:CLASSPATH:$JAVA_HOME/lib/
        export PATH=$JAVA_HOME/bin:$PATH
        #HADOOP_HOME
        export HADOOP_HOME=/opt/hadoop-2.7.0
        export PATH=${HADOOP_HOME}/sbin:${HADOOP_HOME}/bin:$PATH
        #HIVE_HOME
        export HIVE_HOME=/opt/apache-hive-2.1.0-bin
        export PATH=${HIVE_HOME}/bin:$PATH
        ```

    -   添加测试数据，重跑任务

        ```sql
        insert into hive_airflow_task partition(dt='20210504') values ('hive_001', 'hive task', '2021-05-04 10:30:06')
        ```

        