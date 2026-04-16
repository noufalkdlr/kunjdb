from tinydb.database import TinyDB

db = TinyDB('data.json', indent =4)
person = db.table('person')




person.insert({"name":"noufal"})

