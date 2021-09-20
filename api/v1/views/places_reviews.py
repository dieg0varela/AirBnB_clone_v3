#!/usr/bin/python3
"""
Module related with City class
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route("/places/<place_id>/reviews", methods=['GET'],
                 strict_slashes=False)
def get_them_all_review(place_id):
    """Retrive all cities from a given state"""
    place_review = storage.get(Place, place_id)
    if place_review is None:
        abort(404)
    ret_list = []
    for place in place_review.reviews:
        ret_list.append(place.to_dict())
    return jsonify(ret_list)


@app_views.route("/reviews/<review_id>", methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """Retrive object city from their id"""
    obj_review = storage.get(Review, review_id)
    if obj_review is None:
        abort(404)
    return (jsonify(obj_review.to_dict()))


@app_views.route("/reviews/<review_id>>", methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Delete an instance of a city"""
    del_obj = storage.get(Review, review_id)
    if del_obj is not None:
        storage.delete(del_obj)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/places/<place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """Add an instance of a place"""
    if storage.get(Place, place_id) is None:
        abort(404)
    if request.is_json:
        data = request.get_json()
        if "text" not in data:
            abort(400, "Missing text")
        if "user_id" not in data:
            abort(400, "Missing user_id")
        if storage.get(User, data['user_id']) is None:
            abort(404)
        new_review = Review()
        setattr(new_review, "place_id", place_id)
        for k, v in data.items():
            setattr(new_review, k, v)
        new_review.save()
        return jsonify(new_review.to_dict()), 201
    else:
        abort(400, "Not a JSON")


@app_views.route("/reviews/<review_id>", methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """Update an instance of a city"""
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)
    update = request.get_json()
    if update is not None:
        for k, v in update.items():
            if k not in ["id", "user_id", "place_id",
                         "created_at", "updated_at"]:
                setattr(obj, k, v)
        storage.save()
        return jsonify(obj.to_dict())
    else:
        abort(400, "Not a JSON")
