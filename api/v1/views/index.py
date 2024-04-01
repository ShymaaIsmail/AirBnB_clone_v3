#!/usr/bin/python3
""" Index module"""
from flask import jsonify
from . import app_views


@app_views.route('/status', strict_slashes=False)
def status():
    """returns status"""
    return jsonify({"status": "ok"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """returns stats"""
    return None
