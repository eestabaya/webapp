import os

from flask import Blueprint, request, jsonify

from dsg.dsg_linked_role import dsg_linked_role_bp

from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

from discord.interactions import parse_interaction


dsg_bp = Blueprint(
    "dsg",
    __name__,
    url_prefix="/dsg"
)

dsg_bp.register_blueprint(dsg_linked_role_bp)


@dsg_bp.route("/interactions", methods=['POST'])
def interactions():

    PUBLIC_KEY = os.environ.get("DSG_PUBLIC_KEY")

    verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))

    signature = request.headers["X-Signature-Ed25519"]
    timestamp = request.headers["X-Signature-Timestamp"]
    body = request.data.decode("utf-8")

    try:
        verify_key.verify(f'{timestamp}{body}'.encode(), bytes.fromhex(signature))
    except BadSignatureError:
        return 'invalid request signature', 401

    if request.json["type"] == 1:
        return jsonify(
            {
                "type": 1
            }
        )
    
    interaction = parse_interaction(request.json)
    return jsonify(interaction.get_return_data())
