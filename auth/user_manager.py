import os

from flask import session

from db.mongo_db import MongoController
from db.redis_db import RedisController

from discord.token_exchange import (
    get_oauth_user,
    get_user_info,
    refresh_oauth_user
)

from discord.utils import send_init_webhook


def _get_oauth_token(discord_id):

    access_token = RedisController.get(discord_id)

    # Check if token is expired
    if access_token is None:

        # get refresh token and renew access_token
        user = MongoController.get_user(discord_id)

        try:
            data = refresh_oauth_user(
                os.environ.get("CLIENT_ID"),
                os.environ.get("CLIENT_SECRET"),
                user['refresh_token']
            )
        except:
            raise Exception("Error with refresh token")
        
        access_token = data['access_token']
        timeout = data['expires_in']

        RedisController.set(
            discord_id,
            access_token,
            timeout=timeout
        )

    return access_token


def get_discord_info():
    discord_id = session['discord_id']
    access_token = _get_oauth_token(discord_id)

    return get_user_info(access_token)


def init_user(code):

    # Step 1: Get user tokens
    try:
        data = get_oauth_user(
            os.environ.get("CLIENT_ID"),
            os.environ.get("CLIENT_SECRET"),
            os.environ.get("REDIRECT_URI"),
            code
        )
    except:
        raise Exception("Error while initializing user")
    
    access_token = data['access_token']
    refresh_token = data['refresh_token']
    timeout = data['expires_in']

    # Step 2: Get Discord ID
    user_info = get_user_info(access_token)
    discord_id = user_info['id']

    # Step 3: Store access_token in cache
    RedisController.set(
        discord_id,
        access_token,
        timeout=timeout
    )

    # Step 4: Store refresh_token in database
    MongoController.set_user(discord_id, refresh_token)

    # Step 5: Store discord_id in session
    session['discord_id'] = discord_id

    # Step 6: Send information, user initialized
    send_init_webhook(user_info)
