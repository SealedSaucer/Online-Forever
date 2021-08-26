from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def main():
    return '<meta http-equiv="refresh" content="0; URL=https://phantomcodes.ga/support"/>'

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()
