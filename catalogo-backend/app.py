import logging
import os

from flask_cors import CORS

from resources.producto import Producto, ProductoList, ProductoSearch
from resources.proveedor import Proveedor, ProveedorList, ProveedorSearch
from resources.categoria import Categoria, CategoriaList, CategoriaSearch

from flask import Flask, redirect
from flask_restful import Api
from flasgger import Swagger
from db import db

app = Flask(__name__)
CORS(app, support_credentials=True)

api = Api(app, errors={
    'NoAuthorizationError': {
        "message": "La respuesta no tiene token",
        "error": "authorization_required",
        "status": 401
    }
})

PREFIX = os.environ.get('PREFIX_PATH','/api')

# Swagger config
app.config['SWAGGER'] = {
    'title': 'catalogo-backend',
    'version': '1.0.0',
    'description': 'API de servicios REST en Flask',
    'uiversion': 2,
    'tags': [{'name': 'jwt'}],
    'specs': [{
        'endpoint': 'apispec_1',
        'route': f'{PREFIX}/apispec_1.json',
        'rule_filter': lambda rule: True,  # all in
        'model_filter': lambda tag: True  # all in
    }],
    'specs_route': f"{PREFIX}/apidocs/",
    'static_url_path': f'{PREFIX}/static'
}

swagger = Swagger(app)

app.logger.setLevel(logging.INFO)

def env_config(name, default):
    app.config[name] = os.environ.get(name, default = default)

# Database config
env_config('SQLALCHEMY_DATABASE_URI', 'postgresql://postgres:postgres@localhost:5432/catalogo')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SQLALCHEMY_ECHO'] = False

@app.route("/")
@app.route(f'{PREFIX}')
def index():
    return redirect(f"{PREFIX}/apidocs", code= 302)

# Routes
api.add_resource(Producto, f'{PREFIX}/productos/<id>')
api.add_resource(ProductoList, f'{PREFIX}/productos')
api.add_resource(ProductoSearch, f'{PREFIX}/search/productos')

api.add_resource(Categoria, f'{PREFIX}/categorias/<id>')
api.add_resource(CategoriaList, f'{PREFIX}/categorias')
api.add_resource(CategoriaSearch, f'{PREFIX}/search/categorias')

api.add_resource(Proveedor, f'{PREFIX}/proveedores/<id>')
api.add_resource(ProveedorList, f'{PREFIX}/proveedores')
api.add_resource(ProveedorSearch, f'{PREFIX}/search/proveedores')


if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)
else: 
    db.init_app(app)
