#!/usr/bin/python3
"""Review object that handles all default RESTFul API actions"""

from api.v1.views import app_views
from models import storage
from models.place import Place
from models.user import User
from models.review import Review
from flask import abort, request, jsonify


@app_views.route("/places/<place_id>/reviews")
def get_reviews(place_id):
    """ return reviews"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])
