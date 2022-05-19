# Spark任务

-   安装spark程序包

    ```shell
    pip install apache-airflow-providers-apache-spark
    
    ############ 安装成功信息 #############
    #Successfully built pyspark
    #Installing collected packages: py4j, pyspark, apache-airflow-providers-apache-spark
    #Successfully installed apache-airflow-providers-apache-spark-1.0.2 py4j-0.10.9 pyspark-3.1.1
    ```

-   SparkSqlOperator

    -   配置sparksql connection

        ![image-20210505132443637](https://s2.loli.net/2022/05/19/jx8uhK6Zpy3BSaL.png)

    -   使用SparkSqlOperator，编写sparksql任务脚本

        -   sparksql_operator_task.py

            ```python
            # -*- coding:utf-8 -*-
            #__author__ = 'laowei'
            from datetime import date
            
            from airflow import DAG
            from airflow.providers.apache.spark.operators.spark_sql import SparkSqlOperator
            from airflow.utils.dates import days_ago
            
            default_args = {
                'owner':'airflow'
            }
            
            dag = DAG(
                'sparksql_task',
                default_args=default_args,
                schedule_interval="@daily",
                start_date=days_ago(1),
                tags=['itcast']
            )
            
            spark_sql_job = SparkSqlOperator(
                sql="SELECT * FROM hive_airflow_task.hive_airflow_task",
                master="local",
                conn_id="sparksql-airflow-connection",
                task_id="sql_job",
                dag=dag
            )
            
            spark_sql_job
            ```

    -   测试数据(需要hadoop环境、hive环境以及相关支持)

        ```sql
        insert into spark_airflow_task partition(dt='20210504') values ('spark_001', 'spark task', '2021-05-04 11:32:06')
        ```

    -   错误信息

        ```shell
        [2021-05-04 11:40:59,628] {base.py:74} INFO - Using connection to: id: sparksql-airflow-connection. Host: spark.bigdata.cn, Port: 10001, Schema: hive_airflow_task, Login: root, Password: XXXXXXXX, extra: None
        [2021-05-04 11:41:00,565] {spark_sql.py:164} INFO - b'Using properties file: null\n'
        [2021-05-04 11:41:00,693] {spark_sql.py:164} INFO - b'Exception in thread "main" org.apache.spark.SparkException: When running with master \'yarn\' either HADOOP_CONF_DIR or YARN_CONF_DIR must be set in the environment.\n'
        [2021-05-04 11:41:00,693] {spark_sql.py:164} INFO - b'\tat org.apache.spark.deploy.SparkSubmitArguments.error(SparkSubmitArguments.scala:631)\n'
        ```

    -   配置环境变量

        ```shell
        #SPARK_HOME
        export SPARK_HOME=/opt/spark-2.4.7-bin-hadoop2.7
        export PATH=${SPARK_HOME}/bin:${SPARK_HOME}/sbin:$PATH
        #HADOOP_CONF
        export HADOOP_CONF_DIR=/opt/hadoop-2.7.0/etc/hadoop
        ```

    -   远程连接hadoop的yarn（yarn模式）

        ```reStructuredText
        *** Reading local file: /root/airflow/logs/sparksql_task/sql_job/2021-05-04T03:45:56.762135+00:00/1.log
        [2021-05-04 11:45:57,806] {taskinstance.py:851} INFO - Dependencies all met for <TaskInstance: sparksql_task.sql_job 2021-05-04T03:45:56.762135+00:00 [queued]>
        [2021-05-04 11:45:57,818] {taskinstance.py:851} INFO - Dependencies all met for <TaskInstance: sparksql_task.sql_job 2021-05-04T03:45:56.762135+00:00 [queued]>
        [2021-05-04 11:45:57,818] {taskinstance.py:1042} INFO - 
        --------------------------------------------------------------------------------
        [2021-05-04 11:45:57,818] {taskinstance.py:1043} INFO - Starting attempt 1 of 1
        [2021-05-04 11:45:57,818] {taskinstance.py:1044} INFO - 
        --------------------------------------------------------------------------------
        [2021-05-04 11:45:57,826] {taskinstance.py:1063} INFO - Executing <Task(SparkSqlOperator): sql_job> on 2021-05-04T03:45:56.762135+00:00
        [2021-05-04 11:45:57,828] {standard_task_runner.py:52} INFO - Started process 10766 to run task
        [2021-05-04 11:45:57,832] {standard_task_runner.py:76} INFO - Running: ['airflow', 'tasks', 'run', 'sparksql_task', 'sql_job', '2021-05-04T03:45:56.762135+00:00', '--job-id', '4690', '--pool', 'default_pool', '--raw', '--subdir', 'DAGS_FOLDER/sparksql_operator_task.py', '--cfg-path', '/tmp/tmp6y5v1j1s', '--error-file', '/tmp/tmpim2me2_q']
        [2021-05-04 11:45:57,832] {standard_task_runner.py:77} INFO - Job 4690: Subtask sql_job
        [2021-05-04 11:45:57,857] {logging_mixin.py:104} INFO - Running <TaskInstance: sparksql_task.sql_job 2021-05-04T03:45:56.762135+00:00 [running]> on host node1.bigdata.cn
        [2021-05-04 11:45:57,878] {logging_mixin.py:104} WARNING - /anaconda/anaconda3/lib/python3.7/site-packages/sqlalchemy/sql/coercions.py:521 SAWarning: Coercing Subquery object into a select() for use in IN(); please pass a select() construct explicitly
        [2021-05-04 11:45:57,884] {taskinstance.py:1257} INFO - Exporting the following env vars:
        AIRFLOW_CTX_DAG_OWNER=airflow
        AIRFLOW_CTX_DAG_ID=sparksql_task
        AIRFLOW_CTX_TASK_ID=sql_job
        AIRFLOW_CTX_EXECUTION_DATE=2021-05-04T03:45:56.762135+00:00
        AIRFLOW_CTX_DAG_RUN_ID=manual__2021-05-04T03:45:56.762135+00:00
        [2021-05-04 11:45:57,932] {base.py:74} INFO - Using connection to: id: sparksql-airflow-connection. Host: spark.bigdata.cn, Port: 10001, Schema: hive_airflow_task, Login: root, Password: XXXXXXXX, extra: None
        [2021-05-04 11:45:58,549] {spark_sql.py:164} INFO - b'Using properties file: /opt/spark-2.4.7-bin-hadoop2.7/conf/spark-defaults.conf\n'
        [2021-05-04 11:46:41,894] {spark_sql.py:164} INFO - b'21/05/04 11:46:41 INFO ipc.Client: Retrying connect to server: hadoop.bigdata.cn/172.33.0.121:8032. Already tried 0 time(s); retry policy is RetryUpToMaximumCountWithFixedSleep(maxRetries=10, sleepTime=1000 MILLISECONDS)\n'
        
        [2021-05-04 11:48:02,930] {spark_sql.py:164} INFO - b'21/05/04 11:48:02 INFO ipc.Client: Retrying connect to server: hadoop.bigdata.cn/172.33.0.121:8032. Already tried 1 time(s); retry policy is RetryUpToMaximumCountWithFixedSleep(maxRetries=10, sleepTime=1000 MILLISECONDS)\n'
        [2021-05-04 11:48:03,931] {spark_sql.py:164} INFO - b'21/05/04 11:48:03 INFO ipc.Client: Retrying connect to server: hadoop.bigdata.cn/172.33.0.121:8032. Already tried 2 time(s); retry policy is RetryUpToMaximumCountWithFixedSleep(maxRetries=10, sleepTime=1000 MILLISECONDS)\n'
        [2021-05-04 11:48:04,933] {spark_sql.py:164} INFO - b'21/05/04 11:48:04 INFO ipc.Client: Retrying connect to server: hadoop.bigdata.cn/172.33.0.121:8032. Already tried 3 time(s); retry policy is RetryUpToMaximumCountWithFixedSleep(maxRetries=10, sleepTime=1000 MILLISECONDS)\n'
        [2021-05-04 11:48:05,935] {spark_sql.py:164} INFO - b'21/05/04 11:48:05 INFO ipc.Client: Retrying connect to server: hadoop.bigdata.cn/172.33.0.121:8032. Already tried 4 time(s); retry policy is RetryUpToMaximumCountWithFixedSleep(maxRetries=10, sleepTime=1000 MILLISECONDS)\n'
        [2021-05-04 11:48:06,937] {spark_sql.py:164} INFO - b'21/05/04 11:48:06 INFO ipc.Client: Retrying connect to server: hadoop.bigdata.cn/172.33.0.121:8032. Already tried 5 time(s); retry policy is RetryUpToMaximumCountWithFixedSleep(maxRetries=10, sleepTime=1000 MILLISECONDS)\n'
        [2021-05-04 11:48:07,938] {spark_sql.py:164} INFO - b'21/05/04 11:48:07 INFO ipc.Client: Retrying connect to server: hadoop.bigdata.cn/172.33.0.121:8032. Already tried 6 time(s); retry policy is RetryUpToMaximumCountWithFixedSleep(maxRetries=10, sleepTime=1000 MILLISECONDS)\n'
        [2021-05-04 11:48:08,941] {spark_sql.py:164} INFO - b'21/05/04 11:48:08 INFO ipc.Client: Retrying connect to server: hadoop.bigdata.cn/172.33.0.121:8032. Already tried 7 time(s); retry policy is RetryUpToMaximumCountWithFixedSleep(maxRetries=10, sleepTime=1000 MILLISECONDS)\n'
        [2021-05-04 11:48:09,942] {spark_sql.py:164} INFO - b'21/05/04 11:48:09 INFO ipc.Client: Retrying connect to server: hadoop.bigdata.cn/172.33.0.121:8032. Already tried 8 time(s); retry policy is RetryUpToMaximumCountWithFixedSleep(maxRetries=10, sleepTime=1000 MILLISECONDS)\n'
        [2021-05-04 11:48:10,945] {spark_sql.py:164} INFO - b'21/05/04 11:48:10 INFO ipc.Client: Retrying connect to server: hadoop.bigdata.cn/172.33.0.121:8032. Already tried 9 time(s); retry policy is RetryUpToMaximumCountWithFixedSleep(maxRetries=10, sleepTime=1000 MILLISECONDS)\n'
        ```

    -   spark(local模式)

        ![](https://s2.loli.net/2022/05/19/jIBzFfbCLqpyMrx.png)



-   了解：使用jdbc连接hiveql、sparksql

    -   安装jdbc依赖

        `pip install apache-airflow-providers-jdbc`

    -   官方参考文档

        -   https://airflow.apache.org/docs/apache-airflow-providers-jdbc/stable/operators.html