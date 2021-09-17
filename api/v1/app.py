#!/usr/bin/python3
"""
create a variable app, instance of Flask
"""

from flask import Blueprint, render_template, abort, Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)

app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def invalid_route(e):
    """handle 404 error"""
    return jsonify({'error': 'Not found'}), 404


if __name__ == '__main__':

    if getenv('HBNB_API_HOST') is not None:
        HBNB_API_HOST = getenv('HBNB_API_HOST')
    else:
        HBNB_API_HOST = '0.0.0.0'

    if getenv('HBNB_API_PORT') is not None:
        HBNB_API_PORT = getenv('HBNB_API_PORT')
    else:
        HBNB_API_PORT = '5000'

    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
