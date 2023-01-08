from os import environ as env

CONFIG = {
    "HOST": env.get("HOST"),
    "PORT": env.get("PORT"),
    "DEBUG": 1,
}
ODOO = {
    "HOST": env.get("ODOO_HOST"),
    "PORT": env.get("ODOO_PORT"),
    "DB": env.get("ODOO_DB"),
    "USER": env.get("ODOO_USER"),
    "PASSWORD": env.get("ODOO_PASSWORD"),
}
