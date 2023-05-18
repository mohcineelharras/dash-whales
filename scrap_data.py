import requests
import time
import pandas as pd
import json

# Etherscan API URL
url = "https://api.etherscan.io/api"

# Your Etherscan API Key
api_key = "VVJFE7IG5WSK8P2UJIJN5MST5UBQEZYVYW"

# Load the JSON file into a dictionary
with open("ressources/dict_tokens_addr.json", "r") as file:
    dict_addresses = json.load(file)

def get_coin_data(tokenSymbol, contractAddr, n):

    # Get the latest block number
    params = {
        "module": "proxy",
        "action": "eth_blockNumber",
        "apikey": api_key
    }
    response = requests.get(url, params=params)
    latest_block = int(response.json()["result"], 16)

    # Initialize an empty DataFrame to store the transactions
    df_transactions = pd.DataFrame()

    # Define the number of transactions to retrieve per API call
    transactions_per_call = 10_000

    # Iterate 'n' times to retrieve 'n' sets of transactions
    for i in range(n):
        # Calculate the start and end blocks for each API call
        start_block = latest_block - (i + 1) * transactions_per_call
        end_block = latest_block - i * transactions_per_call

        # Make the API request
        params = {
            "module": "account",
            "action": "tokentx",
            "contractaddress": contractAddr,
            "startblock": start_block,
            "endblock": end_block,
            "sort": "asc",
            "apikey": api_key
        }
        response = requests.get(url, params=params)

        # Get the transactions data
        transactions = response.json()["result"]

        # Append the transactions to the DataFrame
        df_transactions = pd.concat([df_transactions, pd.DataFrame(transactions)])

        # Add a delay to avoid hitting the API rate limit
        time.sleep(1)

    df_transactions['timeStamp'] = pd.to_datetime(df_transactions['timeStamp'])
    df_transactions['value'] = df_transactions['value'].astype(float) / 1e18

    # Save transactions to a CSV file
    df_transactions.to_csv(f"output/transactions_{tokenSymbol}.csv", sep=";", index=False)
    print(f"All transactions saved to transactions_{tokenSymbol}_.csv")
    print()

# Define the number of blocks to retrieve transactions from
n_blocks = 20000
n_loop = n_blocks // 10_000


for tokenSymbol, contractAddr in dict_addresses.items():
    print(f"Key: {tokenSymbol}, Value: {contractAddr}")
    get_coin_data(tokenSymbol, contractAddr, n_loop)
