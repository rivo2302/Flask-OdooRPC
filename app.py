from flask import Flask, jsonify
from os import environ as env
from api.ressources import product


app = Flask(__name__)
app.register_blueprint(product)
