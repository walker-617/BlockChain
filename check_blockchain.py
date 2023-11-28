import hashlib
from firebase import get_data

blocks=get_data()

def calculate_hash(index, previous_hash, data):
    value = str(index) + str(previous_hash) + str(data)
    return hashlib.sha256(value.encode()).hexdigest()

compromised=-1
for block_num,block in blocks.items():
    data=[]
    if block_num=="Block-0":
        data="genisis block"
    else:
        ip_columns=['Breathing Problem', 'Fever', 'Dry Cough', 'Sore throat', 'Headache','Fatigue ', 'Gastrointestinal ', 'Abroad travel','Contact with COVID Patient', 'Attended Large Gathering','Visited Public Exposed Places',"timestamp","has Covid"]
        for user in block["data"]:
            x={}
            for key in ip_columns:
                x[key]=user[key]
            data.append(x)
    caluculated_hash=calculate_hash(block_num,block["prev_hash"],data)
    if caluculated_hash!=block["current_hash"]:
        compromised=block_num
        break

if compromised!=-1:
    print("!!! Data has been changed in ",compromised," !!!")
else:
    print("Data is not changed.")