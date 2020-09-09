#!/usr/bin/python3
""" State module """
from models import storage
from api.v1.views import app_views, User
from flask import jsonify, request, abort, make_response


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """ Return all Users """
    return jsonify([v.to_dict() for v in storage.all(User).values()])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_by_id(user_id=None):
    """ Return a user by id """
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    return abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_user_by_id(user_id=None):
    """ Delete a user by id """
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return make_response(jsonify({}), 200)
    return abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """ Put a user """
    body = request.get_json(silent=True)
    if not body:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'email' not in body:
        return make_response(jsonify({'error': 'Missing email'}), 400)
    elif 'password' not in body:
        return make_response(jsonify({'error': 'Missing password'}), 400)

    new_user = User(**body)
    storage.new(new_user)
    storage.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user_by_id(user_id=None):
    """ Put update user by id """
    body = request.get_json(silent=True)
    if not body:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    user = storage.get(User, user_id)
    if user:
        for k, v in body.items():
            if k != 'id' and k != 'created_at' and k != 'updated_at'\
                 and k != 'email':
                setattr(user, k, v)
        storage.save()
        return make_response(jsonify(user.to_dict()), 200)
    else:
        abort(404)
