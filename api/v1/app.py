#!/usr/bin/python3
"""API Module v1"""
from os import getenv
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def teardown(Exception):
    """ tear down request"""
    storage.close()


@app_views.route('/nop', strict_slashes=False)
def no():
    """returns not found"""
    response = jsonify(error="Not found")
    response.status_code = 404
    return response


if __name__ == '__main__':
    app.run(host=getenv("HBNB_API_HOST", '0.0.0.0'),
            port=int(getenv("HBNB_API_PORT", "5000")), threaded=True)
