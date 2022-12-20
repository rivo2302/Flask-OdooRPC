from flask import Flask, Response
from flasgger import Swagger
from api.ressources import product, category, partner, sale, account
from docs import template

app = Flask(__name__)

app.register_blueprint(product)
app.register_blueprint(category)
app.register_blueprint(partner)
app.register_blueprint(sale)
app.register_blueprint(account)


# Instalce swagger
swagger = Swagger(app, template=template)

# Error handler
@app.errorhandler(404)
def not_found(error):
    """Page not found."""
    return Response("Not found sorry", status=404)
