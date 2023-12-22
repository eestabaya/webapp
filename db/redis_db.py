import os
import redis


class RedisController:
    DATABASE = None


    @staticmethod
    def get(k, decoding='utf-8'):
        result = RedisController.DATABASE.get(k)

        if result is not None:
            return result.decode(decoding)
        
        return None


    @staticmethod
    def set(k, v, timeout=None):
        RedisController.DATABASE.set(k, v, ex=timeout)

    
    @staticmethod
    def initialize():
        redis_ip = "redis_db"
        if "REDIS_HOST" in os.environ:
            redis_ip = os.environ['REDIS_HOST']

        redis_port = 6379
        if "REDIS_PORT" in os.environ:
            redis_port = os.environ['REDIS_PORT']

        db_index = 1
        if "REDIS_DB_INDEX" in os.environ:
            db_index = os.environ['REDIS_DB_INDEX']

        username, password = None, None
        if "REDIS_USERNAME" in os.environ and "REDIS_PASSWORD" in os.environ:
            username = os.environ['REDIS_USERNAME']
            password = os.environ['REDIS_PASSWORD']


        print("Redis: Connecting to {}:{}".format(redis_ip, redis_port))
        RedisController.DATABASE = redis.Redis(host=redis_ip,
                            db=db_index,
                            username=username,
                            password=password,
                            port=redis_port)
