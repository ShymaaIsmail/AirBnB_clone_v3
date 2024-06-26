#!/usr/bin/python3
""" States module"""
from flask import abort, jsonify, request
from models import storage
from models.state import State
from . import app_views


@app_views.route('/states', strict_slashes=False)
def get_states():
    """returns all states"""
    states_list = storage.all(State)
    states_dicts = [v.to_dict() for k, v in states_list.items()]
    return jsonify(states_dicts)


@app_views.route('/states/<state_id>', strict_slashes=False)
def get_state(state_id=None):
    """returns state by state_id"""
    state = storage.get(State, state_id)
    if state is not None:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id=None):
    """returns state by state_id"""
    state = storage.get(State, state_id)
    if state is not None:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """post state to storage"""
    if request.is_json:
        request_body = request.get_json()
        if "name" in request_body:
            new_state = State(**request_body)
            storage.new(new_state)
            storage.save()
            return jsonify(new_state.to_dict()), 201
        else:
            abort(400, "Missing name")
    else:
        abort(400, "Not a JSON")


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def put_state(state_id=None):
    """put state to storage"""
    if request.is_json:
        request_body = request.get_json()
        existed_state = storage.get(State, state_id)
        if existed_state is not None:
            for key, value in request_body.items():
                if key not in ['id', 'created_at', 'updated_at', 'cities']:
                    setattr(existed_state, key, value)
            existed_state.save()
            return jsonify(existed_state.to_dict()), 200
        else:
            abort(404)
    else:
        abort(400, "Not a JSON")
