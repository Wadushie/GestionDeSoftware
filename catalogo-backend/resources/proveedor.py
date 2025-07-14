from flasgger import swag_from
from flask import request
from flask_restful import Resource, reqparse
from sqlalchemy import func
from models.proveedor import ProveedorModel

from utils import paginated_results, restrict


class Proveedor(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type = int)
    parser.add_argument('nombre', type = str)
    parser.add_argument('direccion', type = str)
    parser.add_argument('telefono', type = str)

    @swag_from('../swagger/proveedor/get_proveedor.yaml')
    def get(self, id):
        proveedor = ProveedorModel.find_by_id(id=id)

        if proveedor:
            return proveedor.json(), 200
        
        return {'message': 'El proveedor no se ha encontrado'}, 404


    @swag_from('../swagger/proveedor/put_proveedor.yaml')
    def put(self, id):
        proveedor:ProveedorModel = ProveedorModel.find_by_id(id=id)

        if proveedor:
            newdata = Proveedor.parser.parse_args()
            # proveedor.from_reqparse(newdata)
            proveedor.nombre = newdata.get('nombre', None)
            proveedor.direccion = newdata.get('direccion', None)
            proveedor.telefono = newdata.get('telefono', None)

            proveedor.save_to_db()
            return {'message': 'El proveedor ha sido modificado'}, 200
        
        return {'message': 'El proveedor no se ha encontrado'}, 404


    @swag_from('../swagger/proveedor/delete_proveedor.yaml')
    def delete(self, id):
        proveedor:ProveedorModel = ProveedorModel.find_by_id(id=id)
        if proveedor:
            proveedor.delete_from_db()
            return {'message': 'El proveedor ha sido eliminado'}, 200

        return {'message': 'El proveedor no se ha encontrado'}, 404

class ProveedorList(Resource):
    @swag_from('../swagger/proveedor/list_proveedor.yaml')
    def get(self):
        proveedor_model_list = ProveedorModel.query
        if not proveedor_model_list:
            return {'message': 'No se encuentran proveedores'}, 404
        
        return_list = []
        for proveedor_model in proveedor_model_list:
            return_list.append(proveedor_model.json())
        
        return return_list, 200
    
    @swag_from('../swagger/proveedor/post_proveedor.yaml')
    def post(self):
        data = Proveedor.parser.parse_args()

        # Validaciones
        id = data.get('id', None)
        if id:
            proveedor = ProveedorModel.find_by_id(id=id)
            if proveedor:
                return {'message': 'El proveedor ya existe'}, 400
        
        proveedor = ProveedorModel(**data)
        

        try:
            proveedor.save_to_db()
        except Exception as error:
             return {'message': f'Ocurrio un error al agregar el proveedor. Detalle: {error.__cause__}'}, 500

        return {'message': 'El proveedor ha sido agregado'}, 201
    
class ProveedorSearch(Resource):
    @swag_from('../swagger/proveedor/search_proveedor.yaml')
    def post(self):
        query = ProveedorModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters,'id', lambda x: ProveedorModel.id == x)
            query = restrict(query, filters,'nombre', lambda x: func.lower(ProveedorModel.nombre).contains(func.lower(x)))
            query = restrict(query, filters,'direccion', lambda x: func.lower(ProveedorModel.direccion).contains(func.lower(x)))
            query = restrict(query, filters,'telefono', lambda x: func.lower(ProveedorModel.telefono).contains(func.lower(x)))

        return paginated_results(query)