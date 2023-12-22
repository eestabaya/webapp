import re

import requests

from db.redis_db import RedisController

BASE_CACHE_TIMEOUT = 120


def is_proper_mc_name(name):
    return len(name) <= 16 and re.fullmatch(r"^[a-zA-Z0-9_]+$", name)


def get_uuid_by_name(name):

    uuid = RedisController.get("mojang:%s" % name)

    if uuid is not None:
        return (uuid if uuid != "NULL_USER" else None)

    url = "https://api.mojang.com/users/profiles/minecraft/{}".format(name)

    r = requests.get(url)

    if r.status_code != 200:
        RedisController.set(
            "mojang:%s" % name,
            "NULL_USER",
            timeout=BASE_CACHE_TIMEOUT
        )
        return None
    
    json = r.json()
    uuid = json['id']

    RedisController.set(
        "mojang:%s" % name,
        uuid,
        timeout=BASE_CACHE_TIMEOUT
    )

    return uuid

