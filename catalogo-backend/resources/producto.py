import logging
from flasgger import swag_from
from flask import request
from sqlalchemy import func
from models.producto import ProductoModel
from flask_restful import Resource, reqparse

from utils import paginated_results, restrict

class Producto(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type = int)
    parser.add_argument('proveedor_id', type = int)
    parser.add_argument('categoria_id', type = int)
    parser.add_argument('nombre', type = str)
    parser.add_argument('descripcion', type = str)
    parser.add_argument('precio', type = float)
    parser.add_argument('estado', type = str)

    @swag_from('../swagger/producto/get_producto.yaml')
    def get(self, id):
        producto = ProductoModel.find_by_id(id)
        if producto:
            return producto.json()

        return {'message': 'No se encuentra el producto'}, 404

    @swag_from('../swagger/producto/put_producto.yaml')
    def put(self, id):
        producto = ProductoModel.find_by_id(id)
        if producto:
            newdata = Producto.parser.parse_args()
            Producto.from_reqparse(producto, newdata)
            producto.save_to_db()
            return producto.json()

        return {'message': 'No se encuentra el producto'}, 404
    
    @swag_from('../swagger/producto/delete_producto.yaml')
    def delete(self, id):
        task = ProductoModel.find_by_id(id)
        if task:
            task.delete_from_db()

        return {'message': 'Se ha borrado el producto'}
        
class ProductoList(Resource):
    @swag_from('../swagger/producto/list_producto.yaml')
    def get(self):
        producto_model_list = ProductoModel.query
        if not producto_model_list:
            return {'message': 'No se encuentran producto'}, 404
        
        return_list = []
        for producto_model in producto_model_list:
            return_list.append(producto_model.json())
        
        return return_list, 200

    @swag_from('../swagger/producto/post_producto.yaml')
    def post(self):
        data = Producto.parser.parse_args()

        id = data.get('id')

        if id is not None and ProductoModel.find_by_id(id):
            return {'message': "Ya existe un producto con el id"}, 400
        
        task = ProductoModel(**data)
        try:
            task.save_to_db()
        except Exception as e:
            logging.error('Ocurrio un error al crear el producto.', exc_info=e)
            return {'message': "Ocurrio un error al crear el producto"}, 500
        return task.json(), 201

class ProductoSearch(Resource):
    @swag_from('../swagger/producto/search_producto.yaml')
    def post(self):
        query = ProductoModel.query
        if request.json:
            filters = request.json
            query = restrict (query, filters,'id', lambda x: ProductoModel.id == x)
            query = restrict (query, filters,'proveedor_id', lambda x: ProductoModel.proveedor_id == x)
            query = restrict (query, filters,'categoria_id', lambda x: ProductoModel.categoria_id == x)
            query = restrict (query, filters,'nombre', lambda x: func.lower(ProductoModel.nombre).contains(func.lower(x)))
            query = restrict (query, filters,'descripcion', lambda x: func.lower(ProductoModel.descripcion).contains(func.lower(x)))
            query = restrict (query, filters,'precio', lambda x: ProductoModel.precio == x)
            query = restrict (query, filters,'estado', lambda x: func.lower(ProductoModel.estado).contains(func.lower(x)))

        return paginated_results(query)