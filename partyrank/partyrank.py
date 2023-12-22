from flask import Blueprint, render_template, redirect, url_for, session

from auth.auth_utils import require_auth

from partyrank.api import pr_api
from partyrank.utils import validate_entries

from db.mongo_db import MongoController


partyrank_bp = Blueprint(
    "partyrank",
    __name__,
    static_folder="static",
    template_folder="templates",
    url_prefix="/partyrank"
)

partyrank_bp.register_blueprint(pr_api)


# im making the createpr endpoint in here, idk if you would rather want it in a sep file but thats an easy change if you do
#@mod.route("/createpr", methods=["GET", "POST"])
#def createpr():
#    if request.method == "POST":
#        print(request.form['song_name'])
#    return "ok", 200


@partyrank_bp.route("/")
def get_partyrank():
    pr_default = MongoController.find_one(
        'partyrank',
        {
            "_id": "DEFAULT_PR_CONFIGURATION"
        }
    )
    
    if pr_default is None:
        return "something bad happened", 500

    pr_id = pr_default['pr_id']

    return redirect(
        url_for("partyrank.load_pr", pr_id=pr_id)
    )



@partyrank_bp.route("/<pr_id>")
@require_auth()
def load_pr(pr_id):

    # TODO add a permission check later

    # find associated PR first
    pr_base = MongoController.find_one(
        'partyrank',
        {
            "pr_id": pr_id,
            "base": True
        }
    )

    # catch if we are accessing unknown PR
    if pr_base is None:
        return "This party rank isn't defined", 404

    pr_title = pr_base['title']
    songs = pr_base['entries']

    # Find if previous data exists
    discord_id = session['discord_id']

    pr_info = MongoController.find_one(
        'partyrank',
        {
            "discord_id": discord_id,
            "pr_id": pr_id,
            "base": False
        }
    )

    # previous data DNE: make new one
    if pr_info is None:

        # copy over PR songs
        ordering = [entry_id for entry_id in songs.keys()]

        # prepare information
        pr_info = {
            "discord_id": discord_id,
            "base": False,
            "pr_id": pr_id,
            "ordering": ordering
        }

        # insert the user data
        MongoController.insert('partyrank', pr_info)

    # ensure that all songs in ordering appear in the master song list
    ordering = validate_entries(songs, pr_info)

    # process all songs to be returned in correct order
    data_array = []

    for entry_id in ordering:
        entry = songs.get(entry_id)

        data = {
            "id": entry_id,
            "anime_title": entry['anime_title'],
            "song_title": entry['song_title'],
            "artist": entry["artist"],
            "link": entry["link"]
        }
        data_array.append(data)

    return render_template(
        "partyrank.html",
        pr_title=pr_title,
        pr_id=pr_id,
        data_array=data_array
    )

