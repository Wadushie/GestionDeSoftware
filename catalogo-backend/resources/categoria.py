from time import sleep
from flasgger import swag_from
from flask import request
from sqlalchemy import desc, func
from models.categoria import CategoriaModel
from flask_restful import Resource, reqparse

from utils import paginated_results, restrict

class Categoria(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type = int)
    parser.add_argument('descripcion', type = str)

    @swag_from('../swagger/categoria/get_categoria.yaml')
    def get(self, id):
        categoria:CategoriaModel = CategoriaModel.find_by_id(id=id)
        if categoria:
            return categoria.json(), 200
        
        return {'message': 'La categoria no ha sido encontrada'}, 404

    @swag_from('../swagger/categoria/put_categoria.yaml')
    def put(self, id):
        categoria:CategoriaModel = CategoriaModel.find_by_id(id=id)
        if categoria:
            newdata = Categoria.parser.parse_args()
            categoria.descripcion = newdata.get('descripcion', None)

            categoria.save_to_db()
            return categoria.json(), 200
        
        return {'message': 'La categoria no ha sido encontrada'}, 404


    @swag_from('../swagger/categoria/delete_categoria.yaml')
    def delete(self, id):
        categoria:CategoriaModel = CategoriaModel.find_by_id(id=id)
        if categoria:
            categoria.delete_from_db()
            return {'message': 'La categoria ha sido eliminada'}, 200
        
        return {'message': 'La categoria no ha sido encontrada'}, 404

class CategoriaList(Resource):
    @swag_from('../swagger/categoria/list_categoria.yaml')
    def get(self):
        categoria_model_list = CategoriaModel.query.order_by(desc(CategoriaModel.id)).all()
        if not categoria_model_list:
            return {'message': 'No se encuentran categorías'}, 404
        
        return_list = []
        for categoria_model in categoria_model_list:
            return_list.append(categoria_model.json())
        
        return return_list, 200
    
    @swag_from('../swagger/categoria/post_categoria.yaml')
    def post(self):
        data = Categoria.parser.parse_args()

        # Validacion
        id = data.get('id', None)
        if id:
            categoria:CategoriaModel = CategoriaModel.find_by_id(id=id)
            if categoria:
                return {'message': 'La categoria ya existe'}, 400
            
        categoria = CategoriaModel(**data)
        # categoria.descripcion = data.get('descripcion', None)
        
        try:
            # raise Exception("Sorry, no numbers below zero") 
            categoria.save_to_db()
        except Exception as error:
            return {'message': f'La categoria no fue creada debido a un error inesperado. Detalle: {error.__cause__}'}, 500

        return {'message': 'La categoria fue creada'}, 201
    
class CategoriaSearch(Resource):
    @swag_from('../swagger/categoria/search_categoria.yaml')
    def post(self):
        query = CategoriaModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters,'id', lambda x: CategoriaModel.id == x)
            query = restrict(query, filters,'descripcion', lambda x: func.lower(CategoriaModel.descripcion).contains(func.lower(x)))

        print(query)
        return paginated_results(query)
