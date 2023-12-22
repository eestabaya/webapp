import os
import requests

HYPIXEL_BASE_URL = "https://api.hypixel.net"


def get_hypixel_player(uuid):

    API_KEY = os.environ.get("HYPIXEL_API_KEY")

    if API_KEY is None:
        return None

    headers = {
        "API-Key": API_KEY
    }

    query = {
        'uuid': uuid
    }

    # json["player"]["socialMedia"]["links"]["DISCORD"]

    url = "{}/{}".format(HYPIXEL_BASE_URL, "player")

    r = requests.get(url, headers=headers, params=query)

    if r.status_code != 200:
        return None
    
    json = r.json()

    player_data = json['player']

    return player_data


def get_player_discord(player_data):

    if player_data is None:
        return None
    
    #discord = player_data['socialMedia']['links']['DISCORD']
    discord = player_data.get('socialMedia', {}).get('links', {}).get('DISCORD', None)

    return discord
