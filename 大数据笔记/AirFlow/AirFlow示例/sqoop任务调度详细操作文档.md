# Sqoop任务调度

## bash调度sqoop任务

-   需求1：列出oracle服务中所有的数据库

-   编写脚本

    -   sqoop_listdbs_oracle.py

        ```python
        # -*- coding:utf-8 -*-
        #__author__ = 'laowei'
        from airflow import DAG
        from airflow.operators.bash import BashOperator
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
        
        sqoop_test_task
        ```

-   需求2：导出一个表（CISS4.CISS_BASE_AREAS），到hdfs路径（/data/test/CISS_BASE_AREAS）上

    -   需求对应sqoop脚本

        ```shell
        sqoop import \
        --connect jdbc:oracle:thin:@oracle.bigdata.cn:1521:helowin \
        --username ciss \
        --password 123456 \
        --warehouse-dir /data/test/CISS_BASE_AREAS \
        --table CISS4.CISS_BASE_AREAS -m 1
        ```

    -   任务调度脚本：

        -   import_hdfs_task.py

            ```python
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
            ```

        -   sqoop导数据日志

            <center>
                  <img src="images/sqoop导出oracle表数据到hdfs(上).png" height="320"/>
                  <img src="images/sqoop导出oracle表数据到hdfs(中).png" height="320"/>
                  <img src="images/sqoop导出oracle表数据到hdfs(下).png" height="190"/>
            </center> 

## SqoopOperator调度sqoop任务

-   安装sqoop与airflow集成包

    `pip install apache-airflow-providers-apache-sqoop`

-   创建sqoop的connection

    ![](https://s2.loli.net/2022/05/19/xqYEGKc6N3OHrID.png)

    >   注意：Sqoop环境变量配置

-   调度脚本

    -   sqoop_operator_import_hdfs.py

        ```python
        # -*- coding:utf-8 -*-
        #__author__ = 'laowei'
        from airflow import DAG
        from airflow.providers.apache.sqoop.operators.sqoop import SqoopOperator
        from airflow.utils.dates import days_ago
        
        default_args = {
            'owner': 'airflow',
        }
        
        dag = DAG(
            'sqoop_operator_import_hdfs',
            default_args=default_args,
            schedule_interval=None,
            start_date=days_ago(1),
            tags=['itcast']
        )
        
        sqoop_import_hdfs_task = SqoopOperator(
            task_id='sqoop_operator_import_hdfs_task',
            conn_id='sqoop-airflow-connection',
            cmd_type='import',
            target_dir='/data/sqoop/airflow/CISS_BASE_AREAS',
            table='CISS4.CISS_BASE_AREAS',
            num_mappers=1,
            dag=dag)
        
        sqoop_import_hdfs_task
        ```

        