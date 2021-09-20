#!/usr/bin/python3
"""
Module related with User class
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route("/users", methods=['GET'],
                 strict_slashes=False)
def get_them_all_user():
    """Retrive all Users"""
    users = storage.all(User)
    ret_list = []
    for k, v in users.items():
        ret_list.append(v.to_dict())
    return jsonify(ret_list)


@app_views.route("/users/<user_id>", methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """Retrive object User from their id"""
    obj_user = storage.get(User, user_id)
    if obj_user is None:
        abort(404)
    return (jsonify(obj_user.to_dict()))


@app_views.route("/users/<user_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Delete an instance of a User"""
    del_obj = storage.get(User, user_id)
    if del_obj is not None:
        storage.delete(del_obj)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/users", methods=['POST'],
                 strict_slashes=False)
def post_user():
    """Add an instance of a User"""
    if request.is_json:
        data = request.get_json()
        if "email" not in data:
            abort(400, "Missing email")
        if "password" not in data:
            abort(400, "Missing password")
        new_user = User()
        for k, v in data.items():
            setattr(new_user, k, v)
        new_user.save()
        return jsonify(new_user.to_dict()), 201
    else:
        abort(400, "Not a JSON")


@app_views.route("/users/<user_id>", methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id):
    """Update an instance of a User"""
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    update = request.get_json()
    if update is not None:
        for k, v in update.items():
            if k not in ["id", "email", "created_at", "updated_at"]:
                setattr(obj, k, v)
        storage.save()
        return jsonify(obj.to_dict())
    else:
        abort(400, "Not a JSON")
