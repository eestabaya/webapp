from flask import Blueprint, session, request

from auth.auth_utils import require_auth

from skyblock.image_utils import get_images

PREV_IMAGE_KEY = "previous_image_api_endpoint"

skyblock_api = Blueprint(
    "api",
    __name__,
    url_prefix="/api"
)

@skyblock_api.route("/images")
def fetch_images():
    
    page_limit = request.args.get('limit')
    page_number = request.args.get('page')
    query = {}
    if not session.get('discord_id'):
        # LEVELS: 0 1 2 3
        # SAFE < PROBABLY SAFE < RISKY < BAD
        query['cw'] = {"$lt": 2}

    images = get_images(query=query, page_limit=page_limit, page_number=page_number)
    # images, last_entry = get_images(
    #     prev_entry=session.get(PREV_IMAGE_KEY)
    # )

    # session[PREV_IMAGE_KEY] = last_entry

    return {
        "success": True,
        "result": images
    }

@skyblock_api.route("/image")
@require_auth(permission="*", json_return=True)
def edit_image():
    return "im not done yet"
