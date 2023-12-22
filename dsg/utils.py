import os

import requests

from discord.token_exchange import (
    get_oauth_user,
    get_user_info,
    refresh_oauth_user
)

from discord.metadata import push_metadata

from db.mongo_db import MongoController
from db.redis_db import RedisController


def send_dsg_log_webhook(json, headers={'Content-Type': "application/json"}):
    requests.post(
        os.environ.get('DSG_LOG_WEBHOOK_URL'),
        headers=headers,
        json=json
    )


def process_dsg_user(code):

    # Step 1: Get user tokens
    try:
        data = get_oauth_user(
            os.environ.get("DSG_CLIENT_ID"),
            os.environ.get("DSG_CLIENT_SECRET"),
            os.environ.get("DSG_REDIRECT_URI"),
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
        "dsg:%s" % discord_id,
        access_token,
        timeout=timeout
    )

    # Step 4: Store refresh_token in database
    MongoController.set_user(discord_id, refresh_token, db_name="dsg")

    # Step 5: Find id and uuid in database
    entry = MongoController.get_user(discord_id, db_name="dsg")

    if entry is None or entry.get("uuid") is None:
        return None
    
    # Step 6: Send metadata to Discord
    return push_metadata(
        os.environ.get("DSG_CLIENT_ID"),
        access_token,
        {
            "hypixel_link": 1
        }
    )


def _erase_user(discord_id):
    try:
        MongoController.delete_one(
            "users",
            {"_id": discord_id},
            db_name="dsg"
        )
    except:
        print("[WARNING] Could not delete user %s. Ignoring." % discord_id)


def override_user(discord_id):

    # Step 1: Find existing user
    entry = MongoController.get_user(discord_id, db_name="dsg")

    if not entry:
        return

    try:
        access_token = RedisController.get("dsg:%s" % discord_id)

        # Step 2: Use refresh token to generate key if needed
        if not access_token:

            refresh_token = entry.get("refresh_token")

            if not refresh_token:
                # Stop if no refresh token
                raise Exception("No refresh token for %s" % discord_id)
            
            # Step 3: Call Discord API to regenerate token
            data = refresh_oauth_user(
                os.environ.get("DSG_CLIENT_ID"),
                os.environ.get("DSG_CLIENT_SECRET"),
                refresh_token
            )
            access_token = data['access_token']
            
        # Step 4: Invalidate user metadata
        metadata_status = push_metadata(
            os.environ.get("DSG_CLIENT_ID"),
            access_token,
            {
                "hypixel_link": 0
            }
        )
        
        if not metadata_status:
            raise Exception("Could not erase user metadata %s" % discord_id)

    except Exception as e:
        print("[WARN] %s" % str(e))
    finally:
        # Step 5: Erase
        _erase_user(discord_id)

        # Step 6: Send webhook
        json = {
            "content": "Deleting user entry <@%s> with UUID `%s`" % (discord_id, entry.get('uuid'))
        }
        send_dsg_log_webhook(json)
