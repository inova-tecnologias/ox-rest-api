from app import db
from .. import api
from datetime import datetime


class Token(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    jti = db.Column(db.String(300))
    identity = db.Column(db.String(30))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    revoked = db.Column(db.Boolean(), default=False)