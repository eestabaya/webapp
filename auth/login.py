import os
import hashlib

from flask import Blueprint, redirect, request, session

import auth.user_manager
from discord import get_oauth_url

auth_bp = Blueprint("auth", __name__)


@auth_bp.route('/login')
def login():

    # if there is auth, send back
    if 'discord_id' in session:
        target = '/main'
        if 'target' in session:
            target = session.pop('target')

        return redirect(target)

    # build state
    state = hashlib.sha256(os.urandom(1024)).hexdigest()
    session['state'] = state

    oauth_url = get_oauth_url(
        os.environ.get("CLIENT_ID"),
        os.environ.get("REDIRECT_URI"),
        state
    )

    # go !
    return redirect(oauth_url)


@auth_bp.route('/logout')
def logout():

    if 'discord_id' in session:
        session.pop('discord_id')

    if 'state' in session:
        session.pop('state')

    if 'target' in session:
        session.pop('target')

    return redirect('/')


@auth_bp.route("/oauth/discord")
def oauth():
    code = request.args.get('code')

    if code is None:
        return "zzsuperzz"

    state = session.get('state')
    if not state or request.args.get('state', '') != state:
        return "Invalid state parameter.", 403

    auth.user_manager.init_user(code)

    target = "/validate"
    # redirect as necessary
    if 'target' in session:
        target = session.pop('target')

    # everything done, pop state and redirect
    session.pop('state')

    return redirect(target)
