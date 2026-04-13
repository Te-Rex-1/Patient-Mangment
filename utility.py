import json


file_path='patients.json'
def load_data():
    with open(file_path, 'r') as f:
        data = json.load(f)

    return data
def save_data(data):
    with open(file_path,'w') as f:
        json.dump(data,f)