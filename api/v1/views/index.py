#!/usr/bin/python3
"""
initialize the index package
"""


from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.amenity import Amenity


@app_views.route("/status")
def summary():
    """Status check to know if the api is working"""
    d = {"status": "OK"}
    return jsonify(d)


@app_views.route('/stats')
def number_of_obj():
    """Amount of objects of each class"""
    d = {"amenities": storage.count(Amenity),
         "cities":  storage.count(City),
         "places": storage.count(Place),
         "reviews": storage.count(Review),
         "states": storage.count(State),
         "users": storage.count(User)}
    return jsonify(d)
