from airflow import DAG
#from datetime import datetime
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from random import randint
from airflow.utils.dates import days_ago
import json
import os, sys
sys.path.append('..')  # Add the parent folder to the sys.path
print(os.getcwd())
from utils.functions import get_coin_data, update_and_save_csv
#
# Etherscan API URL
url = "https://api.etherscan.io/api"

# Your Etherscan API Key
api_key = "VVJFE7IG5WSK8P2UJIJN5MST5UBQEZYVYW"

# Create output folder
if not os.path.exists("../output"):
    os.makedirs("../output")

# Load the JSON file into a dictionary
print(os.getcwd())
with open("../ressources/dict_tokens_addr.json", "r") as file:
    dict_addresses = json.load(file)


args = {
    "owner":"mrxdey",
    "start_date":days_ago(30),
}

def check_what_happened(ti):
    L_created,L_updated = ti.xcom_pull(task_ids=["save_data"])
    if (len(L_created)>len(L_updated)):
        return "mostly created"
    return "mostly updated"

with DAG(dag_id="etherscan",
         default_args=args,
         schedule="@hourly",
         catchup=True) as dag:
    
    scrap_data_etherscan = PythonOperator(
        task_id="scrap_data_etherscan",
        python_callable=get_coin_data
    )
    
    save_data = PythonOperator(
        task_id="save_data",
        python_callable=update_and_save_csv
    )


    choose_best_model= BranchPythonOperator(
        task_id="check_what_happened",
        python_callable=check_what_happened
    )
    
    update = BashOperator(
        task_id="update",
        bash_command="echo 'mostly updated'"
    )
    
    create = BashOperator(
        task_id="create",
        bash_command="echo 'mostly created"
    )
    
    [scrap_data_etherscan,save_data] >> choose_best_model >> [create, update]