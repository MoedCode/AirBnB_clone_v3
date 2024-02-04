#!/usr/bin/python3
""" handles all default RESTFul API actions"""

from api.v1.views import app_views
from models import storage
from models.state import State
from flask import abort, jsonify, request, Flask


@app_views.route("/states")
def all_states():
    """Return all states"""
    states = storage.all(State).values()
    state_list = [state.to_dict() for state in states]
    return jsonify(state_list)


@app_views.route("/states/<state_id>")
def get_state(state_id):
    """Get state by ID"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=['DELETE'])
def delete_state(state_id):
    """Delete state by ID"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=['POST'])
def post_state():
    """Create a new state"""
    request_data = request.get_json()
    if not request_data:
        return jsonify('Not a JSON'), 400
    if 'name' not in request_data:
        return jsonify('Missing name'), 400

    new_state = State(**request_data)
    storage.new(new_state)
    storage.save()

    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=['PUT'])
def put_state(state_id):
    """Update state by ID"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    request_data = request.get_json()
    if not request_data:
        return jsonify('Not a JSON'), 400
    for key, value in request_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
