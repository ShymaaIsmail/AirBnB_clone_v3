#!/usr/bin/python3
""" Amenities module"""
from flask import abort, jsonify, request
from models import storage
from models.user import Amenity
from . import app_views


@app_views.route('/amenities', strict_slashes=False)
def get_amenities():
    """returns all amenities"""
    amenities_list = storage.all(Amenity)
    amenities_dicts = [v.to_dict() for k, v in amenities_list.items()]
    return jsonify(amenities_dicts)


@app_views.route('/amenities/<user_id>', strict_slashes=False)
def get_user(user_id=None):
    """returns user by user_id"""
    user = storage.get(Amenity, user_id)
    if user is not None:
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.route('/amenities/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id=None):
    """returns user by user_id"""
    user = storage.get(Amenity, user_id)
    if user is not None:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_user():
    """post user to storage"""
    if request.is_json:
        request_body = request.get_json()
        if "name" in request_body:
            new_user = Amenity(**request_body)
            storage.new(new_user)
            storage.save()
            return jsonify(new_user.to_dict()), 201
        else:
            abort(400, "Missing name")
    else:
        abort(400, "Not a JSON")


@app_views.route('/amenities/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id=None):
    """put user to storage"""
    if request.is_json:
        request_body = request.get_json()
        existed_user = storage.get(Amenity, user_id)
        if existed_user is not None:
            for key, value in request_body.items():
                if key not in ['id', 'created_at', 'updated_at']:
                    setattr(existed_user, key, value)
            existed_user.save()
            return jsonify(existed_user.to_dict()), 200
        else:
            abort(404)
    else:
        abort(400, "Not a JSON")
