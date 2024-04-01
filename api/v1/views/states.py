#!/usr/bin/python3
""" States module"""
from flask import abort, jsonify, make_response
from models import storage
from models.state import State
from . import app_views


@app_views.route('/states', strict_slashes=False)
def states():
    """returns all states"""
    states_list = storage.all(State)
    states_dicts = [v.to_dict() for k, v in states_list.items()]
    return jsonify(states_dicts)


@app_views.route('/states/<state_id>', strict_slashes=False)
def state_by_state_id(state_id=None):
    """returns state by state_id"""
    state = storage.get(State, state_id)
    if state is not None:
        return jsonify(state.to_dict())
    else:
        abort(404)
