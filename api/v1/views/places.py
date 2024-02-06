#!/usr/bin/python3
"""Places Routs"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity
from models.review import Review
from models.state import State


@app_views.route('/cities/<string:city_id>/places', methods=['GET'],
                 strict_slashes=False)
def getPlaces_CtyId(city_id):
    """get place by city idy"""
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)
    places_list = []
    for place in city_obj.places:
        places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
def getPlace_Id(place_id):
    """get place instance by id"""
    place_inst = storage.get(Place, place_id)
    if place_inst is None:
        abort(404)
    return jsonify(place_inst.to_dict())


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_placeById(place_id):
    """get place instance by id, delet place instance"""
    place_inst = storage.get(Place, place_id)
    if place_inst is None:
        abort(404)
    place_inst.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/cities/<string:city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """obtain city data , create place instance"""
    city_inst = storage.get(City, city_id)
    if city_inst is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    JData = request.get_json()
    if 'user_id' not in JData:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    user = storage.get(User, JData['user_id'])
    if user is None:
        abort(404)
    if 'name' not in JData:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    JData['city_id'] = city_id
    place = Place(**JData)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """obtain place data , update place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'user_id', 'city_id', 'created_at',
                        'updated_at']:
            setattr(place, attr, val)
    place.save()
    return jsonify(place.to_dict())


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def searchCreatPlace():
    """searchCreatPlace"""
    if request.get_json() is not None:
        place_arg = request.get_json()
        ST_arg = place_arg.get('states', [])
        cities = place_arg.get('cities', [])
        amenities = place_arg.get('amenities', [])
        amenity_objects = []
        for amenity_id in amenities:
            amenity = storage.get(Amenity, amenity_id)
            if amenity:
                amenity_objects.append(amenity)
        if ST_arg == cities == []:
            places = storage.all('Place').values()
        else:
            places = []
            for state_id in ST_arg:
                state = storage.get(State, state_id)
                state_cities = state.cities
                for city in state_cities:
                    if city.id not in cities:
                        cities.append(city.id)
            for city_id in cities:
                city = storage.get(City, city_id)
                for place in city.places:
                    places.append(place)
        confirmed_places = []
        for place in places:
            place_amenities = place.amenities
            confirmed_places.append(place.to_dict())
            for amenity in amenity_objects:
                if amenity not in place_amenities:
                    confirmed_places.pop()
                    break
        return jsonify(confirmed_places)
    else:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
