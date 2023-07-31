from pony.orm import Database

db = Database()
db.bind(provider='sqlite', filename=':sharedmemory:', create_db=True)