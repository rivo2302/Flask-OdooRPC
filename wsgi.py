from os import environ as env
from config import CONFIG as CONF

from app import app

if __name__ == "__main__":
    app.run(CONF["HOST"], CONF["PORT"], CONF["DEBUG"])
