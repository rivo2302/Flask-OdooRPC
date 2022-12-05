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
        [[["active", "=", True], ["sale_ok", "=", True]]],
        {"fields": ["name", "categ_id", "description"]},
    )
    for product in products:
        product[
            "image"
        ] = f"{ODOO['HOST']}/web/image/product.template/{product['id']}/image_1920"
    return Response(
        json.dumps(products), mimetype="application/json", status=200
    )


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
            ]
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


@product.route("/product/images/<int:id>", methods=["POST"])
def get_images(id):
    product = rpc.execute(
        "product.template",
        "search_read",
        [[["id", "=", id]]],
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
        return Response(
            json.dumps(images), mimetype="application/json", status=200
        )
    return Response("Error product not found", status=404)
