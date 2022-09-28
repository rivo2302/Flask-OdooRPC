import odoorpc
from os import environ as env

CONF = {
    "HOST": env.get("DB_HOST"),
    "PORT": env.get("DB_PORT"),
    "DB": env.get("DB_NAME"),
    "USER": env.get("DB_USER"),
    "PASSWD": env.get("DB_PASSWD"),
}

odoo = odoorpc.ODOO(CONF["HOST"], port=CONF["PORT"])
print(odoo.db.list())
odoo.login(CONF["DB"], CONF["USER"], CONF["PASSWD"])
