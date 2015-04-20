from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from pymongo import ASCENDING

class ProfilerMongoUtils(object):

    def __init__(self, init_db=False, address="localhost", port=27017):

        client = MongoClient(address, port)
        db = client["ProfilerDb"]
        self.scrapy_item_collection = db["userinfo"]

        if init_db:
            db.drop_collection(self.scrapy_item_collection)
            self.scrapy_item_collection.ensure_index([("username", ASCENDING), ("resource", ASCENDING)], unique = True)

    def insert_record(self, item_doc):
        try:
            self.scrapy_item_collection.save(item_doc)
        except DuplicateKeyError:
            print "Duplicate entry %s" % str(item_doc)

    def list_records(self):
        return self.scrapy_item_collection.find()

    def list_records_filtered(self, filter):
        return self.scrapy_item_collection.find(filter)

    def list_indices(self):
        return list(self.scrapy_item_collection.list_indexes())

if __name__ == "__main__":

    pm = ProfilerMongoUtils(init_db = True)
    #print pm.list_records()
    #print pm.list_indices()