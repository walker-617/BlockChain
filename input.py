import pandas as pd
import time
import pickle
from firebase import set_data

def collect_patient_data(ip_columns):
    print("\nGive patient details. Enter 'yes' or 'no'.")
    patient_data = []
    i=0
    while i<11:
        n = input("\n" + ip_columns[i] + " : ").lower()
        if n == "yes" or n=="no":
            patient_data.append(n)
        else:
            print("\nPlease enter 'yes' or 'no'.")
            i = i - 1
        i=i+1
    return patient_data

def predict_covid_status(model, patient_data):

    converted_list = [1 if item.lower() == 'yes' else 0 for item in patient_data]

    patient_df = pd.DataFrame([converted_list], columns=ip_columns)
    prediction = model.predict(patient_df)
    if prediction[0] == 1:
        return "Patient has Covid"
    else:
        return "Patient has no Covid"
    
model_filename = 'covid_model.joblib'
model=pickle.load(open(model_filename,"rb"))
ip_columns=['Breathing Problem', 'Fever', 'Dry Cough', 'Sore throat', 'Headache','Fatigue ', 'Gastrointestinal ', 'Abroad travel','Contact with COVID Patient', 'Attended Large Gathering','Visited Public Exposed Places']

user_input_data = collect_patient_data(ip_columns)
result = predict_covid_status(model, user_input_data)

time_struct = time.localtime()
timestamp_str = time.strftime("%I:%M:%S %p %d/%m/%Y", time_struct)

data=dict(zip(ip_columns,user_input_data))
data["timestamp"]=timestamp_str
data["has Covid"]=result
set_data(data)
