#!/usr/bin/python3
"""
Module related with City class
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route("/cities/<city_id>/places", methods=['GET'],
                 strict_slashes=False)
def get_them_all_place(city_id):
    """Retrive all cities from a given state"""
    place_city = storage.get(City, city_id)
    if place_city is None:
        abort(404)
    ret_list = []
    for place in place_city.places:
        ret_list.append(place.to_dict())
    return jsonify(ret_list)


@app_views.route("/places/<place_id>", methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """Retrive object city from their id"""
    obj_place = storage.get(Place, place_id)
    if obj_place is None:
        abort(404)
    return (jsonify(obj_place.to_dict()))


@app_views.route("/places/<place_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Delete an instance of a city"""
    del_obj = storage.get(Place, place_id)
    if del_obj is not None:
        storage.delete(del_obj)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/cities/<city_id>/places", methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """Add an instance of a place"""
    if storage.get(City, city_id) is None:
        abort(404)
    if request.is_json:
        data = request.get_json()
        if "name" not in data:
            abort(400, "Missing name")
        if "user_id" not in data:
            abort(400, "Missing user_id")
        if storage.get(User, data['user_id']) is None:
            abort(404)
        new_place = Plcae()
        for k, v in data.items():
            setattr(new_place, k, v)
        new_place.save()
        return jsonify(new_place.to_dict()), 201
    else:
        abort(400, "Not a JSON")


@app_views.route("/places/<place_id>", methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """Update an instance of a city"""
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    update = request.get_json()
    if update is not None:
        for k, v in update.items():
            if k not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
                setattr(obj, k, v)
        storage.save()
        return jsonify(obj.to_dict())
    else:
        abort(400, "Not a JSON")
