from flask import Flask, Response
from api.ressources import product, category, partner

app = Flask(__name__)
app.register_blueprint(product)
app.register_blueprint(category)
app.register_blueprint(partner)


@app.errorhandler(404)
def not_found(error):
    """Page not found."""
    return Response("Not found sorry", status=404)
