import json
from handlers import user_input_handler, job_stats_handler, users_handler,\
    crawl_services_status_handler, kill_crawl_services_handler,\
    start_crawl_services_handler, clear_crawls_handler, get_data_handler
from threading import Thread
from flask import Flask
from flask import render_template, Response, request
from flask import make_response, redirect, session, url_for
app = Flask(__name__)

def spawn_async_usernames_handler(app, usernames):
    print "executing here!"
    with app.app_context():
        user_input_handler(usernames)


@app.route("/")
def input_usernames():

    users = users_handler()
    return render_template("input.html", users = users)

@app.route("/api/add-usernames", methods = ["POST"])
def user_input_api():
    usernames = request.json
    usernames = usernames[0].split("\n")

    usernames_filtered = []
    for user in usernames:
        print user
        if user.strip():
            usernames_filtered.append(user.strip())

    #user_input_handler(usernames)
    thr = Thread(spawn_async_usernames_handler(app, usernames_filtered))
    thr.start()

    return "{}"

@app.route("/api/job-stats", methods = ["GET"])
def job_stats():
    finished, pending, running = job_stats_handler()

    return '{"finished" : %s, "pending" : %s, "running" : %s, "all" : %s}' % (finished, pending, running, finished + pending + running)

@app.route("/api/crawl-service-status", methods = ["GET"])
def crawl_service_status():
    if crawl_services_status_handler():
        return Response(json.dumps({"status" : "up"}), mimetype="application/json")
    else:
        return Response(json.dumps({"status" : "down"}), mimetype="application/json")

@app.route("/api/kill-crawl-services", methods = ["GET"])
def kill_crawl_services():
    kill_crawl_services_handler()
    return Response("{}", mimetype="application/json")

@app.route("/api/start-crawl-services", methods = ["GET"])
def start_crawl_services():
    start_crawl_services_handler()
    return Response("{}", mimetype="application/json")

@app.route("/api/clear-crawls", methods = ["GET"])
def clear_crawls():
    clear_crawls_handler()
    return Response("{}", mimetype="application/json")

@app.route("/data-download.jl")
def data_download():
    user = request.args.get("user")

    if not user:
        data_handler = get_data_handler()
    else:
        data_handler = get_data_handler(user)

    jl = ""
    for record in data_handler:
        jl += json.dumps(record) + "\n"

    return Response(jl, mimetype="application/json")

if __name__ == "__main__":

    app.debug = True
    app.run('0.0.0.0', port=8080, threaded=True)
