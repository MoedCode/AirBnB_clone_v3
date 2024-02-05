#!/usr/bin/python3
<<<<<<< HEAD
from flask import jsonify
from models.state import State, abort
from models import storage
from api.v1.views import app_views


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
