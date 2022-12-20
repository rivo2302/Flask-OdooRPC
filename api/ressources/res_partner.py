from flask import Blueprint, Response, request
from utils.rpc import RPC
from utils.tools import drop_false
import json
from config import ODOO
from pydantic import BaseModel
from typing import Optional
from flask_pydantic import validate


class Partner(BaseModel):
    name: str
    amp_user_id: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    street: Optional[str]  # addresse
    website: Optional[str]


rpc = RPC(ODOO)
partner = Blueprint("partner", __name__, url_prefix="/partner")


@partner.route("/", methods=["GET"],strict_slashes=False)
def get_list_partner():
    partners = rpc.execute(
        "res.partner",
        "search_read",
        [
            [
                ["active", "=", True],
            ]
        ],
        {
            "fields": [
                "name",
                "phone",
                "email",
                "street",
                "website",
            ]
        },
    )
    partners = drop_false(partners)
    return Response(
        json.dumps(partners), mimetype="application/json", status=200
    )


@partner.route("/<int:id>", methods=["GET"],strict_slashes=False)
def get_detail_partner(id):
    partner = rpc.execute(
        "res.partner",
        "search_read",
        [
            [
                ["id", "=", id],
                ["active", "=", True],
            ]
        ],
        {
            "fields": [
                "name",
                "phone",
                "email",
                "street",
                "website",
            ]
        },
    )
    if partner:
        return Response(
            json.dumps(partner[0]), mimetype="application/json", status=200
        )
    return Response("Error partner not found", status=404)


@partner.route("/", methods=["POST"],strict_slashes=False)
@validate()
def create(body: Partner):
    res = rpc.execute("res.partner", "create", [body.dict()], [])
    if res:
        return Response(
            json.dumps({"id": res}),
            mimetype="application/json",
            status=200,
        )
    return Response("Error partner not created", status=500)
