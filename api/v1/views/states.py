#!/usr/bin/python3
"""
create a variable app, instance of Flask
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
import json


@app_views.route("/states", methods=['GET'], strict_slashes=False)
def get_them_all_state():
    """Retrive all object state"""
    states = storage.all(State)
    ret_list = []
    for k, v in states.items():
        ret_list.append(v.to_dict())
    return jsonify(ret_list)


@app_views.route("/states/<state_id>", methods=['GET'])
def get_state(state_id):
    """Retrive object state from their id"""
    try:
        states = storage.get(State, state_id)
        return (jsonify(states.to_dict()))
    except:
        abort(404)


@app_views.route("/states/<state_id>", methods=['DELETE'])
def delete_state(state_id):
    """Delete an instance of a state"""
    del_obj = storage.get(State, state_id)
    if del_obj is not None:
        storage.delete(del_obj)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/states", methods=['POST'], strict_slashes=False)
def post_state():
    """Add an instance of a state"""
    try:
        data = request.get_json()
        if "name" not in data:
            abort(400, "Missing name")
        new_state = State()
        for k, v in data.items():
            setattr(new_state, k, v)
            new_state.save()
        return jsonify(new_state.to_dict()), 201
    except:
        abort(400, "Not a JSON")


@app_views.route("/states/<state_id>", methods=['PUT'])
def put_state(state_id):
    """put request"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    update = request.get_json()
    if update is not None:
        for k, v in update.items():
            if k not in ["id", "created_at", "update_at"]:
                setattr(obj, k, v)
                obj.save()
        return jsonify(obj.to_dict())

    abort(400, "Not a JSON")
