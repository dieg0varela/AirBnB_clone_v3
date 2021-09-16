from api.v1.views import app_views
from flask import jsonify

@app.route("/status")
def summary():
    d = {"status": "OK"}
    return jsonify(d)
