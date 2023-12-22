import urllib


def get_oauth_url(
        client_id,
        redirect_uri,
        state,
        scope="identify"
    ):

    # oauth environment vars
    # CLIENT_ID = os.environ.get("CLIENT_ID")
    # REDIRECT_URI = os.environ.get("REDIRECT_URI")

    # if we dont have proper variables, raise exception
    #if CLIENT_ID is None or REDIRECT_URI is None:
    #    raise KeyError("MISSING ENVIRONMENT VARIABLES")

    # build oauth2 URL
    query = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": scope,
        "response_type": "code",
        "state": state
    }

    DISCORD_URL = "https://discord.com/api/oauth2/authorize"
    url = DISCORD_URL + "?" + urllib.parse.urlencode(query, quote_via=urllib.parse.quote)
    
    return url
