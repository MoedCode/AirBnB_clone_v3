#!/usr/bin/python3
from api.v1.views import app_view
from flask import jsonify

@app_view.route('/status', methods=['GET'])
def api_status():
    "Routs API status"
    return jsonify({"status":"ok"})
