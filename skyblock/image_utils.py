import random

from db.mongo_db import MongoController

def get_random_image(query={}, projection={"_id": False}):
    images, _ = get_images(query=query, projection=projection)

    return random.choice(images)


def get_images(
    query={},
    projection={"_id": False},
    page_limit=None,
    page_number=None
):
    images = MongoController.find(
        "skyblock",
        query=query,
        projection=projection
    )

    # limit as required
    if page_limit and page_limit.isdigit():
        if page_number and page_number.isdigit():
            images = images.skip(int(page_limit) * (int(page_number) - 1))
        images = images.limit(int(page_limit))

    image_return = list(images)

    return image_return
