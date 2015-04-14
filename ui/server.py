from flask import Flask
from flask import render_template, Response, request
from flask import make_response, redirect, session, url_for
app = Flask(__name__)

@app.route("/")
def input_usernames():
    return render_template("input.html")

@app.route("/api/add-usernames", methods = ["POST"])
def user_input_api():
    usernames = request.json
    for user in usernames:
        print user

    return "{}"

if __name__ == "__main__":

    app.debug = True

    app.run('0.0.0.0', port=8080, threaded=True)
