#!/usr/bin/python3
"""
create a variable app, instance of Flask
"""

from flask import Blueprint, render_template, abort, Flask
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
if getenv('HBNB_API_HOST') is not None:
    HBNB_API_HOST = getenv('HBNB_API_HOST')
else:
    HBNB_API_HOST = '0.0.0.0'
if getenv('HBNB_API_PORT') is not None:
    HBNB_API_PORT = getenv('HBNB_API_PORT')
else:
    HBNB_API_PORT = '5000'

app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()

if __name__ == '__main__':
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)