from flask import Flask
from os import environ as env
from config import CONFIG as CONF
from utils.rpc import RPC

app = Flask(__name__)

odoo = {
    "HOST": env.get("ODOO_HOST"),
    "PORT": env.get("ODOO_PORT"),
    "DB": env.get("ODOO_DB"),
    "USER": env.get("ODOO_USER"),
    "PASSWORD": env.get("ODOO_PASSWORD"),
}
rpc = RPC(odoo)

x = rpc.execute("res.partner", "search_read", [], ["name"])
print(x)

if __name__ == "__main__":
    app.run(CONF["HOST"], CONF["PORT"], CONF["DEBUG"])
