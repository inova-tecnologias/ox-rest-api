from flask_restplus import fields

from app import db
from .. import api
from datetime import datetime


class Mailbox(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    status = db.Column(db.String(20), default="creating", onupdate="updating")
    created = db.Column(db.DateTime, default=datetime.utcnow)
    changed = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    given_name = db.Column(db.String(35))
    last_name = db.Column(db.String(35))
    display_name = db.Column(db.String(35))
    _password = db.Column(db.String(30))
    maxQuota = db.Column(db.Integer, default=50)
    usedQuota = db.Column(db.Integer, default=0)
    plan_id = db.Column(db.Integer, nullable=False)
    ox_id = db.Column(db.Integer)
    context_id = db.Column(db.Integer, db.ForeignKey('context.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)    
    reseller_id = db.Column(db.Integer, db.ForeignKey('reseller.id'), nullable=False)


    @property
    def password(self):
        raise AttributeError('Password not readable')

    @password.setter
    def password(self, password):
        self._password = password


    register_model = api.model('Register Mailbox', {
    'password': fields.String(required=True),
    'email': fields.String(required=True),
    'plan_id': fields.Integer(required=True),
    'given_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'display_name': fields.String(required=True),
    'context_id': fields.Integer(required=True),
    'customer_id': fields.Integer(),
    'reseller_id': fields.Integer(),
    })
    
    resource_model = api.model('Mailbox', {
    'id': fields.Integer(),
    'display_name': fields.String(),
    'given_name': fields.String(),
    'last_name': fields.String(),
    'email': fields.String(),
    'plan_id': fields.Integer(),
    'usedQuota': fields.Integer(),
    'maxQuota': fields.Integer(),
    'status': fields.String(),
    'context_id': fields.Integer(),
    'ox_id': fields.Integer(),
    'aliases': fields.List(fields.String()),
    'customer_id': fields.Integer(),
    'reseller_id': fields.Integer(),
    })

    edit_model = api.model('Edit Mailbox', {
    'plan_id': fields.Integer(),
    'password': fields.String(),
    'status': fields.String(),
    })
