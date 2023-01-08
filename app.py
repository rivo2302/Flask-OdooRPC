from flask import Flask, Response, request, jsonify
from api.ressources import product, category, partner, sale
from os import environ as env

app = Flask(__name__)

# Register the blueprints
app.register_blueprint(product)
app.register_blueprint(category)
app.register_blueprint(partner)
app.register_blueprint(sale)


# Error handler
@app.errorhandler(404)
def not_found(error):
    """Page not found."""
    return Response("Marketbot Error : Page not found", status=404)


# Check token befor any request , the token is set in the .env file
@app.before_request
def header_required():
    if "access-token" not in request.headers:
        return jsonify({"error": "A valid access-token is missing"}), 403
    token = request.headers["access-token"]
    if token != env.get("TOKEN"):
        return jsonify({"error": "Invalid access-token"}), 403
