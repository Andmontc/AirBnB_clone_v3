#!/usr/bin/python3
""" App module """

from os import environ
from flask import Flask
from models import storage
from api.v1.views import app_views
from flask import make_response, jsonify

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def storage_close(self):
    """ storage """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ Not Found Error """
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    hosts = environ.get('HBNB_API_HOST', '0.0.0.0')
    ports = environ.get('HBNB_API_PORT', 5000)
    app.run(host=hosts, port=ports, threaded=True, debug=True)
