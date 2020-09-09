#!/usr/bin/python3
""" State module """
from models import storage
from api.v1.views import app_views, State
from flask import jsonify, request, abort, make_response


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """ Return all States """
    return jsonify([v.to_dict() for v in storage.all(State).values()])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_by_id(state_id=None):
    """ Return a state by id """
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    return abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_state_by_id(state_id=None):
    """ Delete a state by id """
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return make_response(jsonify({}), 200)
    return abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """ Put a state """
    body = request.get_json(silent=True)
    if not body:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in body:
        return make_response(jsonify({'error': 'Missing name'}), 400)

    new_state = State(**body)
    storage.new(new_state)
    storage.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state_by_id(state_id=None):
    """ Put update state by id """
    body = request.get_json(silent=True)
    if not body:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    state = storage.get(State, state_id)
    if state:
        for k, v in body.items():
            if k != 'id' and k != 'created_at' and k != 'updated_at':
                setattr(state, k, v)
        storage.save()
        return make_response(jsonify(state.to_dict()), 200)
    else:
        abort(404)
