from flask_restplus import Resource, Namespace
from flask_migrate import MigrateCommand
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required,
    jwt_refresh_token_required, get_jwt_identity, get_raw_jwt,
    get_jwt_claims, decode_token
)

from app import db, jwt
from .. import api
from ..models.customers import Customer as CustomerModel
from ..models.users import User as UserModel
from ..models.auth import Token

auth_ns = Namespace('Authentication', path='/auth')


# TODO - Refact MigrateCommand to a better place instead auth.py
@MigrateCommand.command
def admin():
    ''' Create Admin Account'''
    print("Creating admin account...")
    user = UserModel()
    model = user.register_model
    
    for attr in [
        'username',
        'password',
        'reseller_id',
        'customer_id'
    ]:
        model.__delitem__(attr)
    
    user.username = input('Username: ')
    from getpass import getpass
    user.password = getpass()

    for attr in model.keys():
        setattr(user, attr, input(attr.capitalize() + ": "))
    
    db.session.add(user)
    db.session.commit()
#

# JWT manipulation
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return Token.query.filter_by(jti=jti).one().revoked


@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    user = UserModel.query.filter_by(username=identity).first()
    
    customer_id = user.customer_id
    reseller_id = user.reseller_id

    claims = dict(
        id = user.id,
        name = user.name,
        username = user.username,
        role = user.role,
        reseller_id = reseller_id,
        customer_id = customer_id,
    )
    return claims


@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.doc(security=[])
    @auth_ns.expect(UserModel.login_model)
    @auth_ns.response(200, 'Success', UserModel.return_token_model)
    @auth_ns.response(401, 'Incorrect username or password')
    def post(self):
        """Generate Access and Refresh token"""
        username = api.payload['username']
        user = UserModel.query.filter_by(username=username).first()
        if not user:
            auth_ns.abort(401, 'Incorrect username or password')
    
        from werkzeug.security import check_password_hash, generate_password_hash
        password = api.payload['password']
        if check_password_hash(user.password_hash, password):        
            access_token = create_access_token(identity=username)
            refresh_token = create_refresh_token(identity=username)

            a_token_jti = decode_token(access_token)['jti']
            r_token_jti = decode_token(refresh_token)['jti']
            
            a = Token(jti=a_token_jti, identity=username)
            r = Token(jti=r_token_jti, identity=username)

            db.session.add(a)
            db.session.add(r)

            db.session.commit()

            return (
                {'message': 'Logged in as %s' % (username)},
                200,
                {
                    'X-Auth-Token': access_token,
                    'X-Refresh-Token': refresh_token
                }
            )
        
        auth_ns.abort(401, 'Incorrect username or password')


@auth_ns.route('/logout')
class logout(Resource):
    @jwt_required
    def post(self):
        """Expire all access and refresh tokens from logged user"""
        identity = get_jwt_identity()
        tokens = Token.query.filter_by(revoked=False, identity=identity).all()
        for token in tokens:
            token.revoked=True
            db.session.add(token)
        db.session.commit()

@auth_ns.route('/refresh')
class refresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        """Renew access token"""
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)

        a_token_jti = decode_token(access_token)['jti']
        a = Token(jti=a_token_jti, identity=username)

        db.session.add(a)    
        db.session.commit()

        return {'access_token': access_token}