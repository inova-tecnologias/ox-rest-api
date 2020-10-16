from flask_restplus import fields

from app import db
from .. import api
from ..models.users import User
from datetime import datetime


user_model = User.resource_model

class Customer(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    changed = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    description = db.Column(db.String(256))
    cnpj = db.Column(db.String(20))
    users = db.relationship('User', backref='customer', lazy=True)
    contexts = db.relationship('Context', backref='customer', lazy=True)

    reseller_id = db.Column(db.Integer, db.ForeignKey('reseller.id'))    

    register_model = api.model('Register Customer', {
    'name': fields.String(required=True),
    'cnpj': fields.String(required=True),
    'reseller_id': fields.Integer(),
    'description': fields.String()
    })
    
    resource_model = api.model('Customer', {
    'id': fields.Integer(),
    'name': fields.String(),
    'cnpj': fields.String(),
    'description': fields.String(),
    'reseller_id': fields.Integer(),
    'users': fields.Nested(user_model),
    }) 