import traceback
from scrapyd_api import ScrapydAPI
import os
import json
this_files_dir = os.path.dirname(os.path.realpath(__file__))

class ScrapydJob(object):

    def __init__(self, scrapyd_host="localhost", scrapyd_port="6800", project="profiler-project", spider="profiler_spider"):

        scrapy_url = "http://" + scrapyd_host + ":" + str(scrapyd_port)
        self.scrapi = ScrapydAPI(scrapy_url)
        self.project = project
        self.spider = spider

    def schedule(self, usernames):

        #usernames will usually be a single username, but can be CSV list
        self.job_id = self.scrapi.schedule(self.project, self.spider, usernames=usernames)

        return self.job_id

    def list_jobs(self):
        return self.scrapi.list_jobs(self.project)

    def get_job_stats(self):
        jobs_list = self.list_jobs()
        finished = len(jobs_list["finished"])
        pending = len(jobs_list["pending"])
        running = len(jobs_list["running"])

        return finished, pending, running

    def get_state(self, job_id):

        try:
            for job in self.scrapi.list_jobs(self.project)["running"]:
                print job_id, job["id"]
                if job["id"] == job_id:
                    return "Running"

            for job in self.scrapi.list_jobs(self.project)["pending"]:
                print job_id, job["id"]
                if job["id"] == job_id:
                    return "Pending"

        except Exception:
            print "handled exception:"
            traceback.print_exc()
            return None

        return "Done"

    def clear_scrapyd(self):
        scrapyd_db_path = os.path.realpath(os.path.join(this_files_dir, "../", "db/"))
        scrapyd_build_path = os.path.realpath(os.path.join(this_files_dir, "../", "build/"))
        scrapyd_logs_path = os.path.realpath(os.path.join(this_files_dir, "../", "logs/"))
        #scrapyd_eggs_path = os.path.realpath(os.path.join(this_files_dir, "../", "eggs/"))
        #os.path.realpath(os.path.join(this_files_dir, "../", "project.egg-info/"))



if __name__ == "__main__":

    scrapyd_util = ScrapydJob("localhost", 6800, project='profiler-project', spider="profiler_spider")
    #scrapyd_util.schedule("blah")
    #print scrapyd_util.get_job_stats()
    scrapyd_util.clear_scrapyd()
