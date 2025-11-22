from flask import Flask, render_template, request, jsonify, redirect, url_for, Response
import time
import json

app = Flask(__name__)

timev = 10
state=0
#0->PAUSE, 1->PLAY, 2->BUFFERING, 3->ENDED

@app.route("/")
def home():
    return render_template("index.html") 


@app.route("/watcher")
def watcher():
    return render_template("watcher.html")

@app.route("/watcher-lead")
def watcher_lead():
    return render_template("watcher_lead.html")


@app.route("/submit-password", methods=["POST"])
def submit_password():
    data = request.get_json()
    password = data.get("password")

    # Example logic
    if password == "a":
        url = url_for("watcher")
        return jsonify({"message": url}), 200
    elif password == "b":
        url = url_for("watcher_lead")
        return jsonify({"message", url}), 200
    else:
        return jsonify({"message": "Invalid password"}), 401



def event_stream():
    while True:
        return {"state":state, "time":time}

@app.route('/stream')
def stream():
    global timev, state
    def event_stream():
        while True:
            time.sleep(2)
            payload = {"time": timev, "status": state}
            yield f"data: {json.dumps(payload)}\n\n"
    return Response(event_stream(), mimetype="text/event-stream")

@app.route("/input_stream", methods=["POST"])
def input_stream():
    global timev, state
    data = request.get_json(force=True)  # decode JSON
    timev = data.get("time")
    state = data.get("state")
    return ""


if __name__ == "__main__":
    app.run(debug=True)