import pymongo



class Database(object):
    URI = "mongodb://127.0.0.1:27017"
    DATABASE = None

    @staticmethod
    def initilize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client["direction_prototype"]

    @staticmethod
    def insert(collection,data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find_all(collection, query):
        datas= Database.DATABASE[collection].find(query)
        if datas is None:
            return None
        return [data for data in datas]

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def update(collection,form,value):
        Database.DATABASE[collection].update(form,value,upsert=False)

    @staticmethod
    def remove(collection,query):
        Database.DATABASE[collection].remove(query)
