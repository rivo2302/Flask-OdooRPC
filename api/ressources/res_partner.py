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
    amp_user_facebook_id: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    street: Optional[str]  # addresse
    website: Optional[str]


rpc = RPC(ODOO)
partner = Blueprint("partner", __name__, url_prefix="/partner")


@partner.route("/", methods=["GET"])
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


@partner.route("/<int:id>", methods=["GET"])
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
                "amp_user_facebook_id",
                "phone",
                "email",
                "street",
                "website",
            ]
        },
    )
    if partner:
        partner = drop_false(partner)
        return Response(
            json.dumps(partner[0]), mimetype="application/json", status=200
        )
    return Response("Error partner not found", status=404)


@partner.route("/", methods=["POST"])
@validate()
def create(body: Partner):
    # add amp_user_id if amp_user_facebook_id is in body
    body = body.dict()
    if "amp_user_facebook_id" in body.keys():
        print("here")
        # get amp_user_id
        print(body["amp_user_facebook_id"])
        amp_user_id = rpc.execute(
            "amp.user",
            "search_read",
            [
                [
                    [
                        "user_id",
                        "=",
                        body["amp_user_facebook_id"],
                    ],
                ]
            ],
            {"limit": 1},
        )
        print(amp_user_id)
        if amp_user_id:
            del body["amp_user_facebook_id"]
            body["amp_user_id"] = amp_user_id[0]["id"]
            res = rpc.execute("res.partner", "create", [body])
            if res:
                return Response(
                    json.dumps({"id": res}),
                    mimetype="application/json",
                    status=200,
                )
            return Response("Error partner not created", status=500)
        return Response("Error amp_user not found", status=400)
    res = rpc.execute("res.partner", "create", [body])
    if res:
        return Response(
            json.dumps({"id": res}),
            mimetype="application/json",
            status=200,
        )
    return Response("Error partner not created", status=500)


@partner.route("/amp_user/<string:sender_id>", methods=["GET"])
def get_user_partner(sender_id):
    partner = rpc.execute(
        "res.partner",
        "search_read",
        [
            [
                [
                    "amp_user_facebook_id",
                    "=",
                    sender_id,
                ],
            ]
        ],
        {
            "fields": [
                "name",
                "amp_user_facebook_id",
                "phone",
                "email",
                "street",
                "website",
            ],
            "limit": 1,
        },
    )
    if partner:
        partner = drop_false(partner)
        return Response(
            json.dumps(partner[0]), mimetype="application/json", status=200
        )
    return Response("Error partner not found", status=404)
