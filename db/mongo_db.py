import os
import pymongo


class MongoController:
    DATABASE_CLIENT = None
    DEFAULT_DATABASE = "base"


    @staticmethod
    def set_user(discord_id, refresh_token, db_name=None):
        
        # Create user if does not exist
        res = MongoController.get_user(discord_id, db_name=db_name)

        if res is None:
            MongoController.insert(
                "users",
                {
                    "_id": discord_id,
                    "permissions": []
                },
                db_name=db_name
            )

        # Set refrseh_token in database
        MongoController.update_one(
            "users",
            {
                "_id": discord_id
            },
            {
                "$set": {
                    "refresh_token": refresh_token
                }
            },
            db_name=db_name
        )

    
    @staticmethod
    def get_user(discord_id, db_name=None):
        return MongoController.find_one(
            "users",
            {
                "_id": discord_id
            },
            db_name=db_name
        )
    

    @staticmethod
    def _get_database(db_name):
        if db_name is None:
            db_name = MongoController.DEFAULT_DATABASE

        return MongoController.DATABASE_CLIENT[db_name]         


    @staticmethod
    def insert(col, data, db_name=None):
        db = MongoController._get_database(db_name)
        db[col].insert(data)

    
    @staticmethod
    def insert_many(col, data_arr, db_name=None):
        db = MongoController._get_database(db_name)
        db[col].insert_many(data_arr)

    
    @staticmethod
    def find(col, query={}, projection=None, db_name=None):
        db = MongoController._get_database(db_name)
        return db[col].find(query, projection=projection)
    

    @staticmethod
    def find_one(col, query, projection=None, db_name=None):
        db = MongoController._get_database(db_name)
        return db[col].find_one(query, projection=projection)
    

    @staticmethod
    def update_one(col, query, data, db_name=None):
        db = MongoController._get_database(db_name)
        db[col].update_one(query, data)


    @staticmethod
    def delete_one(col, query, db_name=None):
        db = MongoController._get_database(db_name)
        db[col].delete_one(query)


    @staticmethod
    def initialize():
        mongo_ip = "localhost"
        if "MONGO_HOST" in os.environ:
            mongo_ip = os.environ['MONGO_HOST']
        db_connect_string = "mongodb://{}:27017".format(mongo_ip)

        db_auth_source = "admin"
        if "MONGO_AUTH_DATABASE" in os.environ:
            db_auth_source = os.environ['MONGO_AUTH_DATABASE']

        username, password = None, None
        if "MONGO_USERNAME" in os.environ and "MONGO_PASSWORD" in os.environ:
            username = os.environ['MONGO_USERNAME']
            password = os.environ['MONGO_PASSWORD']

        if "MONGO_DEFAULT_DATABASE" in os.environ:
            MongoController.DEFAULT_DATABASE = os.environ['MONGO_DEFAULT_DATABASE']

        timeout = 1500

        print("Connecting to {}".format(db_connect_string))
        client = pymongo.MongoClient(db_connect_string,
                                    username=username,
                                    password=password,
                                    authSource=db_auth_source,
                                    serverSelectionTimeoutMS=timeout)
        
        MongoController.DATABASE_CLIENT = client
