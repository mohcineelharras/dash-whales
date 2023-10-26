import requests
import time
import pandas as pd
import json
import os

# Etherscan API URL
url = "https://api.etherscan.io/api"

# Your Etherscan API Key
api_key = "VVJFE7IG5WSK8P2UJIJN5MST5UBQEZYVYW"

# Create output folder
if not os.path.exists("output"):
    os.makedirs("output")

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
        start_block = latest_block - (n-i) * transactions_per_call
        end_block = latest_block - (n-1-i) * transactions_per_call
        # print((n-1-i) * transactions_per_call)
        # print(transactions_per_call)
        # print("latest_block",latest_block)
        # print("start_block",start_block)
        # print("end_block",end_block)
        # print()
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

    df_transactions['timeStamp'] = pd.to_datetime(df_transactions['timeStamp'].astype(int), unit='s')
    df_transactions['value'] = df_transactions['value'].astype(float) / 1e18
    return df_transactions


# Define the number of blocks to retrieve transactions from
n_blocks = 20000
n_loop = n_blocks // 10_000
for tokenSymbol, contractAddr in dict_addresses.items():
    file = f"output/transactions_{tokenSymbol}.csv"
    print(file)
    if not os.path.exists(file):
        print("Creating file and scrapping data")
        print(f"Key: {tokenSymbol}, Value: {contractAddr}")
        df_transactions = get_coin_data(tokenSymbol, contractAddr, n_loop)
        # Save transactions to a CSV file
        df_transactions = df_transactions.drop(["confirmations","input"],axis=1)
        df_transactions_no_dup = df_transactions.drop_duplicates(subset="hash")
        df_transactions_no_dup.to_csv(file, sep=";", index=False)
        print(f"All transactions saved to transactions_{tokenSymbol}_.csv")
        print("shape of created transaction dataframe",df_transactions_no_dup.shape)
        print()
    else:
        # UPDATE THE DATA
        print("Completion of data")
        # load file
        df_temp = pd.read_csv(file,sep=";")
        print("shape of existing file ",df_temp.shape)
        # sort descendenly by block number
        df_temp = df_temp.sort_values("blockNumber", ascending=False)
        # get start block for new api call which is last time last block
        start_block = df_temp["blockNumber"].iloc[0]
        # Get the latest block number
        params = {
            "module": "proxy",
            "action": "eth_blockNumber",
            "apikey": api_key
        }
        # api call
        response = requests.get(url, params=params)
        # convert to int
        latest_block = int(response.json()["result"], 16)
        # determine number of loops
        n_loop_to_concat = ((latest_block-start_block)//10000) + 1
        df_transactions = get_coin_data(df_temp["tokenSymbol"].unique(), df_temp["contractAddress"].unique(), n_loop_to_concat)
        #print("shape of latest downloaded df_transactions before merging", df_transactions.shape)
        # Append the transactions to the DataFrame
        df_latest = pd.concat([df_transactions, df_temp]).drop(["confirmations","input"],axis=1)
        df_latest_no_dup = df_latest.drop_duplicates(subset="hash")
        print("shape of latest df_transactions after merging and without duplicates", df_latest_no_dup.shape)
        print("Number of new transactions registered", df_latest_no_dup.shape[0]-df_temp.shape[0])
        print()
        df_latest_no_dup.loc[:,"blockNumber"] = df_latest_no_dup["blockNumber"].astype(int)
        #print(df_latest)
        df_latest_no_dup = df_latest_no_dup.sort_values(by = "blockNumber")
        df_latest_no_dup.to_csv(file, sep=";", index=False)
        break

