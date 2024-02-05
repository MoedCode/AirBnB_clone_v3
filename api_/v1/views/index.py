#!/usr/bin/python3
"""status routs file"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('status', strict_slashes=False)
def home_statues():
    """Home Page Status """
    status = {"status": "OK"}
    return jsonify(status), 200


@app_views.route('stats', strict_slashes=False)
def home_api():
    """BNB routs"""
    data = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User),
    }
    return jsonify(data)
