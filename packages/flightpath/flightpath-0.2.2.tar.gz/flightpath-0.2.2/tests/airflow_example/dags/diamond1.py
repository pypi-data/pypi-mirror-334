# An example dag with 200 tasks
import time
import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator


with DAG(
    "diamond1",
    description="An example dag with a diamond shape",
    schedule_interval="*/10 * * * *",
    start_date=datetime.datetime(2020, 1, 1),
    catchup=False,
) as dag:

    def fast():
        pass

    def slow():
        time.sleep(2)

    fork = [
        PythonOperator(task_id="fast_path", python_callable=fast),
        PythonOperator(task_id="slow_path", python_callable=slow),
    ]

    task_1 = DummyOperator(task_id="task_1")
    task_2 = DummyOperator(task_id="task_2")

    task_1 >> fork >> task_2

    prev_task = task_2

    # for i in range(3, 200):
    #     next_task = DummyOperator(task_id=f'task_{i}')
    #     prev_task >> next_task
    #     prev_task = next_task

    prev_task >> DummyOperator(task_id="end")
