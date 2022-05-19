# Mysql任务调度

-   创建测试库，添加数据

    ```sql
    -- 创建测试库（root用户）
    create DATABASE test;
    -- 创建测试表（root用户）
    CREATE TABLE test.test_airflow_mysql_task(
    	id int(11) primary key not null auto_increment COMMENT '注解',
    	task_name VARCHAR(255) COMMENT '任务名称',
    	create_name VARCHAR(25) DEFAULT 'airflow' COMMENT '创建人',
    	update_name VARCHAR(25) DEFAULT 'airflow' COMMENT '修改人',
    	crete_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    	update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '修改时间'
    )
    
    -- 插入数据
    INSERT INTO `test`.`test_airflow_mysql_task`(`id`, `task_name`, `create_name`, `update_name`, `crete_time`, `update_time`) VALUES (1, '测试airflow调度mysql任务', 'airflow', 'airflow', '2021-04-19 15:17:08', '2021-04-19 15:17:08');
    -- 插入数据，简化版
    INSERT INTO `test`.`test_airflow_mysql_task`(`task_name`) VALUES ( '测试airflow调度mysql任务2');
    ```

-   页面添加connection

    ![](https://s2.loli.net/2022/05/19/pM8OZla3b6jBmVz.png)

-   创建airflow任务，实现以下2个需求：

    -   需求1：创建mysql查询测试表任务(单个sql任务)

        1.  sql

            ```sql
            select * from test.test_airflow_mysql_task;
            ```

        2.  airflow脚本

            -   注意`mysql_conn_id`为上一步添加airflow的mysql连接名称：mysql-airflow-connection

                ```python
                # -*- coding:utf-8 -*-
                #__author__ = 'laowei'
                from airflow import DAG
                from airflow.providers.mysql.operators.mysql import MySqlOperator
                from airflow.utils.dates import days_ago
                
                default_args = {
                    'owner': 'airflow',
                }
                
                dag = DAG(
                    'query_mysql_use_sql',
                    default_args=default_args,
                    start_date=days_ago(1),
                    tags=['itcast'],
                )
                
                query_table_mysql_task = MySqlOperator(
                    task_id='query_table_mysql', 
                    mysql_conn_id='mysql_airflow_connection', 
                    sql=r"""select * from test.test_airflow_mysql_task;""",
                    dag=dag
                )
                query_table_mysql_task
                ```

        3.  运行日志：

            ![](https://s2.loli.net/2022/05/19/C675OTh8FxArI4p.png)

    -   需求1实现的第二种方式

        -   本地创建好sql脚本执行

            -   test_airflow_mysql_task.sql

                -   内容：select * from test.test_airflow_mysql_task;

                    ```python
                    mysql_task = MySqlOperator(
                        task_id='create_table_mysql_external_file',
                        mysql_conn_id='mysql_conn_id',
                        # sql文件存放在dags目录下，指定其他路径，将会使用到jinja2模板
                        sql='drop_table.sql',
                        dag=dag,
                    )
                    ```

        -   query_mysql_task2.py

            ```python
            # -*- coding:utf-8 -*-
            #__author__ = 'laowei'
            from airflow import DAG
            from airflow.providers.mysql.operators.mysql import MySqlOperator
            from airflow.utils.dates import days_ago
            
            default_args = {
                'owner': 'airflow',
            }
            
            dag = DAG(
                'query_mysql_use_sql2',
                default_args=default_args,
                start_date=days_ago(1),
                tags=['itcast'],
            )
            
            query_table_mysql_task = MySqlOperator(
                task_id='query_table_mysql_second', 
                mysql_conn_id='mysql-airflow-connection', 
                sql='test_airflow_mysql_task.sql',
                dag=dag
            )
            query_table_mysql_task
            ```

        -   sql文件在dag任务中配置绝对路径（不使用jinja2模板）

            -   使用template_searchpath 

                - query_mysql_task3.py

                    ```python
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
                    ```

    -   需求2：创建mysql插入数据到测试表，然后更新数据，查询数据

        -   sql

            ```sql
            -- 插入三条数据
            INSERT INTO `test`.`test_airflow_mysql_task`(`task_name`) VALUES ( '测试airflow调度mysql任务3');
            INSERT INTO `test`.`test_airflow_mysql_task`(`task_name`) VALUES ( '测试airflow调度mysql任务4');
            INSERT INTO `test`.`test_airflow_mysql_task`(`task_name`) VALUES ( '测试airflow调度mysql任务5');
            -- 更新已存在的第一条数据（更新任务名称为：test1、更新时间为执行更新记录的时间）
            update `test`.`test_airflow_mysql_task` set `task_name` = '测试1',`update_time` = CURRENT_TIMESTAMP  where id = 1;
            -- 查询全部数据
            select * from test.test_airflow_mysql_task;
            ```

        -   调度任务脚本

            -   depencies_mysql_operator_task.py

                ```mysql
                # -*- coding:utf-8 -*-
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
                INSERT INTO `test`.`test_airflow_mysql_task`(`task_name`) VALUES ( 'test airflow mysql task3');
                INSERT INTO `test`.`test_airflow_mysql_task`(`task_name`) VALUES ( 'test airflow mysql task4');
                INSERT INTO `test`.`test_airflow_mysql_task`(`task_name`) VALUES ( 'test airflow mysql task5');
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
                
                insert_table_mysql_task << update_table_mysql_task << query_table_mysql_tas
                ```

                