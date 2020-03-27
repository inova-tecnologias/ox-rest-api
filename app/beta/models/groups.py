from flask_restplus import fields

from app import db
from .. import api

mailbox_model = api.model('Mailbox', {
    'id': fields.Integer(),
    'display_name': fields.String(),
    'email': fields.String(),
    'usedQuota': fields.Integer(),
    'maxQuota': fields.Integer(),
    'enabled': fields.Boolean(),
    'ctx_id': fields.Integer(),
    'ox_id': fields.Integer(),
    }) 

association_table = db.Table('group_member', db.Model.metadata,
    db.Column('group_id', db.Integer, db.ForeignKey('group.id')),
    db.Column('mailbox_id', db.Integer, db.ForeignKey('mailbox.id'))
)

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), unique=True, nullable=False)
    members = db.relationship("Mailbox",
                    secondary=association_table)

    register_model = api.model('Register Group', {
    'email': fields.String(required=True),
    })
    
    resource_model = api.model('Group', {
    'id': fields.Integer(),
    'email': fields.String(),
    'member': fields.List(fields.Integer())
    })  

 