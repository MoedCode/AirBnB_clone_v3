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

# POST
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
