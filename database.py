import pymongo

# client = pymongo.MongoClient("mongodb+srv://hanzo:<oassword>@cluster0.13jih.mongodb.net/?retryWrites=true&w=majority")

def get_db(db_name:str):
    client = pymongo.MongoClient("localhost", 27017)
    # client = pymongo.MongoClient("mongodb+srv://hanzo:<password>@cluster0.13jih.mongodb.net/?retryWrites=true&w=majority")
    db = client.test
    db = client.get_database(db_name)
    # try:
    #     yield db
    # finally:
    #     db.close()
    return db