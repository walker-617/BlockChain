import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

da = pd.read_csv("Covid Dataset.csv")
columns_to_drop = ['Running Nose', 'Asthma', 'Chronic Lung Disease', 'Heart Disease',
                   'Diabetes', 'Hyper Tension', 'Family working in Public Exposed Places',
                   'Wearing Masks', 'Sanitization from Market']
da.drop(columns=columns_to_drop, inplace=True)
da.replace({'Yes': 1, 'No': 0}, inplace=True)

ip = da.drop("COVID-19", axis=1)
op = da["COVID-19"]
ip_columns = ip.columns
train_x, test_x, train_y, test_y = train_test_split(ip, op, test_size=0.2, stratify=op)

model = RandomForestClassifier(n_estimators=45)
model.fit(train_x, train_y)
model_filename = 'covid_model.joblib'
pickle.dump(model, open(model_filename,"wb"))