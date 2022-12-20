from os import environ as env

template = {
    "swagger": "2.0",
    "uiversion": 3,
    "info": {
        "title": "Marketbot API",
        "description": "API to link Odoo and Bot Messenger",
        "contact": {
            "responsibleOrganization": "iTeam-$",
            "responsibleDeveloper": "Rivo2302",
            "email": "rivo2302@gmail.com",
            "url": "www.iteam-s.mg",
        },
        "termsOfService": "http:/iteam-s.mg/terms",
        "version": "0.0.2",
    },
    "host": f"{env.get('HOST')}:{env.get('PORT')}",
    "basePath": "",
    "schemes": ["http", "https"],
    "operationId": "getmyData",
    "produces": ["application/json"],
    "consumes": ["application/json"],
}

