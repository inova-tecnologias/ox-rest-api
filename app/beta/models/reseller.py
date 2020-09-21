from flask_restplus import fields

from app import db
from .. import api
from ..models.users import User
from ..models.customer import customer


user_model = User.resource_model
customer_model = Customer.resource_model

class Reseller(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(256))
    cnpj = db.Column(db.String(20))
    users = db.relationship('User', backref='reseller', lazy=True)
    customer = db.relationship('Customer', backref='reseller', lazy=True)


    register_model = api.model('Register Reseller', {
    'name': fields.String(required=True),
    'cnpj': fields.String(required=True),
    'description': fields.String()
    })
    
    resource_model = api.model('Reseller', {
    'id': fields.Integer(),
    'name': fields.String(),
    'cnpj': fields.String(),
    'description': fields.String(),
    'users': fields.Nested(user_model),
    'reseller': fields.Nested(context_model)
    }) 