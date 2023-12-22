import requests

API_VERSION = "10"
DISCORD_API_BASE_URL = "https://discord.com/api/v{}".format(API_VERSION)


def get_user_info(access_token):
    
    headers = {
        'Authorization': "Bearer {}".format(access_token)
    }

    response = requests.get(
        "%s/users/@me" % DISCORD_API_BASE_URL,
        headers=headers
    )

    response.raise_for_status()

    return response.json()


def get_oauth_user(
        client_id,
        client_secret,
        redirect_uri,
        code
    ):
    
    # get env vars
    # CLIENT_ID = os.environ.get("CLIENT_ID")
    # CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
    # REDIRECT_URI = os.environ.get("REDIRECT_URI")

    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        "redirect_uri": redirect_uri,
        'grant_type': "authorization_code",
        'code': code
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(
        "%s/oauth2/token" % DISCORD_API_BASE_URL,
        data=payload,
        headers=headers
    )

    response.raise_for_status()

    return response.json()


def refresh_oauth_user(
        client_id,
        client_secret,
        refresh_token
    ):

    # get env vars
    # CLIENT_ID = os.environ.get("CLIENT_ID")
    # CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(
        "%s/oauth2/token" % DISCORD_API_BASE_URL,
        data=payload,
        headers=headers
    )

    response.raise_for_status()

    return response.json()
