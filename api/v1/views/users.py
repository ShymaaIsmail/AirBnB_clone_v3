#!/usr/bin/python3
"""
    Flask route that returns json response
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.user import User


method = ['PUT', 'GET', 'POST', 'DELETE']


@app_views.route('/users/', strict_slashes=False, methods=method)
def user_api():
    """ just a discription"""
    if request.method == 'GET':
        user = storage.all('User')
        user_to_list = []
        for key, value in user.items():
            user_to_list.append(value.to_dict())
        return jsonify(user_to_list)

    if request.method == 'POST':
        data_json = request.get_json(force=True, silent=True)
        if not data_json:
            abort(400, "Not a JSON")
        if "email" not in data_json:
            abort(400, "Missing email")
        if "password" not in data_json:
            abort(400, "Missing password")
        user = User(**data_json)
        user.save()
        return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=method)
def user_by_id(user_id):
    """ just a discription"""
    user = storage.get('User', user_id)
    if not user:
        abort(404)

    if request.method == 'GET':
        return jsonify(user.to_dict())

    elif request.method == 'DELETE':
        # Delete a state
        storage.delete(user)
        storage.save()
        return jsonify({}), 200

    elif request.method == 'PUT':
        json_data = request.get_json(force=True, silent=True)
        if not json_data:
            abort(400, "Not a JSON")
        for key, value in json_data.items():
            if key == 'id' or key == 'created_at'\
                    or key == 'updated_at':
                continue
            else:
                setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict()), 200
