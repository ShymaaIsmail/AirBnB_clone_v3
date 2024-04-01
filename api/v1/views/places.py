#!/usr/bin/python3
"""Cities Module"""

# api/v1/views/places.py

from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from . import app_views


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_all_places(city_id):
    """Retrieve all Place objects of a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    places = city.places
    places_list = [place.to_dict() for place in places]
    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieve a specific Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Delete a specific Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Create a new Place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if not request.is_json:
        abort(400, "Not a JSON")

    data = request.get_json()
    if "user_id" not in data:
        abort(400, "Missing user_id")
    if "name" not in data:
        abort(400, "Missing name")

    user_id = data.get("user_id")
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    data['city_id'] = city_id
    new_place = Place(**data)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Update a specific Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if not request.is_json:
        abort(400, "Not a JSON")

    data = request.get_json()
    for key in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
        data.pop(key, None)

    for key, value in data.items():
        setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
