from flask_restplus import fields
from werkzeug.security import generate_password_hash
from sqlalchemy import event



from app import db
from .. import api


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(50))
    description = db.Column(db.String(200))
    reseller_id = db.Column(db.Integer, db.ForeignKey('reseller.id'))    
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))    
    
    password_hash = db.Column(db.String(150), nullable=False)

    @property
    def role(self):
        if self.customer_id:
            role = "customer"
        elif self.reseller_id:
            role = "reseller"
        else:
            role = "admin"

        return role

    @property
    def password(self):
        raise AttributeError('Password not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)


    resource_model = api.model('User', {
        'id': fields.Integer(),
        'username': fields.String(),
        'role': fields.String(),
        'name': fields.String(),
        'description': fields.String(),
        'reseller_id': fields.Integer(),
        'customer_id': fields.Integer()


    })

    register_model = api.model('Register User', {
    'username': fields.String(required=True),
    'password': fields.String(required=True),
    'name': fields.String(),
    'description': fields.String(),
    'reseller_id': fields.Integer(),
    'customer_id': fields.Integer()

    })

    login_model = api.model('Login', {
    'username': fields.String(required=True),
    'password': fields.String(required=True)
    })
    
    return_token_model = api.model('AuthToken', {
    'access_token': fields.String(required=True),
    'refresh_token': fields.String(required=True)
    })
    

@event.listens_for(User, 'before_insert')
def teste(m, c, t):
    print("Start Load")
    print (m, c, t)