from airflow import DAG, Dataset
from airflow.decorators import task
from datetime import datetime

my_file = Dataset("/tmp/my_file.txt")
my_file_2 = Dataset("/tmp/my_file_2.txt")

with DAG(
    dag_id = "producer",
    schedule = "@daily",
    start_date = datetime(2024,12,30),
    catchup = False
):

    # dataset과 상호작용하는 DAG 생성 시 dataset 정의 후 Decorator에 지정
    # update_dataset 작업 성공 시 데이터셋에 의존하는 DAG가 자동으로 my_file 트리거함
    @task(outlets = [my_file])
    def update_dataset():
        with open(my_file.uri, "a+") as f:
            f.write("producer update")

    @task(outlets = [my_file_2])
    def update_dataset_2():
        with open(my_file_2.uri, "a+") as f:
            f.write("producer update")


    update_dataset() >> update_dataset_2()