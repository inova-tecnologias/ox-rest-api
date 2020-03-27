from flask_restplus import fields

from app import db
from .. import api
from ..models.users import User
from ..models.contexts import Context


user_model = User.resource_model
context_model = Context.resource_model

class Costumer(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(30))
    description = db.Column(db.String(200))
    users = db.relationship('User', backref='costumer', lazy=True)
    contexts = db.relationship('Context', backref='costumer', lazy=True)


    register_model = api.model('Register Costumer', {
    'name': fields.String(required=True),
    'description': fields.String()
    })
    
    resource_model = api.model('Costumer', {
    'id': fields.Integer(),
    'name': fields.String(),
    'description': fields.String(),
    'users': fields.Nested(user_model),
    'contexts': fields.Nested(context_model)
    }) 