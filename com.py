import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import json
import hashlib
import time

class Block: 
    def __init__(self, index, previous_hash, timestamp, data, model_output, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.model_output = model_output
        self.hash = hash

def calculate_hash(index, previous_hash, timestamp, data, model_output):
    value = str(index) + str(previous_hash) + str(timestamp) + str(data) + str(model_output)
    return hashlib.sha256(value.encode()).hexdigest()

def create_genesis_block():
    return Block(0, "0", time.time(), "Genesis Block", "Initial Model Output", calculate_hash(0, "0", time.time(), "Genesis Block", "Initial Model Output"))

def create_new_block(previous_block, data, model_output):
    index = previous_block.index + 1
    timestamp = time.time()
    hash = calculate_hash(index, previous_block.hash, timestamp, data, model_output)
    return Block(index, previous_block.hash, timestamp, data, model_output, hash)

def collect_patient_data(ip_columns):
    print("\nGive patient details. Enter 'yes' or 'no'.")
    patient_data = []
    for i in range(11):
        n = input("\n" + ip_columns[i] + " : ").lower()
        if n == "yes":
            patient_data.append(1)
        elif n == "no":
            patient_data.append(0)
        else:
            print("\nPlease enter 'yes' or 'no'.")
            i = i - 1
    return patient_data

def predict_covid_status(model, patient_data):
    patient_df = pd.DataFrame([patient_data], columns=ip_columns)
    prediction = model.predict(patient_df)
    if prediction[0] == 1:
        return "Patient has Covid"
    else:
        return "Patient has no Covid"

# Load the dataset
da = pd.read_csv("Covid Dataset.csv")
columns_to_drop = ['Running Nose', 'Asthma', 'Chronic Lung Disease', 'Heart Disease',
                   'Diabetes', 'Hyper Tension', 'Family working in Public Exposed Places',
                   'Wearing Masks', 'Sanitization from Market']
da.drop(columns=columns_to_drop, inplace=True)
da.replace({'Yes': 1, 'No': 0}, inplace=True)

# Prepare data for training the model
ip = da.drop("COVID-19", axis=1)
op = da["COVID-19"]
ip_columns = ip.columns
train_x, test_x, train_y, test_y = train_test_split(ip, op, test_size=0.2, stratify=op)

# Train the machine learning model
model = RandomForestClassifier(n_estimators=45)
model.fit(train_x, train_y)

# Create the blockchain and add the genesis block
blockchain = [create_genesis_block()]
previous_block = blockchain[0]

# Collect patient data for each block
num_users_per_block = 2
num_blocks_to_add = 2

for _ in range(num_blocks_to_add):
    block_data = []
    for _ in range(num_users_per_block):
        user_input_data = collect_patient_data(ip_columns)
        result = predict_covid_status(model, user_input_data)

        my_dict = {}
        for i in range(11):
            if user_input_data[i] == 1:
                my_dict[ip_columns[i]] = "Yes"
            elif user_input_data[i] == 0:
                my_dict[ip_columns[i]] = "No"
        print(my_dict)

        json_data = json.dumps(my_dict)
        block_data.append((json_data, result))

    # Combine data from two users into one block
    combined_data = {
        "User1": block_data[0][0],
        "User2": block_data[1][0],
        "Result1": block_data[0][1],
        "Result2": block_data[1][1]
    }

    # Create a new block for each pair of users
    new_block = create_new_block(previous_block, json.dumps(combined_data), "Combined Results")
    blockchain.append(new_block)
    previous_block = new_block

# Print the blockchain
for block in blockchain:
    print(f"Index: {block.index}")
    print(f"Previous Hash: {block.previous_hash}")
    print(f"Timestamp: {block.timestamp}")
    print(f"Data: {block.data}")
    print(f"Model Output: {block.model_output}")
    print(f"Hash: {block.hash}")
    print("\n" + "="*50 + "\n")
