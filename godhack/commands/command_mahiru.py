import random

from discord.interactions.command_base import DiscordCommand

from db.mongo_db import MongoController


class CommandMahiru(DiscordCommand):
    
    def __init__(self, interaction):
        DiscordCommand.__init__(self, interaction)


    def get_return_data(self):
        images = MongoController.find(
            "mahiru",
            query={"title": "mahiru"},
            projection={"_id": False}
        )
        image = random.choice(list(images))

        return {
            "type": 4,
            "data": {
                "content": image['link']
            }
        }
