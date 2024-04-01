#!/usr/bin/python3
"""Places Reviews Module"""

from flask import abort, jsonify, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from . import app_views


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_all_reviews(place_id):
    """Retrieve all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    reviews = place.reviews
    reviews_list = [review.to_dict() for review in reviews]
    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieve a specific Review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Delete a specific Review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Create a new Review"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if not request.is_json:
        abort(400, "Not a JSON")

    data = request.get_json()
    if "user_id" not in data:
        abort(400, "Missing user_id")
    if "text" not in data:
        abort(400, "Missing text")

    user_id = data.get("user_id")
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    data['place_id'] = place_id
    new_review = Review(**data)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Update a specific Review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    if not request.is_json:
        abort(400, "Not a JSON")

    data = request.get_json()
    for key in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
        data.pop(key, None)

    for key, value in data.items():
        setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
