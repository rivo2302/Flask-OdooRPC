from flask import Blueprint, Response, request
from utils.rpc import RPC
from utils.tools import drop_false
import json
from pydantic import BaseModel
from typing import Optional, List
from config import ODOO
from flask_pydantic import validate

rpc = RPC(ODOO)
sale = Blueprint("sale", __name__, url_prefix="/sale")


class SaleOrderLine(BaseModel):
    product_id: int
    product_uom_qty: int


class SaleOrder(BaseModel):
    partner_id: Optional[int]
    partner_shipping_id: Optional[int]
    date_order: Optional[str]
    order_line: List[SaleOrderLine]


@sale.route("/", methods=["GET"])
def list_sale():
    """
    By default the filter is only all sale order that state is in sale
    so we will get all the
    sales in sale state but if there is partner_id in the
    request we will filter the sales by the partner_id
    """
    filter = [
        ["state", "=", "sale"],
    ]

    # Get the partner_id from the request , if true add it to the filter
    partner_id_param = request.args.get("partner_id")
    if partner_id_param:
        if not partner_id_param.isnumeric():
            return Response(
                json.dumps({"error": "partner_id must be a number"}),
                mimetype="application/json",
                status=400,
            )
        filter.append(["partner_id", "=", int(partner_id_param)])
    sales = rpc.execute(
        "sale.order",
        "search_read",
        [filter],
        {
            "fields": [
                "name",
                "partner_id",
                "partner_shipping_id",
                "date_order",
                "order_line",
                "amount_total",
                "picking_ids",
            ]
        },
    )
    for sale in sales:
        # Get the object of customer , shipping_customer and order lines not only the id  .
        if sale["partner_id"]:
            partner = rpc.execute(
                "res.partner",
                "search_read",
                [[["id", "=", sale["partner_id"][0]]]],
                {"fields": ["name", "phone", "mobile", "email"]},
            )
            sale["partner_id"] = partner[0] if partner else {}
        if sale["partner_shipping_id"]:
            shipping = rpc.execute(
                "res.partner",
                "search_read",
                [[["id", "=", sale["partner_shipping_id"][0]]]],
                {"fields": ["name", "phone", "mobile", "email"]},
            )
            sale["partner_shipping_id"] = shipping[0] if shipping else {}
        if sale["order_line"]:
            order_lines = rpc.execute(
                "sale.order.line",
                "search_read",
                [[["id", "in", sale["order_line"]]]],
                {"fields": ["product_id", "product_uom_qty", "price_unit"]},
            )
            sale["order_line"] = order_lines if order_lines else []
        if sale["picking_ids"]:
            pickings = rpc.execute(
                "stock.picking",
                "search_read",
                [[["id", "in", sale["picking_ids"]]]],
                {"fields": ["name", "state"]},
            )
            sale["picking_ids"] = pickings if pickings else []

    sales = drop_false(sales)
    return Response(json.dumps(sales), mimetype="application/json", status=200)


@sale.route("/<int:id>", methods=["GET"])
def get_sale_order(id):
    sale = rpc.execute(
        "sale.order",
        "search_read",
        [
            [
                ["id", "=", id],
            ]
        ],
        {
            "fields": [
                "name",
                "partner_id",
                "partner_shipping_id",
                "date_order",
                "order_line",
                "amount_total",
                "picking_ids",
            ],
            "limit": 1,
        },
    )
    if not sale:
        return Response(
            json.dumps({"error": "Sale order not found"}),
            mimetype="application/json",
            status=404,
        )
    sale = sale[0]
    if sale["partner_id"]:
        partner = rpc.execute(
            "res.partner",
            "search_read",
            [[["id", "=", sale["partner_id"][0]]]],
            {"fields": ["name", "phone", "mobile", "email"]},
        )
        sale["partner_id"] = partner[0] if partner else {}
    if sale["partner_shipping_id"]:
        shipping = rpc.execute(
            "res.partner",
            "search_read",
            [[["id", "=", sale["partner_shipping_id"][0]]]],
            {"fields": ["name", "phone", "mobile", "email"]},
        )
        sale["partner_shipping_id"] = shipping[0] if shipping else {}
    if sale["order_line"]:
        order_lines = rpc.execute(
            "sale.order.line",
            "search_read",
            [[["id", "in", sale["order_line"]]]],
            {"fields": ["product_id", "product_uom_qty", "price_unit"]},
        )
        sale["order_line"] = order_lines if order_lines else []
    if sale["picking_ids"]:
        pickings = rpc.execute(
            "stock.picking",
            "search_read",
            [[["id", "in", sale["picking_ids"]]]],
            {"fields": ["name", "state"]},
        )
        sale["picking_ids"] = pickings if pickings else []

    sale = drop_false(sale)
    return Response(json.dumps(sale), mimetype="application/json", status=200)


@sale.route("/", methods=["POST"])
@validate()
def create(body: SaleOrder):

    body = body.dict()
    # First we have to create the sale order and get the id of the created sale order
    sale_order_id = rpc.execute(
        "sale.order",
        "create",
        [
            {
                "partner_id": body.get("partner_id"),
                "partner_shipping_id": body.get("partner_shipping_id"),
                "state": "sale",  # By default the state of the sale order is draft so we will change it to sale
            }
        ],
    )
    if not sale_order_id:
        return Response("Error sale order not created", status=500)

    # The sale order is created now we will create the order lines
    order_lines = body.get("order_line")

    for order_line in order_lines:
        order_line_id = rpc.execute(
            "sale.order.line",
            "create",
            [
                {
                    "product_id": order_line["product_id"],
                    "product_uom_qty": order_line["product_uom_qty"],
                    "order_id": sale_order_id,  # Here we will pass the id of the created sale order
                }
            ],
        )
        if not order_line_id:
            return Response("Error sale order line not created", status=500)

    # Now the sale order is created we will get the name of the sale order and return it to the user
    sale_order = rpc.execute(
        "sale.order",
        "search_read",
        [[["id", "=", sale_order_id]]],
        {"fields": ["name"]},
    )
    name = sale_order[0]["name"] if sale_order else None
    return Response(
        json.dumps({"id": sale_order_id, "name": name}),
        mimetype="application/json",
        status=200,
    )
