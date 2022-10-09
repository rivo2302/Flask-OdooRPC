from os import environ as env

CONFIG = {
    "HOST": env.get("HOST"),
    "PORT": env.get("PORT"),
    "DEBUG": 1,
}
