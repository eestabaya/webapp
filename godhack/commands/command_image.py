from discord.interactions.command_base import DiscordCommand

from skyblock.image_utils import get_random_image


class CommandImage(DiscordCommand):
    
    def __init__(self, interaction):
        DiscordCommand.__init__(self, interaction)


    def get_return_data(self):
        query = {}
        #projection = {}
        image = get_random_image(query=query)

        #return super().get_return_data()
        return {
            "type": 4,
            "data": {
                "content": image['image']
            }
        }
