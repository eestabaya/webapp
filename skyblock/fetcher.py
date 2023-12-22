from flask import Blueprint, render_template, session

from auth.auth_utils import require_auth

from skyblock.api import skyblock_api

from skyblock.s3_utils import S3
from skyblock.image_utils import get_random_image

PREV_IMAGE_KEY = "previous_image_api_endpoint"

skyblock_bp = Blueprint(
    "skyblock",
    __name__,
    static_folder="static",
    template_folder="templates",
    url_prefix="/skyblock"
)

skyblock_bp.register_blueprint(skyblock_api)


# @skyblock_bp.route("/")
# def get_image_json():
#     return {
#         "success": True,
#         "result": get_random_image(
#             query={} # TODO: add query for images
#         )
#     }

@skyblock_bp.route("/")
def display_gallery():

    # if session.get(PREV_IMAGE_KEY):
    #     session.pop(PREV_IMAGE_KEY)

    mod = False
    cw_map = {}
    if session.get('discord_id'):
        cw_map = {
            "0": "Safe",
            "1": "Maybe Safe",
            "2": "Risky",
            "3": "NSFW"
        }
        mod = True

    return render_template("imageviewer.html", cw_map=cw_map, mod=mod)


@skyblock_bp.route("/reload")
@require_auth(permission="*", json_return=True)
def reload_images():
    result = S3.reload_objects("skyblock")

    return {
        "success": True,
        "count": len(result)
    }
