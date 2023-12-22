import os
import sys
import uuid

# XXX Flask imports XXX

from flask import Flask
from flask import send_from_directory

from flask_cors import CORS

# XXX Flask imports XXX


# db
from db.mongo_db import MongoController
from db.redis_db import RedisController


# blueprints
from auth import login
from partyrank import partyrank
from skyblock import fetcher

from godhack import godhack
from dsg import dsg

# extras
from skyblock.s3_utils import S3


app = Flask(__name__)
CORS(app)

app.secret_key = str(uuid.uuid4())

registers = [
    login.auth_bp,
    partyrank.partyrank_bp,
    fetcher.skyblock_bp,
    godhack.godhack_bp,
    dsg.dsg_bp
]

for reg in registers:
    app.register_blueprint(reg)


if __name__ == "__main__":

    # initialize databases now
    MongoController.initialize()
    RedisController.initialize()

    # initialize S3
    S3.initialize()

    debug = os.environ.get('DEBUG', False)

    # Validate env vars if we are not on debug mode
    if not debug and not (
        os.environ.get("CLIENT_ID")
        and os.environ.get("CLIENT_SECRET")
        and os.environ.get("REDIRECT_URI")
    ):
        sys.exit("Missing one or more required environment variables!")

    app.run(debug=debug, port=8080, host='0.0.0.0')
