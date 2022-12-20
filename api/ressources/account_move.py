from flask import Blueprint, Response, request
from utils.rpc import RPC
from utils.tools import drop_false
import json
from pydantic import BaseModel
from typing import Optional, List
from config import ODOO
from flasgger.utils import swag_from
from flask_pydantic import validate

rpc = RPC(ODOO)
account = Blueprint("account", __name__, url_prefix="/account")

"""
In this route we will create the account move for the sale order and we will get 
the id of the created account move and return it to the user
by default the account move will be created in the posted state and 
the payment state will be paid
"""


@account.route("/", methods=["POST"])
def create_account_move():
    # Get the id of the sale order from the request

    sale_order_id = request.args.get("sale_order_id")
    if not sale_order_id or not sale_order_id.isdigit():
        return Response(
            json.dumps({"error": "sale_order_id is required or not valid"}),
            mimetype="application/json",
            status=400,
        )
    # Get the sale order from the odoo database
    sale_order_id = int(sale_order_id)
    sale_order = rpc.execute(
        "sale.order",
        "search_read",
        [[["id", "=", sale_order_id]]],
        {"limit": 1},
    )
    if not sale_order:
        return Response(
            json.dumps({"error": "Sale order not found"}),
            mimetype="application/json",
            status=400,
        )
    sale_order = sale_order[0]
    res = rpc.execute("sale.advance.payment.inv", "_create_invoice", [sale_order_id, {}, {}])
    return Response(
        json.dumps({"id": res}), mimetype="application/json", status=200
    )
