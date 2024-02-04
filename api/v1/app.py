#!/usr/bin/python3
"""this is flask APP"""

from flask import Flask, jsonify
from models import storage
from os import getenv
from api.v1.views import app_views
from flask_cors import CORS

APP = Flask(__name__)
APP.register_blueprint(app_views)
cors = CORS(APP, resources={r"/api/v1/*": {"origins": "*"}})
APP.url_map.strict_slashes = False

HOST = getenv('HBNB_API_HOST')
PORT = getenv('HBNB_API_PORT')


@APP.teardown_appcontext
def close(self):
    """close the session"""
    storage.close()


@APP.errorhandler(404)
def Error_404(error):
    '''return a Error dictionary with  '''
    ErrDict = {'error': 'Not found'}
    return jsonify(ErrDict), 404


if __name__ == "__main__":

    if not HOST:
        HOST = '0.0.0.0'
    if not PORT:
        port = '5000'
    APP.run(host=HOST, port=PORT, threaded=True)
