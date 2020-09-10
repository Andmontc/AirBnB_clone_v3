#!/usr/bin/python3
""" State module """
from models import storage
from api.v1.views import app_views, State, City, Place, User
from flask import jsonify, request, abort, make_response


@app_views.route('cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_by_city(city_id=None):
    """ Return all places in a city """
    city = storage.get(City, city_id)
    if city:
        return jsonify([v.to_dict() for v in city.places]), 200
    return abort(404)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place_by_id(place_id=None):
    """ Return a place by id """
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    return abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_place_by_id(place_id=None):
    """ Delete a place by id """
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return make_response(jsonify({}), 200)
    return abort(404)


@app_views.route('cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id=None):
    """ Post a place in a city with an id """
    body = request.get_json(silent=True)
    if not body:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in body:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    if 'name' not in body:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    city = storage.get(City, city_id)
    user = storage.get(User, body['user_id'])
    if city and user:
        new_place = Place(**body)
        new_place.city_id = city.id
        storage.new(new_place)
        storage.save()
        return make_response(jsonify(new_place.to_dict()), 201)
    return abort(404)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place_in_place_by_id(place_id=None):
    """ Put update place in a place by id """
    body = request.get_json(silent=True)
    if not body:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    place = storage.get(Place, place_id)
    if place:
        for k, v in body.items():
            if k != 'id' and k != 'created_at' and k != 'updated_at'\
             and k != 'user_id' and k != 'city_id':
                setattr(place, k, v)
        storage.save()
        return make_response(jsonify(place.to_dict()), 200)
    else:
        abort(404)
