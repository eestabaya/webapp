import uuid

from discord.interactions.command_base import DiscordCommand

from dsg.utils import override_user, send_dsg_log_webhook

from mojang import (
    is_proper_mc_name,
    get_uuid_by_name
)

from hypixel import (
    get_hypixel_player,
    get_player_discord
)

from db.mongo_db import MongoController

USERS_COL = "users"
BLACKLIST_COL = "chunger"

class CommandVerify(DiscordCommand):
    
    def __init__(self, interaction):
        DiscordCommand.__init__(self, interaction)


    def get_return_data(self):

        # init
        user = super().get_interaction_user()
        discord_id = user['id']

        # workflow

        # step 1: get username from interaction data
        options = super().get_interaction_options()
        name = options[0]['value']

        # step 2: process name/uuid
        try:
            uuid.UUID(name)
            minecraft_uuid = name.replace("-", "")
        except:
            if not is_proper_mc_name(name):
                return {
                    "type": 4,
                    "data": {
                        "content": "Invalid Minecraft username",
                        "flags": (1 << 6)
                    }
                }
            
            # call mojang to get uuid if necessary
            minecraft_uuid = get_uuid_by_name(name)
            if minecraft_uuid is None:
                return {
                    "type": 4,
                    "data": {
                        "content": "Could not find UUID from Minecraft username",
                        "flags": (1 << 6)
                    }
                }

        # step 3: IS BLACKLISTED?
        blacklist_entry = MongoController.find_one(
            BLACKLIST_COL,
            {
                "uuid": minecraft_uuid
            },
            db_name="dsg"
        )

        if blacklist_entry:
            reason = blacklist_entry.get("reason")
            if not reason:
                reason = "Unspecified"

            # LOG ATTEMPT
            send_dsg_log_webhook(
                {
                    "content": "User <@%s> attempt to verify with blacklisted user `%s`\nReason: ```%s```" % (discord_id, minecraft_uuid, reason)
                }
            )

            return {
                "type": 4,
                "data": {
                    "content": "YOU ARE BLACKLISTED FOR REASON: ```%s```" % reason,
                    "flags": (1 << 6)
                }
            }

        # step 4: call hypixel api
        player_data = get_hypixel_player(minecraft_uuid)

        if player_data is None:
            return {
                "type": 4,
                "data": {
                    "content": "Could not find Hypixel player",
                    "flags": (1 << 6)
                }
            }

        # step 5: check social discord
        hypixel_discord = get_player_discord(player_data)

        # step 6: validate
        discord_username = user['username']
        discriminator = user['discriminator']

        curr_discord = discord_username
        if discriminator != "0":
            curr_discord = "{}#{}".format(discord_username, discriminator)

        if curr_discord != hypixel_discord:
            return {
                "type": 4,
                "data": {
                    "content": "Discord on Hypixel does not match",
                    "flags": (1 << 6)
                }
            }
        
        # discord is valid

        # STOP: check if duplicate discord
        mc_entry = MongoController.find_one(
            USERS_COL,
            {
                "uuid": minecraft_uuid
            },
            db_name="dsg"
        )

        if mc_entry:

            if mc_entry['_id'] == discord_id:
                return {
                    "type": 4,
                    "data": {
                        "content": "You already linked your Minecraft account! Use the linked role Discord feature to get your role! (You will need to log in with Discord) https://cdn.litdab.xyz/dsg_linked_role.png",
                        "flags": (1 << 6)
                    }
                }
            
            # Forcefully override the account
            override_user(mc_entry['_id'])
        
        entry = MongoController.get_user(
            discord_id,
            db_name="dsg"
        )

        # INSERT !
        if entry:
            MongoController.update_one(
                USERS_COL,
                {
                    "_id": discord_id
                },
                {
                    "$set": {
                        "uuid": minecraft_uuid
                    }
                },
                db_name="dsg"
            )
        else:
            MongoController.insert(
                USERS_COL,
                {
                    "_id": discord_id,
                    "uuid": minecraft_uuid
                },
                db_name="dsg"
            )

        # LOG WEBHOOK

        json = {
            "content": "Discord user <@%s> now linked with UUID `%s`" % (discord_id, minecraft_uuid)
        }
        send_dsg_log_webhook(json)

        return {
            "type": 4,
            "data": {
                "content": "You have successfully linked your Minecraft account! Use the linked role Discord feature to get your role! (You will need to log in with Discord) https://cdn.litdab.xyz/dsg_linked_role.png",
                "flags": (1 << 6)
            }
        }
