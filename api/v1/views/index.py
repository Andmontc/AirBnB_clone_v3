#!/usr/bin/python3
""" Route index module """
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def route_json():
    """ Return a Json """
    return jsonify({"status": "OK"})
