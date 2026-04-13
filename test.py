# from tinydb.database import TinyDB

# db = TinyDB('data.json')
# person = db.table('person')

# print(type(person))

from typing import Dict

data = {'name':"noufal"}

def name(data:Dict):
    return data['name']


print(name(data))