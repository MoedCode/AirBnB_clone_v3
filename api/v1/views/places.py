#!/usr/bin/python3
"""places handlers"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<string:city_id>/places', methods=['GET'],
                 strict_slashes=False)
def getPlacesByCity(city_id):
    """get list of places"""
    ob = storage.all('Place')
    if not storage.get(City, city_id):
        abort(404)
    ll = []
    for place in ob.values():
        if city_id == place.city_id:
            ll.append(place.to_dict())
    if len(ll) <= 0:
        return 0
    return jsonify(ll)


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
def getPlacesByid(place_id):
    """get place by id"""
    ob = storage.get(Place, place_id)
    if ob is None:
        abort(404)
    return jsonify(ob.to_dict())


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def deletePlacesByid(place_id):
    """delete place by id"""
    ob = storage.get(Place, place_id)
    if ob is None:
        abort(404)
    else:
        storage.delete(ob)
        storage.save()
        return jsonify({}), 200


@app_views.route('/cities/<string:city_id>/places', methods=['POST'],
                 strict_slashes=False)
def createPlaces(city_id):
    """create place"""
    response = request.get_json()
    if not response:
        abort(400, {'Not a JSON'})
    if not response.get('name'):
        abort(400, {'Missing name'})
    if not response.get('user_id'):
        abort(400, {'Missing user_id'})
    if not storage.get(City, city_id) or not storage.get(User, response.get('\
            user_id')):
        abort(404)
    stateObject = Place(**response)
    setattr(stateObject, 'city_id', city_id)
    storage.new(stateObject)
    storage.save()
    return jsonify(stateObject.to_dict()), '201'


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
def putplace(place_id):
    '''update place'''
    response = request.get_json()
    if not response:
        abort(400, {'Not a JSON'})
    stateObject = storage.get(Place, place_id)
    if stateObject is None:
        abort(404)
    ignoreKeys = ['id', 'created_at', 'updated_at', 'city_id', 'user_id']
    for key, val in response.items():
        if key not in ignoreKeys:
            setattr(stateObject, key, val)
    storage.save()
    return jsonify(stateObject.to_dict()), '200'
