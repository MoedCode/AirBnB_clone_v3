#!/usr/bin/python3
"""States Ruts"""

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
def del_state(state_id):
    """Deletes A specified state by id"""
    state_obj = storage.get('State', state_id)
    if state_obj is None:
        abort(404)
    storage.delete(state_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/', methods=['POST'])
def post_state():
    """obtaining a state data instantiate state """
    # receive a post request
    state_JData = request.get_json()
    # vallation checks
    if not state_JData:
        abort(400, {'Not a JSON'})
    if not state_JData.get('name'):
        abort(400, {'Missing name'})

    # insatiate instant with request data
    state_inst = State(**state_JData)

    # update storage type with state data and save
    storage.new(state_inst)
    storage.save()
    # 201 indicates that the saving process is done
    return jsonify(state_inst.to_dict()), '201'


@app_views.route('/states/<string:state_id>/', methods=['PUT'])
def put_state(state_id):
    """ state data update state obtained"""
    # validation
    state_JData = request.get_json()
    if not state_JData:
        abort(400, {'Not a JSON'})
    if state_JData.get('name') is None:
        abort(400, {'Missing name'})
    # get state instance fro storage
    state_inst = storage.get('State', state_id)
    if state_inst is None:
        abort(404)
    # avoid keys that shouldn't be change
    void_keys = ['created_at', 'id', 'updated_at']
    for key, value in state_JData:
        if key not in void_keys:
            setattr(state_inst, key, value)
    # save changes to storage
    storage.save()

    return jsonify(state_inst.to_dict()), 200
