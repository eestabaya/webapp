import os
import hashlib

from flask import Blueprint, request, redirect, session

from discord import get_oauth_url

from dsg.utils import process_dsg_user

DSG_STATE_PARAM = "dsg_state"


dsg_linked_role_bp = Blueprint(
    "linked_role",
    __name__
)


@dsg_linked_role_bp.route("/linked-role")
def dsg_role_oauth():

    # build state
    state = hashlib.sha256(os.urandom(1024)).hexdigest()
    session[DSG_STATE_PARAM] = state

    oauth_url = get_oauth_url(
        os.environ.get("DSG_CLIENT_ID"),
        os.environ.get("DSG_REDIRECT_URI"),
        state,
        scope="role_connections.write identify"
    )
    
    return redirect(oauth_url)


@dsg_linked_role_bp.route("/callback")
def oauth_redirect():
    code = request.args.get('code')

    if code is None:
        return "zzsuperzz"

    state = session.get(DSG_STATE_PARAM)
    if not state or request.args.get("state", '') != state:
        return "Invalid state parameter.", 403
    
    # process DSG user here
    try:
        success = process_dsg_user(code)
    except:
        return "An error has occurred while processing this request.", 500

    # everything done, pop state and redirect
    session.pop(DSG_STATE_PARAM)

    if success is None:
        return "Could not find user. Use /verify to verify!", 404

    if not success:
        return "An error has occurred when calling Discord API", 500
    
    return "Verified! Go back to Discord!"
