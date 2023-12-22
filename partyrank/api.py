from flask import Blueprint, request, jsonify, session

from auth.auth_utils import require_auth

from db.mongo_db import MongoController

pr_api = Blueprint(
    "api",
    __name__,
    url_prefix="/api"
)


@pr_api.route("/submit", methods=['POST'])
@require_auth(json_return=True)
def submit_pr():

    user = MongoController.get_user(session['discord_id'])

    perms = user.get('permissions')
#    if perms is None or not ('*' in perms or 'partyrank' in perms):
#        return {"success": False, "cause": "No permission"}, 403

    # process data
    data = request.json

    pr_id = data.get("pr_id")
    ordering = data.get("entries")

    if pr_id is None or ordering is None:
        return {
            "success": False,
            "cause": "one or more required fields not found"
        }, 400

    # find the pr
    if MongoController.find_one("partyrank", {"base": True, "pr_id": pr_id}) is None:
        return {
            "success": False,
            "cause": "party rank not found"
        }, 404

    # validate orderings
    if not isinstance(ordering, list):
        return {
            "success": False,
            "cause": "entries field must be an array"
        }, 400

    # update user data
    MongoController.update_one(
        'partyrank',
        {
            "discord_id": user['_id'],
            "base": False,
            "pr_id": pr_id
        },
        {
            "$set": {"ordering": ordering}
        }
    )

    return {
        "success": True,
        "result": ordering
    }


@pr_api.route("/backgrounds")
def get_bg():

    backgrounds = MongoController.find('pr_backgrounds')

    '''
    {
        "_id": "ID",
        "title": "?",
        "link": "link"
    }
    '''

    res = []
    for entry in backgrounds:
        link = entry['link']
        res.append(link)

    json = {
        "success": True,
        "result": res
    }

    return jsonify(json)


