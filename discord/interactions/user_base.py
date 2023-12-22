from discord.interactions import Interaction

class UserInteraction(Interaction):

    def __init__(self, interaction):
        self.target_user_id = interaction['data']['target_id']

        Interaction.__init__(self, interaction)


    def get_target_user_id(self):
        return self.target_user_id
