#!/usr/bin/python3
""" App module """

from os import environ
from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def storage_close(self):
    """ storage """
    storage.close()


if __name__ == "__main__":
    hosts = environ.get('HBNB_API_HOST', '0.0.0.0')
    ports = environ.get('HBNB_API_PORT', 5000)
    app.run(host=hosts, port=ports, threaded=True, debug=True)
