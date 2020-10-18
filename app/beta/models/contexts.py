from flask_restplus import fields

from app import db
from .. import api
from datetime import datetime


class Context(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    status = db.Column(db.String(20), default="creating", onupdate="updating")
    description = db.Column(db.String(256))

    created = db.Column(db.DateTime, default=datetime.utcnow)
    changed = db.Column(db.DateTime)

    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)    
    reseller_id = db.Column(db.Integer, db.ForeignKey('reseller.id'), nullable=False)
    
    ox_id = db.Column(db.Integer, unique=True)
    # OX Cloud dependencies
    maxQuota = db.Column(db.Integer, default=500)
    usedQuota = db.Column(db.Integer, default=0)
    admin = db.Column(db.String(200))
    password = db.Column(db.String(200))
    
    # Models
    register_model = api.model('Register Context', {
    'name': fields.String(required=True),
    'description': fields.String(),
    'reseller_id': fields.Integer(),
    'customer_id': fields.Integer()
    })
    
    resource_model = api.model('Context', {
    'id': fields.Integer(),
    'name': fields.String(),
    'description': fields.String(),
    'status': fields.String(),
    'created': fields.DateTime(),
    'changed': fields.DateTime(),
    'usedQuota': fields.Integer(),
    'ox_id': fields.Integer(),
    'customer_id': fields.Integer(),
    'reseller_id': fields.Integer(),
    })

    theme_model = api.model('Theming', {
    'context_id': fields.Integer(),
    'mainColor': fields.String(),
    'logoURL': fields.String(),
    'logoWidth': fields.Integer(default=60),
    })  

