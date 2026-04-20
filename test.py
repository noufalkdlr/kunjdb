from tinydb.database import TinyDB
from tinydb.table import Document

db = TinyDB("data.json", indent=4)


db.insert({"name": "noufal"})
db.insert(Document({"name": "Noufal"}, doc_id=501))

db.insert({"name": "noufal"})
