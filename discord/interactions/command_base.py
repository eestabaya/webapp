from discord.interactions import Interaction

class DiscordCommand(Interaction):

    def __init__(self, interaction):
        self.interaction_data = interaction['data']
        self.base_options = interaction['data'].get('options')

        Interaction.__init__(self, interaction)


    def get_interaction_data(self):
        return self.interaction_data


    def get_interaction_options(self):
        return self.base_options
