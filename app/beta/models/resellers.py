from flask_restplus import fields

from app import db
from .. import api
from ..models.users import User
from ..models.customers import Customer
from datetime import datetime


user_model = User.resource_model
customer_model = Customer.resource_model

class Reseller(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    changed = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
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
    'customers': fields.Nested(customer_model),
    }) 