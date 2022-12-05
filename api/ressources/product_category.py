from flask import Blueprint, Response
from utils.rpc import RPC
import json
from config import ODOO

rpc = RPC(ODOO)
category = Blueprint("category", __name__)


@category.route("/category", methods=["POST"])
def get_list_category():
    categories = rpc.execute(
        "product.category",
        "search_read",
        [],
        {"fields": ["name"]},
    )
    if categories:
        for category in categories:
            category[
                "image"
            ] = f"{ODOO['HOST']}/web/image/product.category/{category['id']}/image_1920"
            return Response(
                json.dumps(categories), mimetype="application/json", status=200
            )


@category.route("/category/<int:id>", methods=["POST"])
def get_detail_category(id):
    category = rpc.execute(
        "product.category",
        "search_read",
        [[["id", "=", id]]],
        {"fields": ["name"], "limit": 1},
    )
    if category:
        category = category[0]
        category[
            "image"
        ] = f"{ODOO['HOST']}/web/image/product.category/{id}/image_1920"
        category["products"] = rpc.execute(
            "product.template",
            "search_read",
            [[["categ_id", "=", id]]],
            {"fields": ["name", "description"]},
        )
        return Response(
            json.dumps(category), mimetype="application/json", status=200
        )
    else:
        return Response("Error product not found", status=404)