import sys

from discord.interactions import Interaction

# list relevant command imports here
from godhack.commands import *
from dsg.interactions import *


def parse_interaction(interaction):
    interaction_type = interaction['type']

    # mainstream application command
    if interaction_type == 2:
        command_type = interaction['data']['type']

        # fetch and sanitize
        command_name = interaction['data']['name'].replace(" ", "")

        # slash command
        if command_type == 1:
            cls = getattr(
                sys.modules[__name__],
                "Command%s" % command_name.capitalize()
            )
            return cls(interaction)
        
        # user command
        if command_type == 2:
            cls = getattr(
                sys.modules[__name__],
                "UserI%s" % command_name.capitalize()
            )
            return cls(interaction)


    # not implemented
    return Interaction(interaction)
