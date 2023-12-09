from threading import Thread
from flask import Flask, render_template

app = Flask("")


@app.route("/")
def index():
    return "Join Yoko for free friends"

def run():
    app.run(host="0.0.0.0", port=8080)

def start():
    t = Thread(target=run)
    t.start()
