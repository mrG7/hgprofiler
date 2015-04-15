from ui.profiler_mongo.profiler_mongo_utils import ProfilerMongoUtils

class MongoPipeline(object):

    def __init__(self, mongo_location, mongo_port):
        self.mongo_location = mongo_location
        self.mongo_port = mongo_port
        self.profiler_mongo = ProfilerMongoUtils(address = mongo_location, port = mongo_port)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_location=crawler.settings.get('MONGO_LOCATION'),
            mongo_port=crawler.settings.get('MONGO_PORT'),
        )

    def process_item(self, item, spider):
        item_dic = dict(item)
        print "Inserting %s" % str(item)
        self.profiler_mongo.insert_record(item_dic)
        return item
