from handlers import user_input_handler, job_stats_handler, users_handler
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
    #user_input_handler(usernames)
    thr = Thread(spawn_async_usernames_handler(app, usernames))
    thr.start()

    return "{}"

@app.route("/api/job-stats", methods = ["GET"])
def job_stats():
    finished, pending, running = job_stats_handler()

    return '{"finished" : %s, "pending" : %s, "running" : %s, "all" : %s}' % (finished, pending, running, finished + pending + running)

if __name__ == "__main__":

    app.debug = True

    app.run('0.0.0.0', port=8080, threaded=True)
