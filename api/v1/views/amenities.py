#!/usr/bin/python3
"""Amenity object that handles all default RESTFul API actions"""

from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models import storage
import jason


@app_views.route("/amenities", methods=['GET'])
def get_all_amenities():
    """retuen all aminities """
    amenities = storage.all(Amenity).values()
    amenity_list = [amenity.to_dict() for amenity in amenities]
    return jsonify(amenity_list)

@app_views.route("/amenities/<amenity_id>", methods=['GET'])
def get_amenity(amenity_id):
    """retuen all aminities"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())

@app_views.route("/amenities/<amenity_id>", methods=['DELETE'])
def delete_amenity(amenity_id):
    """delete method"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200

@app_views.route("/amenities", methods=['POST'])
def create_amenity():
    """post method"""
    request_data = request.get_json()
    if not request_data:
        return jsonify(error='Not a JSON'), 400
    if 'name' not in request_data:
        return jsonify(error='Missing name'), 400

    new_amenity = Amenity(name=request_data['name'])
    storage.add(new_amenity)
    storage.save()

    return jsonify(new_amenity.to_dict()), 201

@app_views.route("/amenities/<amenity_id>", methods=['PUT'])
def update_amenity(amenity_id):
    """Update an existing amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)

    storage.save()
    return jsonify(amenity.to_dict()), 200

