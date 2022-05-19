# oracle任务调度

-   页面添加oracle connection

    -   用户操作页面，Admin->Connections->add（+号）

        -   在extra中，添加内容，给定服务监听（主机和ip都可以作为host或dsn）

            - `{"dsn":"192.168.10.100","service_name":"helowin"}`

            ![](https://s2.loli.net/2022/05/19/1Q2YAG5DJbh7FPO.png)

    -   airflow命令添加connection（选其一）

        ```shell
        airflow connections add 'oracle-airflow-connection' \
            --conn-uri 'oracle://ciss:123456@192.168.10.100:1521/helowin'
        ```

-   需求：每天查询一次oracle某张（ciss4.ciss_base_areas）已存在的表

    -   编写oracle调度脚本：query_oracle_task.py

        ```python
        # -*- coding:utf-8 -*-
        #__author__ = 'laowei'
        from datetime import timedelta
        
        from airflow import DAG
        
        from airflow.operators.bash import BashOperator
        from airflow.utils.dates import days_ago
        from airflow.providers.oracle.operators.oracle import OracleOperator
        
        default_args = {
            'owner': 'airflow',
            'depends_on_past': False,
            #'email': ['airflow@example.com'],
            #'email_on_failure': False,
            #'email_on_retry': False,
            'retries': 1,
            'retry_delay': timedelta(minutes=30)
        }
        
        dag = DAG(
            'oracle_operator_dag',
            default_args=default_args,
            description='query one oracle table task of dag',
            schedule_interval=timedelta(days=1),
            start_date=days_ago(1),
            tags=['itcast'],
        )
        
        query_oracle_task = OracleOperator(
            task_id = 'oracle_operator_task',
            sql = 'select * from ciss4.ciss_base_areas',
            oracle_conn_id = 'oracle-airflow-connection',
            autocommit = True,
            dag=dag)
        
        query_oracle_task
        ```

    -   报错：

        - 找不到oracle客户端

            - 由于oracle使用docker安装，安装目录宿主机不可以见，因此找不到oracle的客户端信息

                ![](https://s2.loli.net/2022/05/19/LO9m5f6YXdyVTxI.png)

        - 从oracle的docker容器中复制dbhome_2目录以及内容

            ```shell
            # 宿主机上创建目录
            mkdir /home/oracle/app/oracle/product/11.2.0/
            # 使用docker命令复制dbhome_2目录以及内容
            docker cp oracle:/home/oracle/app/oracle/product/11.2.0/dbhome_2/ /home/oracle/app/oracle/product/11.2.0/
            ```

    -   再次运行调度oracle的任务

        ![](https://s2.loli.net/2022/05/19/aHKIwMFVTNkrCDx.png)