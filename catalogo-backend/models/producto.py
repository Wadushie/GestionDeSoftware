from models.proveedor import ProveedorModel
from models.categoria import CategoriaModel
from flask_restful.reqparse import Namespace
from db import BaseModel, db

from utils import _assign_if_something

class ProductoModel(BaseModel):
    __tablename__ = 'producto'

    id = db.Column(db.BigInteger, primary_key = True)
    proveedor_id = db.Column(db.BigInteger, db.ForeignKey(ProveedorModel.id))
    categoria_id = db.Column(db.BigInteger, db.ForeignKey(CategoriaModel.id))
    nombre = db.Column(db.String)
    descripcion = db.Column(db.String)
    precio = db.Column(db.Float)
    estado = db.Column(db.String)

    _proveedor = db.relationship('ProveedorModel', uselist=False, foreign_keys=[proveedor_id])

    _categoria = db.relationship('CategoriaModel', uselist=False,
        primaryjoin='CategoriaModel.id == ProductoModel.categoria_id', foreign_keys='ProductoModel.categoria_id')

    def __init__(self, id=None, proveedor_id=None, categoria_id=None, nombre=None, descripcion=None, precio=None, estado=None):
        self.id = id
        self.proveedor_id = proveedor_id
        self.categoria_id = categoria_id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.estado = estado
    
    def json(self, jsondepth = 0):
        json = {
            'id': self.id,
            'proveedor_id': self.proveedor_id,
            'categoria_id': self.categoria_id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio': self.precio,
            'estado': self.estado
        }

        if jsondepth > 0:
            json['_proveedor'] = self._proveedor.json(jsondepth-1) if self._proveedor else None
            json['_categoria'] = self._categoria.json(jsondepth-1) if self._categoria else None

        return json