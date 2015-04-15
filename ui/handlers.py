from profiler_mongo.profiler_mongo_utils import ProfilerMongoUtils
import shelve
from scrapydutils import ScrapydJob

def user_input_handler(usernames):

    d = shelve.open("dbobjects/" + "users.shelve.db")
    d["users"] = usernames
    sdj = ScrapydJob("localhost", 6800, project='profiler-project', spider="profiler_spider")
    for user in usernames:
        sdj.schedule(user)

def  job_stats_handler():

    sdj = ScrapydJob("localhost", 6800, project='profiler-project', spider="profiler_spider")
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

def clear_results():




if __name__ == "__main__":

    print job_stats_handler()
    #user_input_handler(open("../usernames.txt").readlines())