#!/usr/bin/python3
""" Review module """
from models import storage
from api.v1.views import app_views, State, City, Place, User, Review
from flask import jsonify, request, abort, make_response


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_review_by_place(place_id=None):
    """ Return all places in a city """
    place = storage.get(Place, place_id)
    if place:
        return jsonify([v.to_dict() for v in place.reviews]), 200
    return abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review_by_id(review_id=None):
    """ Return a review by id """
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    return abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_review_by_id(review_id=None):
    """ Delete a review by id """
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return make_response(jsonify({}), 200)
    return abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id=None):
    """ Post a review in a place with an id """
    body = request.get_json(silent=True)
    if not body:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in body:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    if 'text' not in body:
        return make_response(jsonify({'error': 'Missing text'}), 400)
    place = storage.get(Place, place_id)
    user = storage.get(User, body['user_id'])
    if place and user:
        new_review = Review(**body)
        new_review.place_id = place.id
        storage.new(new_review)
        storage.save()
        return make_response(jsonify(new_review.to_dict()), 201)
    return abort(404)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_review_in_review_by_id(review_id=None):
    """ Put update review in a review by id """
    body = request.get_json(silent=True)
    if not body:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    review = storage.get(Review, review_id)
    if review:
        for k, v in body.items():
            if k != 'id' and k != 'created_at' and k != 'updated_at'\
             and k != 'user_id' and k != 'city_id':
                setattr(review, k, v)
        storage.save()
        return make_response(jsonify(review.to_dict()), 200)
    else:
        abort(404)
