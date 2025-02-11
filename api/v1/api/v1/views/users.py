#!/usr/bin/python3
""" Users Routs"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def list_users():
    """list all users instances"""
    users_list = []
    user_VLst = storage.all(User).values()
    for user in user_VLst:
        users_list.append(user.to_dict())
    return jsonify(users_list)


@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
def getUser_byId(user_id):
    """gets a user instance by id"""
    user_inst = storage.get(User, user_id)
    if user_inst is None:
        abort(404)
    return jsonify(user_inst.to_dict())


@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteUser_byId(user_id):
    """gets a user instance by id , then Delete it"""
    user_inst = storage.get(User, user_id)
    if user_inst is None:
        abort(404)
    user_inst.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """obtain user Data && instantiate User instance """
    userJ_data = request.get_json()
    # data validation
    if not userJ_data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'email' not in userJ_data:
        return make_response(jsonify({'error': 'Missing email'}), 400)
    if 'password' not in userJ_data:
        return make_response(jsonify({'error': 'Missing password'}), 400)
    # now data is valid use to create user instance
    user_inst = User(**userJ_data)
    # update storage type with user instance and save
    user_inst.save()
    return make_response(jsonify(user_inst.to_dict()), 201)


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """update a user instance"""
    user_inst = storage.get(User, user_id)
    if user_inst is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user_inst, attr, val)
    user_inst.save()
    return jsonify(user_inst.to_dict())
