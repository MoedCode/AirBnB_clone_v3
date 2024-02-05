#!/usr/bin/python3
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.state import State
from models import storage
from models.user import User

def instantiate_user():
    """obtain user Data && instantiate User instance """
    usr_JData = request.get_json()
    # data validation
    if not usr_JData:
        return jsonify({"error":"Not a Json"}), 400
    if not usr_JData.get('email'):
        return jsonify({"error": "Missing email"}), 400
    if not usr_JData :
        return jsonify({"error": "Missing password"}), 400
    # now data is valid use to create user instance
    user_inst = User(**usr_JData)
    # update storage type with user instance and save
    storage.new(user_inst)
    storage.save()
    # return user data with 201 indicates that saving process Done
    return jsonify(user_inst.to_dict()), 201
