#!/usr/bin/python3
"""
create a variable app, instance of Flask
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
import json


@app_views.route("/states", methods=['GET'], strict_slashes = False)
def get_them_all():
    """Method Get PastranaRaymundo"""
    states = storage.all(State)
    ret_list = []
    for k, v in states.items():
        ret_list.append(v.to_dict())
    return jsonify(ret_list)


@app_views.route("/states/<state_id>", methods=['GET'])
def get(state_id):
    """Method Get PastranaRaymundo"""
    try:
        states = storage.get(State, state_id)
        return (jsonify(states.to_dict()))
    except:
        abort(404)


@app_views.route("/states/<state_id>", methods=['DELETE'])
def delete(state_id):
    """Delete an instance of a state"""
    del_obj = storage.get(State, state_id)
    if del_obj is not None:
        storage.delete(del_obj)
        return jsonify({})
    else:
        abort(404)


@app_views.route("/states", methods=['POST'], strict_slashes = False)
def post():
    """Add an instance of a state"""
    try:
        data = request.get_json()
        print(type(data))
        '''if "name" not in data
            abort(400, "Missing name")'''
        return jsonify({}, 201)
    
    except:
        abort(400, "Not a JSON")

@app_views.route("/states/<state_id>", methods=['PUT'])
def put(state_id):
    """put request"""
    obj = storage.get(State, state_id)
    if obj is None: abort(404)
    try:
        update = request.get_json()
        for k, v in update.items():
            if "id" not in update or "created_at" not in update or "updated_at" not in update:
                setattr(obj, k, v)
                obj.save()

    except ValueError as err:
        abort(400, "Not a JSON")

