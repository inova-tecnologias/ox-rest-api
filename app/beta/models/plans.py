from flask_restplus import fields

from app import db
from .. import api
from datetime import datetime


class Plan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    changed = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    description = db.Column(db.String(50))
    
    #OX Requirements
    ma = db.Column(db.String(50))
    config = db.Column(db.String(300))
    quota = db.Column(db.Integer)


    # Models
    register_model = api.model('Register Plan', {
    'name': fields.String(required=True),
    'ma': fields.String(required=True),
    'quota': fields.Integer(required=True),
    'config': fields.String(),
    'description': fields.String()
    })
    
    resource_model = api.model('Plan', {
    'id': fields.Integer(),
    'name': fields.String(),
    'ma': fields.String(),
    'quota': fields.Integer(),
    'config': fields.String(),
    'description': fields.String(),
    })  
