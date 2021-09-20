#!/usr/bin/python3
"""
create a variable app, instance of Flask
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
import json


@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
def get_them_all_Amenity():
    """Retrive all object Amenity"""
    amenities = storage.all(Amenity)
    ret_list = []
    for k, v in amenities.items():
        ret_list.append(v.to_dict())
    return jsonify(ret_list)


@app_views.route("/amenities/<amenity_id>", methods=['GET'],
                 strict_slashes=False)
def get_Amenity(amenity_id):
    """Retrive object Amenity from their id"""
    try:
        amenities = storage.get(Amenity, amenity_id)
        return (jsonify(amenities.to_dict()))
    except:
        abort(404)


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'], strict_slashes=False)
def delete_Amenity(amenity_id):
    """Delete an instance of a Amenity"""
    del_obj = storage.get(Amenity, amenity_id)
    if del_obj is not None:
        storage.delete(del_obj)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/amenities", methods=['POST'], strict_slashes=False)
def post_amenity():
    """Add an instance of a Amenity"""
    try:
        data = request.get_json()
        if "name" not in data:
            abort(400, "Missing name")
        new_Amenity = Amenity()
        for k, v in data.items():
            setattr(new_Amenity, k, v)
            new_Amenity.save()
        return jsonify(new_Amenity.to_dict()), 201
    except:
        abort(400, "Not a JSON")


@app_views.route("/amenities/<amenity_id>", methods=['PUT'],
                 strict_slashes=False)
def put_Amenity(amenity_id):
    """put request"""
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    update = request.get_json()
    if update is not None:
        for k, v in update.items():
            if k not in ["id", "created_at", "updated_at"]:
                setattr(obj, k, v)
                obj.save()
        return jsonify(obj.to_dict())

    abort(400, "Not a JSON")
