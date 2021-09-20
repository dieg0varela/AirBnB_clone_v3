#!/usr/bin/python3
"""
Module related with City class
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City
import json


@app_views.route("states/<state_id>/cities", methods=['GET'])
def get_them_all_city(state_id):
    """Retrive all cities from a given state"""
    city_state = storage.get(State, state_id)
    if city_state is None:
        abort(404)
    ret_list = []
    for city in city_state.cities:
        ret_list.append(city.to_dict())
    return jsonify(ret_list)


@app_views.route("/cities/<city_id>", methods=['GET'])
def get_city(city_id):
    """Retrive object city from their id"""
    obj_city = storage.get(City, city_id)
    if obj_city is None:
        abort(404)
    return (jsonify(obj_city.to_dict()))



@app_views.route("/cities/<city_id>", methods=['DELETE'])
def delete_city(city_id):
    """Delete an instance of a city"""
    del_obj = storage.get(City, city_id)
    if del_obj is not None:
        storage.delete(del_obj)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/states/<state_id>/cities", methods=['POST'])
def post_city(state_id):
    """Add an instance of a city"""
    if storage.get(State, state_id) is None:
        abort(404)
    if request.is_json:
        data = request.get_json()
        if "name" not in data:
            abort(400, "Missing name")
        new_city = City()
        setattr(new_city, "state_id", state_id)
        for k, v in data.items():
            setattr(new_city, k, v)
        new_city.save()
        return jsonify(new_city.to_dict()), 201
    else:
        abort(400, "Not a JSON")


@app_views.route("/cities/<city_id>", methods=['PUT'])
def put_city(city_id):
    """Update an instance of a city"""
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
        update = request.get_json()
    if update is not None:
        for k, v in update.items():
            if k not in ["id", "state_id", "created_at", "updated_at"]:
                setattr(obj, k, v)
        storage.save()
        return jsonify(obj.to_dict())
    else:
        abort(400, "Not a JSON")
