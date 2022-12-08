from flask import Blueprint, Response
from utils.rpc import RPC
from utils.tools import drop_false
import json
from config import ODOO
from api.ressources import token_required
from pydantic import BaseModel
from typing import Optional
from flask_pydantic import validate


class Partner(BaseModel):
    name: str
    phone: Optional[str]
    email: Optional[str]
    street: Optional[str]
    website: Optional[str]
    amp_user_id: Optional[str]


rpc = RPC(ODOO)
partner = Blueprint("partner", __name__)


@partner.route("/partner", methods=["POST"])
@token_required
@validate()
def create(body: Partner):
    res = rpc.execute("res.partner", "create", [body.dict()], [])
    if partner:
        return Response(
            json.dumps({"id": res}),
            mimetype="application/json",
            status=200,
        )
    return Response("Error partner not created", status=500)
