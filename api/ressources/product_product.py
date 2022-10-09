from flask import Blueprint, Response
from retry import retry
from utils.rpc import RPC
from os import abort, environ as env
import json

odoo = {
    "HOST": env.get("ODOO_HOST"),
    "PORT": env.get("ODOO_PORT"),
    "DB": env.get("ODOO_DB"),
    "USER": env.get("ODOO_USER"),
    "PASSWORD": env.get("ODOO_PASSWORD"),
}
rpc = RPC(odoo)

product = Blueprint("product", __name__)


@product.route("/product", methods=["POST"])
def get_product_product():
    products = rpc.execute(
        "product.template",
        "search_read",
        [],
        ["name", "list_price", "description"],
    )
    if products:
        for product in products:
            product[
                "image"
            ] = f"{odoo['HOST']}/web/image/product.template/{product['id']}/image_1920"
            movies = json.dumps(products)
            return Response(movies, mimetype="application/json", status=200)
    return Response(status=404)
