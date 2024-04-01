#!/usr/bin/python3
""" Amenities module"""
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity
from . import app_views


@app_views.route('/amenities', strict_slashes=False)
def get_amenities():
    """returns all amenities"""
    amenities_list = storage.all(Amenity)
    amenities_dicts = [v.to_dict() for k, v in amenities_list.items()]
    return jsonify(amenities_dicts)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def get_amenity(amenity_id=None):
    """returns amenity by amenity_id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is not None:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id=None):
    """returns amenity by amenity_id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is not None:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """post amenity to storage"""
    if request.is_json:
        request_body = request.get_json()
        if (request_body["name"] is not None):
            new_amenity = Amenity(**request_body)
            storage.new(new_amenity)
            storage.save()
            return jsonify(new_amenity.to_dict()), 201
        else:
            abort(400, "Missing name")
    else:
        abort(400, "Not a JSON")


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id=None):
    """put amenity to storage"""
    if amenity_id is not None and request.is_json:
        request_body = request.get_json()
        existed_amenity = storage.get(Amenity, amenity_id)
        if existed_amenity is not None:
            for key, value in request_body.items():
                if key not in ['id', 'created_at', 'updated_at']:
                    setattr(existed_amenity, key, value)
            existed_amenity.save()
            return jsonify(existed_amenity.to_dict()), 201
        else:
            abort(404)
    else:
        abort(400, "Not a JSON")
