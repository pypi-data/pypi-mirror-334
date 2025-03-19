# An example dag with 200 tasks
import time
from datetime import datetime

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.sensors.external_task_sensor import ExternalTaskSensor

with DAG(
    "diamond2",
    description="An example dag with a diamond shape",
    schedule_interval="*/10 * * * *",
    start_date=datetime(2020, 1, 1),
    catchup=False,
) as dag:

    def fast():
        pass

    def slow():
        time.sleep(10)

    fork = [
        PythonOperator(task_id="fast_path", python_callable=fast),
        PythonOperator(task_id="slow_path_1", python_callable=slow),
        PythonOperator(task_id="slow_path_2", python_callable=slow),
        PythonOperator(task_id="slow_path_3", python_callable=slow),
        PythonOperator(task_id="slow_path_4", python_callable=slow),
        PythonOperator(task_id="slow_path_5", python_callable=slow),
        PythonOperator(task_id="slow_path_6", python_callable=slow),
        PythonOperator(task_id="slow_path_7", python_callable=slow),
        PythonOperator(task_id="slow_path_8", python_callable=slow),
        PythonOperator(task_id="slow_path_9", python_callable=slow),
        PythonOperator(task_id="slow_path_10", python_callable=slow),
        PythonOperator(task_id="slow_path_11", python_callable=slow),
        PythonOperator(task_id="slow_path_12", python_callable=slow),
        PythonOperator(task_id="slow_path_13", python_callable=slow),
        PythonOperator(task_id="slow_path_14", python_callable=slow),
        PythonOperator(task_id="slow_path_15", python_callable=slow),
        PythonOperator(task_id="slow_path_16", python_callable=slow),
        PythonOperator(task_id="slow_path_17", python_callable=slow),
        PythonOperator(task_id="slow_path_18", python_callable=slow),
        PythonOperator(task_id="slow_path_19", python_callable=slow),
        PythonOperator(task_id="slow_path_20", python_callable=slow),
    ]

    task_1 = DummyOperator(task_id="task_1")
    task_2 = DummyOperator(task_id="task_2")

    # Add the wait task
    wait_for_diamond1 = ExternalTaskSensor(
        task_id="wait_for_diamond1",
        external_dag_id="diamond1",
        external_task_id="end",
        timeout=600,
        poke_interval=60,
        mode="poke",
    )

    wait_for_diamond1 >> task_1 >> fork >> task_2

    prev_task = task_2

    # for i in range(3, 200):
    #     next_task = DummyOperator(task_id=f'task_{i}')
    #     prev_task >> next_task
    #     prev_task = next_task

    prev_task >> DummyOperator(task_id="end")
