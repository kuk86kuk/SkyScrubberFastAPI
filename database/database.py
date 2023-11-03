import os
import json



def get_data(number: int ):
    data = fake_database(number)
    return data
    


def fake_database(number: int):
    with open('database/fake_database.json') as f:
         data = json.load(f)
         data_json = []
         for i in data['data']:
             data_json.append(i)
    return data_json


get_data(5)