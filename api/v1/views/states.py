#!/usr/bin/python3
"""comment for file"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states/', methods=['GET'])
def get_states():
    """cash all state objects from storage"""
    states_obj = storage.all('State')
    states_lis = []
    for state in states_obj.values():
        states_lis.append(state.to_dict())
    return jsonify(states_lis)


@app_views.route('/states/<string:state_id>/', methods=['GET'])
def getState_byId(state_id):
    """rout state data for specified id"""
    state_inst = storage.get(State, state_id)
    if not state_inst:
        abort(404, 'Not found')
    return jsonify(state_inst.to_dict()), 200


@app_views.route('/states/<string:state_id>/', methods=['DELETE'])
def del_state_byId(state_id):
    """Deletes A   specified state by id"""
    state_obj = storage.get('State', state_id)
    if state_obj is None:
        abort(404)
    storage.delete(state_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<string:state_id>/', methods=['PUT'])
def putstate(state_id):
    """put state"""
    response = request.get_json()
    if not response:
        abort(400, {'Not a JSON'})
    if response.get('name') is None:
        abort(400, {'Missing name'})
    stateObject = storage.get('State', state_id)
    if stateObject is None:
        abort(404)
    ignoreKeys = ['id', 'created_at', 'updated_at']
    for key, val in response.items():
        if key not in ignoreKeys:
            setattr(stateObject, key, val)
    storage.save()
    return jsonify(stateObject.to_dict()), '200'


@app_views.route('/states/', methods=['POST'])
def poststate():
    """post state"""
    response = request.get_json()
    if not response:
        abort(400, {'Not a JSON'})
    if not response.get('name'):
        abort(400, {'Missing name'})
    stateObject = State(**response)
    storage.new(stateObject)
    storage.save()
    return jsonify(stateObject.to_dict()), '201'
