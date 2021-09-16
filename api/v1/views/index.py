from api.v1.views import app_views
from flask import jsonify

@app_views.route("/status")
def summary():
    d = {"status": "OK"}
    return jsonify(d)
