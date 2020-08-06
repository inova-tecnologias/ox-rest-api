from flask_restplus import fields

from app import db
from .. import api


class Plan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    oxid = db.Column(db.String(50))
    description = db.Column(db.String(50))
    quota = db.Column(db.Integer)


    # Models
    register_model = api.model('Register Plan', {
    'name': fields.String(required=True),
    'oxid': fields.String(required=True),
    'quota': fields.Integer(required=True),
    'description': fields.String()
    })
    
    resource_model = api.model('Plan', {
    'id': fields.Integer(),
    'name': fields.String(),
    'oxid': fields.String(),
    'quota': fields.Integer(),
    'description': fields.String(),
    })  
