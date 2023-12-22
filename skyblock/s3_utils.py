import os

import boto3

from db.mongo_db import MongoController


class S3:

    S3_CLIENT = None

    @staticmethod
    def reload_objects(bucket_name):
        paginator = S3.S3_CLIENT.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket='skyblock')
        #bucket = S3.S3_CLIENT.list_objects_v2(Bucket=bucket_name)

        result = []

        for page in pages:
            for item in page['Contents']:
                path = item['Key']

                # imgur/hash.jpg
                parts = path.split("/")

                source_type = parts[0]
                image = "https://sb.litdab.xyz/%s" % path
                raw_hash = parts[-1]
                original_creator = "unknown"
                nsfw = False

                # Check if exists
                entry = MongoController.find_one(
                    "skyblock",
                    {
                        "source_type": source_type,
                        "raw_hash": raw_hash
                    }
                )

                if entry:
                    continue

                # Create new entry

                json = {
                    "source_type": source_type,
                    "image": image,
                    "raw_hash": raw_hash,
                    "original_creator": original_creator,
                    "nsfw": nsfw
                }

                result.append(json)

        # insert properly
        if len(result) > 0:
            MongoController.insert_many(
                "skyblock",
                result.copy()
            )

        return result


    @staticmethod
    def initialize():
        url = os.environ.get("S3_URL")
        access_key = os.environ.get("S3_ACCESS_KEY")
        secret_key = os.environ.get("S3_SECRET_KEY")

        if (url is None
            or access_key is None
            or secret_key is None):
            print("[WARNING] Missing environment variables for S3 service")
            return
        
        S3.S3_CLIENT = boto3.client(
            's3',
            endpoint_url = url,
            aws_access_key_id = access_key,
            aws_secret_access_key = secret_key
        )
