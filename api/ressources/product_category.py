from flask import Blueprint, Response
from utils.rpc import RPC
import json
from config import ODOO
from api.ressources import token_required

rpc = RPC(ODOO)
category = Blueprint("category", __name__)


@category.route("/category", methods=["POST"])
@token_required
def get_list_category():
    categories = rpc.execute(
        "product.category",
        "search_read",
        [],
        {"fields": ["name"]},
    )
    print("redirection")
    for category in categories:
        category[
            "image"
        ] = f"{ODOO['HOST']}/web/image/product.category/{category['id']}/image_1920"
    return Response(
        json.dumps(categories), mimetype="application/json", status=200
    )


@category.route("/category/<int:id>", methods=["POST"])
@token_required
def get_detail_category(id):
    category = rpc.execute(
        "product.category",
        "search_read",
        [[["id", "=", id]]],
        {"fields": ["name"]},
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
    return Response("Error product category not found", status=404)
