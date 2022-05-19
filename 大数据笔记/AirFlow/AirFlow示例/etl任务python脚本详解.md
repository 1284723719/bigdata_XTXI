# ETL任务调度

-   python脚本解释

    -   ETL:extract、transform、load

    ```python
    # -*- coding:utf-8 -*-
    #__author__ = 'laowei'
    import json
    
    # The DAG object; we'll need this to instantiate a DAG
    from airflow import DAG
    
    # Operators; we need this to operate!
    from airflow.operators.python import PythonOperator
    from airflow.utils.dates import days_ago
    # These args will get passed on to each operator
    # You can override them on a per-task basis during operator initialization
    default_args = {
        'owner': 'airflow',
    }
    with DAG(
        'python_etl_dag',
        default_args=default_args,
        description='DATA ETL DAG',
        schedule_interval=None,
        start_date=days_ago(2),
        tags=['itcast'],
    ) as dag:
        dag.doc_md = __doc__
        def extract(**kwargs):
            ti = kwargs['ti']
            # json格式:{"订单ID", 订单金额}
            data_string = '{"1001": 301.27, "1002": 433.21, "1003": 502.22, "1004": 606.65, "1005": 777.03}'
            # 将数据放到xcom中
            ti.xcom_push('order_data', data_string)
        def transform(**kwargs):
            ti = kwargs['ti']
            # 从xcom中加载数据
            extract_data_string = ti.xcom_pull(task_ids='extract', key='order_data')
            order_data = json.loads(extract_data_string)
            # 计算订单金额总数
            total_order_value = 0
            for value in order_data.values():
                total_order_value += value
            # 组装订单金额总数为json格式
            total_value = {"total_order_value": total_order_value}
            # 字符串转json
            total_value_json_string = json.dumps(total_value)
            # 把订单金额结果数据放入xcom中
            ti.xcom_push('total_order_value', total_value_json_string)
        def load(**kwargs):
            ti = kwargs['ti']
            # 从xcom中得到上一任务的订单金额结果数据
            total_value_string = ti.xcom_pull(task_ids='transform', key='total_order_value')
            total_order_value = json.loads(total_value_string)
            # 打印订单金额结果数据
            print(total_order_value)
        extract_task = PythonOperator(
            task_id='extract',
            python_callable=extract,
        )
        extract_task.doc_md = """\
    #### Extract Task：
    1.该提取任务为其余数据管道准备好数据。
    2.通过读取JSON字符串来模拟获取数据。
    3.将这些数据放入xcom(airflow数据传递工具)，作为下一个任务输入数据，进行处理。
    """
    
        transform_task = PythonOperator(
            task_id='transform',
            python_callable=transform,
        )
        transform_task.doc_md = """\
    #### Transform task：
    1.该转换任务从xcom中收集订单数据并计算订单总价值
    2.然后将计算后的结果值放入到xcom中，传递给下一个任务处理。
    """
    
        load_task = PythonOperator(
            task_id='load',
            python_callable=load,
        )
        load_task.doc_md = """\
    #### Load task：
    该加载任务，通过xcom中获得转换任务结果，只是打印出结果到控制台，并未保存结果数据。
    """
    #### 定义ETL任务依赖关系：抽取数据任务 -> 转换任务 -> 加载任务
        extract_task >> transform_task >> load_task
    ```