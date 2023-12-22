import uuid

import datetime

from discord.interactions.command_base import DiscordCommand

from mojang import (
    is_proper_mc_name,
    get_uuid_by_name
)

from db.mongo_db import MongoController

from discord import DiscordEmbed

BLACKLIST_COL = "chunger"


class CommandGetblacklist(DiscordCommand):
    
    def __init__(self, interaction):
        DiscordCommand.__init__(self, interaction)


    def get_return_data(self):

        # step 1: get username from interaction data
        options = super().get_interaction_options()
        name = options[0]['value']

        # step 2: validate username/UUID
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
            
            # translate as required
            minecraft_uuid = get_uuid_by_name(name)
            if minecraft_uuid is None:
                return {
                    "type": 4,
                    "data": {
                        "content": "Could not find UUID from Minecraft username",
                        "flags": (1 << 6)
                    }
                }
            
        # step 3: find entry
        entry = MongoController.find_one(
            BLACKLIST_COL,
            {
                "uuid": minecraft_uuid
            },
            db_name="dsg"
        )

        timestamp = None

        if not entry:
            embed = DiscordEmbed(description="Could not find blacklisted user", color=0xFF0000)
        else:
            reason = entry.get("reason")
            invoker = entry.get("invoker")
            timestamp = entry.get("timestamp")

            if not reason:
                reason = "Unknown"

            if invoker:
                invoker = "<@%s>" % invoker
            else:
                invoker = "Unknown"

            if timestamp:
                timestamp = datetime.datetime.fromtimestamp(timestamp).isoformat()
            else:
                timestamp = None

            # build embed
            embed = DiscordEmbed(description="Search successful", color=0x00FF00)

            embed.add_field(
                "Invoker",
                invoker,
                inline=True
            )
            embed.add_field(
                "Minecraft UUID",
                minecraft_uuid,
                inline=True
            )
            embed.add_field(
                "Reason",
                reason,
                inline=False
            )
            
            override_code = entry.get("override")
            if override_code:
                embed.set_footer("Override: %s" % override_code)

        return {
            "type": 4,
            "data": {
                "embeds": [embed.get_embed(timestamp=timestamp)],
                "flags": (1 << 6)
            }
        }
