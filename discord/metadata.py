import requests

API_VERSION = "10"

def push_metadata(
        client_id,
        access_token,
        metadata
    ):

    url = "https://discord.com/api/v%s/users/@me/applications/%s/role-connection" % (API_VERSION, client_id)

    body = {
        "metadata": metadata
    }

    headers = {
        'Authorization': "Bearer %s" % access_token,
        'Content-Type': "application/json"
    }

    r = requests.put(url, json=body, headers=headers)

    try:
        r.raise_for_status()
        return True
    except:
        return False
