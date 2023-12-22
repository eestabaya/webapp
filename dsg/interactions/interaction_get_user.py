from discord.interactions.command_base import DiscordCommand
from discord.interactions.user_base import UserInteraction

from db.mongo_db import MongoController

from discord import DiscordEmbed

USERS_COL = "users"


def get_user(discord_id=None, minecraft_uuid=None):
    query = {}

    if discord_id:
        query["_id"] = discord_id
    
    if minecraft_uuid:
        query["uuid"] = minecraft_uuid

    entry = MongoController.find_one(
        USERS_COL,
        query,
        db_name="dsg"
    )

    # send message accordingly
    if entry is None or not entry.get('uuid'):
        embed = DiscordEmbed(description="Could not find verified user", color=0xFF0000)
    else:
        target_id = entry['_id']
        mc_uuid = entry['uuid']

        # build embed
        embed = DiscordEmbed(description="Search successful", color=0x00FF00)

        embed.add_field(
            "User",
            "<@%s>" % target_id,
            inline=True
        )
        embed.add_field("IGN", "`NOT IMPLEMENTED`", inline=True)
        embed.add_field("Minecraft UUID", mc_uuid, inline=False)

    return {
        "type": 4,
        "data": {
            "embeds": [embed.get_embed()],
            "flags": (1 << 6)
        }
    }


class CommandGetuser(DiscordCommand):
    
    def __init__(self, interaction):
        DiscordCommand.__init__(self, interaction)


    def get_return_data(self):
        options = super().get_interaction_options()

        discord_id = None
        minecraft_uuid = None

        for option in options:
            
            if option['name'] == "discord":
                discord_id = option['options'][0]['value']

            if option['name'] == "minecraft":
                minecraft_uuid = option['options'][0]['value']

        return get_user(
            discord_id=discord_id,
            minecraft_uuid=minecraft_uuid
        )


class UserIGetuser(UserInteraction):
    
    def __init__(self, interaction):
        UserInteraction.__init__(self, interaction)


    def get_return_data(self):
        target_id = super().get_target_user_id()
        
        return get_user(discord_id=target_id)
