#!/usr/bin/python3
""" Users module"""
from flask import abort, jsonify, request
from models import storage
from models.user import User
from . import app_views


@app_views.route('/users', strict_slashes=False)
def get_all_users():
    """returns all users"""
    users_list = storage.all(User)
    users_dicts = [v.to_dict() for k, v in users_list.items()]
    return jsonify(users_dicts)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id=None):
    """returns user by user_id"""
    user = storage.get(User, user_id)
    if user is not None:
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id=None):
    """returns user by user_id"""
    user = storage.get(User, user_id)
    if user is not None:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """post user to storage"""
    if not request.is_json:
        abort(400, "Not a JSON")
    request_body = request.get_json()
    if "email" not in request_body:
        abort(400, "Missing email")
    if "password" not in request_body:
        abort(400, "Missing password")
    new_user = User(**request_body)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id=None):
    """put user to storage"""
    if not request.is_json:
        abort(400, "Not a JSON")
    request_body = request.get_json()
    existed_user = storage.get(User, user_id)
    if existed_user is not None:
        for key, value in request_body.items():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(existed_user, key, value)
        existed_user.save()
        return jsonify(existed_user.to_dict()), 200
    else:
        abort(404)
