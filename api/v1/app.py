#!/usr/bin/python3
from flask import Flask

from models import storage
from api.v1.views import app_view
import os

APP = Flask(__name__)

APP.register_blueprint(app_view, url_prefix='/api/v')
@APP.teardown_appcontext
def teardown(exception):
    "CClose storage"
    storage.close()
if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    APP.run(host=host, port=port, threaded=True)