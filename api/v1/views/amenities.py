#!/usr/bin/python3
""" State module """
from models import storage
from api.v1.views import app_views, State, Amenity
from flask import jsonify, request, abort, make_response


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """ Return all amenities """
    return jsonify([v.to_dict() for v in storage.all(Amenity).values()])


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity_by_id(amenity_id=None):
    """ Return an amenity by id """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    return abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_amenity_by_id(amenity_id=None):
    """ Delete an amenity by id """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return make_response(jsonify({}), 200)
    return abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """ Put an amenity """
    body = request.get_json(silent=True)
    if not body:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in body:
        return make_response(jsonify({'error': 'Missing name'}), 400)

    new_amenity = Amenity(**body)
    storage.new(new_amenity)
    storage.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def put_amenity_by_id(amenity_id=None):
    """ Put update amenity by id """
    body = request.get_json(silent=True)
    if not body:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        for k, v in body.items():
            if k != 'id' and k != 'created_at' and k != 'updated_at':
                setattr(amenity, k, v)
        storage.save()
        return make_response(jsonify(amenity.to_dict()), 200)
    else:
        abort(404)
