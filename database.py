import pymongo

# enable the comment to provide access to mongo cloud
# client = pymongo.MongoClient("mongodb+srv://hanzo:<oassword>@cluster0.13jih.mongodb.net/?retryWrites=true&w=majority")

def get_db(db_name:str):
<<<<<<< HEAD
    client = pymongo.MongoClient("mongodb:27017")
=======
    client = pymongo.MongoClient("localhost", 27017)
    # client = pymongo.MongoClient("mongodb+srv://hanzo:<password>@cluster0.13jih.mongodb.net/?retryWrites=true&w=majority")
>>>>>>> a5342c98ed6562cf5b0fec9ed88f14b85093355d
    db = client.test
    db = client.get_database(db_name)
    # try:
    #     yield db
    # finally:
    #     db.close()
    return db
