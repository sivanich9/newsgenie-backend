import pymongo

def get_db(db_name:str):
    client = pymongo.MongoClient("mongodb:27017")
    db = client.test
    db = client.get_database(db_name)
    # try:
    #     yield db
    # finally:
    #     db.close()
    return db
