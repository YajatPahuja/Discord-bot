from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')

def home():
    return "This is a Discord bot running on a Flask web server!"

def run():
    app.run(host = "0.0.0.0", port = 8080)

def keep_alive():
    t = Thread(target = run)
    t.start()
