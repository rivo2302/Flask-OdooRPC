from flask import Blueprint, Response
from utils.rpc import RPC
import json
from config import ODOO

rpc = RPC(ODOO)
product = Blueprint("product", __name__)


@product.route("/product", methods=["POST"])
def get_list_product():
    products = rpc.execute(
        "product.template",
        "search_read",
        [[["active", "=", True]]],
        {"fields": ["name", "categ_id", "description"]},
    )
    if products:
        for product in products:
            product[
                "image"
            ] = f"{ODOO['HOST']}/web/image/product.template/{product['id']}/image_1920"
            return Response(
                json.dumps(products), mimetype="application/json", status=200
            )
    return Response(json.dumps({"error": "No product found"}), status=404)


@product.route("/product/<int:id>", methods=["POST"])
def get_detail_product(id):
    product = rpc.execute(
        "product.template",
        "search_read",
        [[["id", "=", id]]],
        {
            "fields": [
                "name",
                "categ_id",
                "list_price",
                "default_code",
                "description",
            ],
            "limit": 1,
        },
    )
    if product:
        product = product[0]
        product[
            "image"
        ] = f"{ODOO['HOST']}/web/image/product.template/{id}/image_1920"
        return Response(
            json.dumps(product), mimetype="application/json", status=200
        )
    return Response("Error product not found", status=404)
