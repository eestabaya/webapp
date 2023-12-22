from functools import wraps

from flask import session, request, redirect, url_for

from db.mongo_db import MongoController

def _not_logged_in(json_return):
    # return raw json or redirect as required by endpoint
    if json_return:
        return {
            "success": False,
            "cause": "Unauthorized"
        }, 401
    
    # redirecting, save target path
    session['target'] = request.path
    return redirect(
        url_for("auth.login")
    )


def require_auth(permission=None, json_return=False):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):

            # check if active session
            discord_id = session.get('discord_id')
            if discord_id is None:
                return _not_logged_in(json_return)

            # permission check
            if permission:

                # step 1: get user
                user = MongoController.get_user(discord_id)
                permissions = user['permissions']

                # step 2: compare permission
                if '*' not in permissions and permission not in permissions:
                    # return raw json or display message as required by endpoint
                    if json_return:
                        return {
                            "success": False,
                            "cause": "Insufficient Permissions"
                        }, 403
                    
                    return "Insufficient Permissions", 403

            return f(*args, **kwargs)

        return wrapper
    return decorator
