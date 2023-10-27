import requests
import time
import pandas as pd
import json
import os
from utils.functions import update_and_save_csv

# Create output folder
if not os.path.exists("output"):
    os.makedirs("output")

# Load the JSON file into a dictionary
print(os.getcwd())
with open("ressources/dict_tokens_addr.json", "r") as file:
    dict_addresses = json.load(file)

update_and_save_csv(dict_addresses)