# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import firestore
# import hashlib

# cred = credentials.Certificate('blockchain-private-key-hema.json')

# app = firebase_admin.initialize_app(cred)

# db = firestore.client()

# def calculate_hash(index, previous_hash, data):
#     value = str(index) + str(previous_hash) + str(data)
#     return hashlib.sha256(value.encode()).hexdigest()

# def set_data(data):
#     current=db.collection("BlockChain").document("current").get().to_dict()
#     current_block_num=current["current_block"]
#     current_block=db.collection("BlockChain").document("Block-"+str(current_block_num)).get().to_dict()
#     current_hash=current_block["current_hash"]
#     current_data=[]
#     ip_columns=['Breathing Problem', 'Fever', 'Dry Cough', 'Sore throat', 'Headache','Fatigue ', 'Gastrointestinal ', 'Abroad travel','Contact with COVID Patient', 'Attended Large Gathering','Visited Public Exposed Places',"timestamp","has Covid"]
#     if current_block_num!=0:
#         for user in current_block["data"]:
#             x={}
#             for key in ip_columns:
#                 x[key]=user[key]
#             current_data.append(x)
#     else:
#         current_data=current_block["data"]
#     prev_hash=current_block["prev_hash"]
#     if len(current_data)==5:
#         new_data=[data]
#         new_hash=calculate_hash("Block-"+str(current_block_num+1),current_hash,new_data)
#         db.collection("BlockChain").document("Block-"+str(current_block_num+1)).set(
#             {
#                 "current_hash":new_hash,
#                 "data": new_data,
#                 "prev_hash": current_hash,
#             },
#             merge=True
#         )
#         db.collection("BlockChain").document("current").update({"current_block":firestore.Increment(1)})
#     else:
#         current_data.append(data)
#         new_hash=calculate_hash("Block-"+str(current_block_num),prev_hash,current_data)
#         db.collection("BlockChain").document("Block-"+str(current_block_num)).set(
#             {
#                 "current_hash":new_hash,
#                 "data": current_data,
#             },
#             merge=True
#         )

# def get_data():
#     docs=db.collection("BlockChain").stream()
#     data={}
#     for doc in docs:
#         if doc.id!="current":
#             data[doc.id]=doc.to_dict()
#     return data

from urllib.parse import urlencode
import requests
import json

def set_data(data):
    params={"query":"set","data":data}
    params=urlencode(params)
    requests.get("https://asia-south1-hod-portal-383002.cloudfunctions.net/BlockChain-firebase", params=params)
    return

def get_data():
    params={"query":"get"}
    params=urlencode(params)
    data=requests.get("https://asia-south1-hod-portal-383002.cloudfunctions.net/BlockChain-firebase", params=params)
    data=json.loads(data.content.decode('utf-8'))
    return data