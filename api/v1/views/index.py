#!/usr/bin/python3
""" Index module"""
from flask import jsonify, make_response
from models import storage
from models.amenity import Amenity
from models.city import City
from models.review import Review
from models.state import State
from models.user import User
from models.place import Place
from . import app_views


@app_views.route('/status', strict_slashes=False)
def status():
    """returns status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """returns stats"""
    return jsonify(
        amenities=storage.count(Amenity),
        cities=storage.count(City),
        places=storage.count(Place),
        reviews=storage.count(Review),
        states=storage.count(State),
        users=storage.count(User),
    )

@app_views.route('/nop', strict_slashes=False)
def no():
    """returns not found"""
    response = jsonify(error="Not found")
    response.status_code = 404
    return response
