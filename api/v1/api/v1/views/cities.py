#!/usr/bin/python3
"""Cities Routs"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<string:state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def getCites_byStIdd(state_id):
    """ git city by state ide """
    state_inst = storage.get(State, state_id)
    if state_inst is None:
        abort(404)
    cities_list = []
    for city in state_inst.cities:
        cities_list.append(city.to_dict())
    return jsonify(cities_list)


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 strict_slashes=False)
def getCity_byId(city_id):
    """get city by id"""
    city_inst = storage.get(City, city_id)
    if city_inst is None:
        abort(404)
    return jsonify(city_inst.to_dict())


@app_views.route('/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteCity_byID(city_id):
    """deletes a city by id"""
    city_inst = storage.get(City, city_id)
    if city_inst is None:
        abort(404)
    city_inst.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/states/<string:state_id>/cities/', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """create a new city"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    kwargs = request.get_json()
    kwargs['state_id'] = state_id
    city = City(**kwargs)
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id):
    """update a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, attr, val)
    city.save()
    return jsonify(city.to_dict())
