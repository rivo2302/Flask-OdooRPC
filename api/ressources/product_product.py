from flask import Blueprint, Response
from utils.rpc import RPC
from utils.tools import drop_false
import json
from config import ODOO

rpc = RPC(ODOO)
product = Blueprint("product", __name__, url_prefix="/product")


@product.route("/", methods=["GET"])
def get_list_product():
    products = rpc.execute(
        "product.template",
        "search_read",
        [
            [
                ["active", "=", True],
                ["sale_ok", "=", True],
                ["detailed_type", "=", "product"],
            ]
        ],
        {
            "fields": [
                "name",
                "categ_id",
                "image_url",
                "qty_available",
                "list_price",
                "default_code",
                "description",
            ]
        },
    )
    products = drop_false(products)
    return Response(
        json.dumps(products), mimetype="application/json", status=200
    )


@product.route("/<int:id>", methods=["GET"])
def get_detail_product(id):
    product = rpc.execute(
        "product.template",
        "search_read",
        [
            [
                ["id", "=", id],
                ["active", "=", True],
                ["sale_ok", "=", True],
                ["detailed_type", "=", "product"],
            ]
        ],
        {
            "fields": [
                "name",
                "categ_id",
                "image_url",
                "qty_available",
                "list_price",
                "default_code",
                "description",
            ]
        },
    )
    if product:
        product = drop_false(product)
        # return only the first product
        return Response(
            json.dumps(product[0]), mimetype="application/json", status=200
        )
    return Response("Error product not found", status=404)


@product.route("/images/<int:id>", methods=["GET"])
def get_images(id):
    product = rpc.execute(
        "product.template",
        "search_read",
        [
            [
                ["id", "=", id],
                ["active", "=", True],
                ["sale_ok", "=", True],
                ["detailed_type", "=", "product"],
            ]
        ],
        {"fields": ["pictures_ids"]},
    )
    if product:
        images = rpc.execute(
            "ir.attachment",
            "search_read",
            [[["id", "in", product[0]["pictures_ids"]]]],
            {"fields": ["name", "description"]},
        )
        for image in images:
            image[
                "url"
            ] = f"{ODOO['HOST']}/web/image/ir.attachment/{image['id']}/datas"
        images = drop_false(images)
        return Response(
            json.dumps(images), mimetype="application/json", status=200
        )
    return Response(json.dumps("Error product not found"), status=404)
