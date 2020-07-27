from flask_restplus import fields

from app import db
from .. import api
from ..models.groups import association_table


class Mailbox(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    given_name = db.Column(db.String(35))
    last_name = db.Column(db.String(35))
    _password = db.Column(db.String(30))
    maxQuota = db.Column(db.Integer, default=50)
    usedQuota = db.Column(db.Integer, default=0)
    plan_id = db.Column(db.Integer, nullable=False)
    enabled = db.Column(db.Boolean, default=True)
    groups = db.relationship("Group", secondary=association_table)
    ox_id = db.Column(db.Integer, nullable=False)
    ctx_id = db.Column(db.Integer, db.ForeignKey('context.id'))
    

    @property
    def display_name(self):
        dn = "%s %s" %(self.given_name, self.last_name)
        return dn

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
    'ctx_id': fields.Integer(required=True)
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
    'enabled': fields.Boolean(),
    'ctx_id': fields.Integer(),
    'ox_id': fields.Integer(),
    'aliases': fields.List(fields.String())
    })

