from profiler_mongo.profiler_mongo_utils import ProfilerMongoUtils
from scrapydutils import ScrapydJob

def user_input_handler(usernames):

    sdj = ScrapydJob("localhost", 6801, project='profiler-project', spider="profiler_spider")
    for user in usernames:
        sdj.schedule(user)

def  job_stats_handler():

    sdj = ScrapydJob("localhost", 6801, project='profiler-project', spider="profiler_spider")
    return sdj.get_job_stats()

def users_handler():

    pmu = ProfilerMongoUtils()
    users_and_counts = {}
    #FIXME: hacky and slow
    for user_dic in pmu.list_records():
        user = user_dic["username"]
        if user not in users_and_counts:
            users_and_counts[user] = 1
        else:
            users_and_counts[user] += 1

    return users_and_counts

def records_handler(username):
    pass

def kill_crawl_services_handler():
    sdj = ScrapydJob("localhost", 6801, project='profiler-project', spider="profiler_spider")
    sdj.kill_crawl_services()

def crawl_services_status_handler():
    sdj = ScrapydJob("localhost", 6801, project='profiler-project', spider="profiler_spider")
    return sdj.crawl_service_status()

def start_crawl_services_handler():
    sdj = ScrapydJob("localhost", 6801, project='profiler-project', spider="profiler_spider")
    sdj.start_crawl_services()

def clear_crawls_handler():
    sdj = ScrapydJob("localhost", 6801, project='profiler-project', spider="profiler_spider")
    sdj.clear_scrapyd()
    ProfilerMongoUtils(init_db = True)

def get_data_handler(username = None):

    pmu = ProfilerMongoUtils()
    if not username:
        records = list(pmu.list_records())
    else:
        filter = {"username" : username}
        records = list(pmu.list_records_filtered(filter))

    for record in records:
        del record["_id"]

    return records

if __name__ == "__main__":

    for record in get_data_handler():
        print record
    #print job_stats_handler()
    #user_input_handler(open("../usernames.txt").readlines())
