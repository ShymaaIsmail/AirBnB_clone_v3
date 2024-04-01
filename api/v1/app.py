#!/usr/bin/python3
"""API Module v1"""
from os import getenv
from flask import Flask, jsonify
from flask_cors import CORS
from api.v1.views import app_views
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')

# Allow CORS for all routes (/*) from 0.0.0.0
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(Exception):
    """ tear down request"""
    storage.close()


@app.route('/nop')
def nop():
    """nop request"""
    pass


@app.errorhandler(404)
def not_found(error):
    """not found handler"""
    return jsonify(error="Not found"), 404


if __name__ == '__main__':
    app.run(host=getenv("HBNB_API_HOST", '0.0.0.0'),
            port=int(getenv("HBNB_API_PORT", "5000")), threaded=True)
