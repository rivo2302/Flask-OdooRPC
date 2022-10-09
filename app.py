from flask import Flask, jsonify
from os import environ as env
from config import CONFIG as CONF
from api.ressources import product


app = Flask(__name__)
app.register_blueprint(product)

if __name__ == "__main__":
    app.run(CONF["HOST"], CONF["PORT"], CONF["DEBUG"])
