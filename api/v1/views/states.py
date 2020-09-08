#!/usr/bin/python3
""" State module """
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models.state import State
from models import storage


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
