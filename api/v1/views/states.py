#!/usr/bin/python3
"""states.py"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """cash all state objects from storage"""
    states_list = []
    for state in storage.all("State").values():
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def getState_byId(state_id):
    """rout state data for specified id"""
    state_inst = storage.get(State, state_id)
    if state_inst is None:
        abort(404)
    return jsonify(state_inst.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_state(state_id):
    """Deletes A specified state by id"""
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)
    state_obj.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def post_state():
    """obtaining a state data instantiate state"""
    # receive a post request
    state_JData = request.get_json()
    # vallation checks
    if not state_JData:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in state_JData:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    # insatiate instant with request data
    state_inst = State(**state_JData)
    state_inst.save()
    return make_response(jsonify(state_inst.to_dict()), 201)


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def put_state(state_id):
    """update a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'created_at', 'updated_at']:
            setattr(state, attr, val)
    state.save()
    return jsonify(state.to_dict())
