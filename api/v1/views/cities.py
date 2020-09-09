#!/usr/bin/python3
""" Cities module """
from models import storage
from api.v1.views import app_views, State, City
from flask import jsonify, request, abort, make_response


@app_views.route('states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities_by_states(state_id=None):
    """ Return all cities in a state """
    state = storage.get(State, state_id)
    if state:
        return jsonify([v.to_dict() for v in state.cities]), 200
    return abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city_by_id(city_id=None):
    """ Return a city by id """
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    return abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_city_by_id(city_id=None):
    """ Delete a city by id """
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return make_response(jsonify({}), 200)
    return abort(404)


@app_views.route('states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id=None):
    """ Post a city in a state with an id """
    body = request.get_json(silent=True)
    if not body:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in body:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    state = storage.get(State, state_id)
    if state:
        new_city = City(**body)
        new_city.state_id = state.id
        storage.new(new_city)
        storage.save()
        return make_response(jsonify(new_city.to_dict()), 201)
    return abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city_in_state_by_id(city_id=None):
    """ Put update city in a state by id """
    body = request.get_json(silent=True)
    if not body:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    cities = storage.get(City, city_id)
    if cities:
        for k, v in body.items():
            if k != 'id' and k != 'created_at' and k != 'updated_at':
                setattr(cities, k, v)
        storage.save()
        return make_response(jsonify(cities.to_dict()), 200)
    else:
        abort(404)
