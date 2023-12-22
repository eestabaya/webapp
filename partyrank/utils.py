from db.mongo_db import MongoController

def validate_entries(master_list, pr_info):

    # go through songs missing in the user's ordering
    missing_ord = master_list.keys() - pr_info['ordering']
    for missing in missing_ord:
        pr_info['ordering'].append(missing)

    # go through songs no longer in the master list
    removed_songs = pr_info['ordering'] - master_list.keys()
    for removed in removed_songs:
        pr_info['ordering'].remove(removed)

    # update if necessary
    if len(missing_ord) > 0 or len(removed_songs) > 0:
        MongoController.update_one(
            'partyrank',
            {
                "discord_id": pr_info['discord_id'],
                "base": False,
                "pr_id": pr_info['pr_id']
            },
            {
                "$set": {"ordering": pr_info['ordering']}
            }
        )

    return pr_info['ordering']
