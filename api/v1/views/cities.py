#!/usr/bin/python3
"""City object that handles all default RESTFul API actions"""

from flask import abort, request, jsonify
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=['GET'])
def get_cities(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route("/cities/<city_id>", methods=['GET'])
def get_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=['DELETE'])
def delete_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=['POST'])
def post_city(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    request_data = request.get_json()
    if not request_data or 'name' not in request_data:
        return jsonify('Invalid data'), 400

    new_city = City(**request_data)
    new_city.state_id = state_id
    storage.new(new_city)
    storage.save()

    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=['PUT'])
def put_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    request_data = request.get_json()
    if not request_data:
        return jsonify('Invalid data'), 400

    for key, value in request_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, value)

    storage.save()
    return jsonify(city.to_dict()), 200
