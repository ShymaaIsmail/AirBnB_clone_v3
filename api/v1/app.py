#!/usr/bin/python3
"""API Module v1"""
from os import getenv
from flask import Flask
from api.v1.views import app_views
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def teardown(Exception):
    storage.close()


if __name__ == '__main__':
    app.run(host=getenv("HBNB_API_HOST", '0.0.0.0'),
            port=int(getenv("HBNB_API_PORT", "5000")), threaded=True)
