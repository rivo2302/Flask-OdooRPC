from flask import Blueprint, Response
from utils.rpc import RPC
from utils.tools import drop_false
import json
from config import ODOO
from flasgger.utils import swag_from
from docs.category import list_specs, detailed_specs

rpc = RPC(ODOO)
category = Blueprint("category", __name__, url_prefix="/category")


@category.route(
    "/",
    methods=["GET"],
)
@swag_from(list_specs, methods=["GET"])
def get_list_category():
    """Get list of product category."""
    categories = rpc.execute(
        "product.category",
        "search_read",
        [],
        {"fields": ["name"]},
    )
    for category in categories:
        category[
            "image"
        ] = f"{ODOO['HOST']}/web/image/product.category/{category['id']}/image_1920"
    categories = drop_false(categories)
    return Response(
        json.dumps(categories), mimetype="application/json", status=200
    )


@category.route(
    "/<int:id>",
    methods=["GET"],
)
@swag_from(detailed_specs, methods=["GET"])
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
        category = drop_false(category)
        return Response(
            json.dumps(category), mimetype="application/json", status=200
        )
    return Response("Error product category not found", status=404)
