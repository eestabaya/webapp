
class Interaction:

    def __init__(self, interaction):
        self.interaction = interaction
        self._process_base_interaction_data(interaction)


    def _process_base_interaction_data(self, interaction):
        self.interaction_id = interaction['id']
        self.application_id = interaction['application_id']
        self.token = interaction['token']

        # translate user object
        self.interaction_user = interaction.get('user')
        if not self.interaction_user:
            self.interaction_user = interaction['member']['user']


    def _get_full_interaction(self):
        return self.interaction
    

    def get_interaction_user(self):
        return self.interaction_user
    

    def get_continuation_token(self):
        return self.token
    

    def get_return_data(self):
        return {
            "type": 4,
            "data": {
                "content": "Not implemented yet.",
                "flags": (1 << 6)
            }
        }
