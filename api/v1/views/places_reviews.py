#!/usr/bin/python3
"""comment for file"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('places/<string:place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def ReviewByPlaces(place_id):
    """get review by place id"""
    reviews = storage.all('Review')
    ll = []
    for val in reviews.values():
        if val.place_id == place_id:
            ll.append(val.to_dict())
    if len(ll) <= 0:
        abort(404)
    return jsonify(ll), 200


@app_views.route('reviews/<string:review_id>', methods=['GET'],
                 strict_slashes=False)
def ReviewById(review_id):
    """get review by id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict()), 200


@app_views.route('reviews/<string:review_id>', methods=['DELETE'],
                 strict_slashes=False)
def DeleteReviewById(review_id):
    """delete review by id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('places/<string:place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def POSTReviewById(place_id):
    """delete review by id"""
    response = request.get_json()
    if not response:
        abort(400, {'error': 'Not a JSON'})
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not response.get('user_id'):
        abort(400, {'error': 'Missing user_id'})
    if not response.get('text'):
        abort(400, {'error': 'Missing text'})
    if not storage.get(User, response.get('user_id')):
        abort(404)
    stateObject = Review(**response)
    setattr(stateObject, 'place_id', place_id)
    storage.new(stateObject)
    storage.save()
    return jsonify(stateObject.to_dict()), '201'


@app_views.route('reviews/<string:review_id>', methods=['PUT'],
                 strict_slashes=False)
def PUTReviewById(review_id):
    """delete review by id"""
    response = request.get_json()
    if not response:
        abort(400, {'error': 'Not a JSON'})
    stateObject = storage.get(Review, review_id)
    if stateObject is None:
        abort(404)
    ignoreKeys = ['id', 'created_at', 'updated_at', 'place_id', 'user_id']
    for key, val in response.items():
        if key not in ignoreKeys:
            setattr(stateObject, key, val)
    storage.save()
    return jsonify(stateObject.to_dict()), '200'
