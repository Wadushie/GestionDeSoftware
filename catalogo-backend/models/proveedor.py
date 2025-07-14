from flask_restful.reqparse import Namespace
from db import BaseModel, db

from utils import _assign_if_something

class ProveedorModel(BaseModel):
    __tablename__ = 'proveedor'

    id = db.Column(db.BigInteger, primary_key = True)
    nombre = db.Column(db.String)
    direccion = db.Column(db.String)
    telefono = db.Column(db.String)

    def __init__(self, id=None, nombre=None, direccion=None, telefono=None):
        self.id = id
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
    
    def json(self, jsondepth = 0):
        json = {
            'id': self.id,
            'nombre': self.nombre,
            'direccion': self.direccion,
            'telefono': self.telefono
        }

        return json
