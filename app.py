from flask import Flask
from os import environ as env
from config import CONFIG as CONF

app = Flask(__name__)

if __name__ == "__main__":
    app.run(CONF["HOST"], CONF["PORT"], CONF["DEBUG"])
