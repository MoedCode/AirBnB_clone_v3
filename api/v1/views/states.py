#!/usr/bin/python3
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.state import State
from models import storage
from models.user import User

# Retrieves the list of all /Retrieves a


@app_views.route('/states/', methods=['GET'])
def get_states():
    "cash all state objects from storage"
    states_list = []
    states_inst_list = storage.all('State')
    for state_inst in states_inst_list:
        states_list.append(state_inst.to_dict())
    return (states_list)


@app_views.route('/states/<string:state_id>/', methods=['GET'])
def getState_byId(state_id):
    "rout state data for specified id"
    state_inst = storage.get(State, state_id)
    if not state_inst:
        abort(404, 'Not found')
    return jsonify(state_inst.to_dict()), 200

    # DELETE/


@app_views.route('/states/<string:state_id>/', methods=['DELETE'])
def del_state(state_id):
    """Deletes A specified state by id"""
    state_obj = storage.get('State', state_id)
    if state_obj is None:
        abort(404)
    storage.delete(state_obj)
    storage.save()
    return jsonify({}), 200

@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def getUser():
    """get user"""
    ob = storage.all('User')
    ll = []
    for state in ob.values():
        ll.append(state.to_dict())
    return jsonify(ll)


@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
def getUserById(user_id):
    """user amentiy"""
    element = storage.get(User, user_id)
    if element:
        return jsonify(element.to_dict())
    else:
        abort(404)


@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def DeleteUserById(user_id):
    """delete amentiy"""
    element = storage.get(User, user_id)
    if not element:
        abort(404)
    else:
        storage.delete(element)
        storage.save()
        return (jsonify({}), 200)


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def CreateUser():
    """Post user"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if not data.get('email'):
        return jsonify({"error": "Missing email"}), 400
    if not data.get('password'):
        return jsonify({"error": "Missing password"}), 400
    user = User(**data)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def UpdateUser(user_id):
    """Update user"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    else:
        ignoreKeys = ['id', 'created_at', 'updated_at']
        for key, val in data.items():
            if key not in ignoreKeys:
                setattr(user, key, val)
        storage.save()
        return jsonify(user.to_dict()), '200'
