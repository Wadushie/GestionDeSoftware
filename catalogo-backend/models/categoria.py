from flask_restful.reqparse import Namespace
from db import BaseModel, db

from utils import _assign_if_something

class CategoriaModel(BaseModel):
    __tablename__ = 'categoria'

    id = db.Column(db.BigInteger, primary_key = True)
    descripcion = db.Column(db.String)

    def __init__(self, id=None, descripcion=None):
        self.id = id
        self.descripcion = descripcion
    
    def json(self, jsondepth = 0):
        json = {
            'id': self.id,
            'descripcion': self.descripcion
        }

        return json
    