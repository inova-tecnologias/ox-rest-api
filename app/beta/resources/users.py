import re
from flask_restplus import Resource, Namespace, fields
from sqlalchemy import text
from app import db
from .. import api
from .base import BaseResource
from ..models.users import User as UserModel
from flask import request
from flask_jwt_extended import get_jwt_claims

user_ns = Namespace('Users',path='/users')


@user_ns.route('/')
class UserList(BaseResource):
    # 4-16 symbols, can contain A-Z, a-z, 0-9, _ (_ can not be at the begin/end and can not go in a row (__))
    USERNAME_REGEXP = r'^(?![_])(?!.*[_]{2})[a-zA-Z0-9._]+(?<![_])$'

    # 6-64 symbols, required upper and lower case letters. Can contain !@#$%_  .
    PASSWORD_REGEXP = r'^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])[\w\d!@#$%_]{6,64}$'
    

    @user_ns.marshal_with(UserModel.resource_model)
    @user_ns.doc(
        params={
            'page': 'Default = 1',
            'per_page': 'Default = 10',
            'sort': '',
            'order': '',
            'filter': ''
            })
    def get(self):
        """Get the list of users"""
        claims = get_jwt_claims()
        customer_id = claims['customer_id']
        reseller_id = claims['reseller_id']
        validation = {'customer_id': customer_id} if customer_id else {}
        if reseller_id:
            validation.update({'reseller_id': reseller_id})
        result = self.paginate(UserModel, validation=validation)
        return result.items, {'X-Total-Count': result.total}

        

    @user_ns.marshal_with(UserModel.resource_model)
    @user_ns.expect(UserModel.register_model, validate=True)
    @user_ns.response(400, 'username or password incorrect')
    def post(self):
        """ Create User """
        data = api.payload        
        user = self.make_instance(UserModel, data)
        db.session.add(user)
        db.session.commit()
        return user, 201
'''
        username = data['username']
        password = data['password']
        if not re.search(self.USERNAME_REGEXP, username):
            raise ValidationException(error_field_name='username',
                                      message='4-16 symbols, can contain A-Z, a-z, 0-9, _ \
                                      (_ can not be at the begin/end and can not go in a row (__))')

        if not re.search(self.PASSWORD_REGEXP, password):
            raise ValidationException(error_field_name='password',
                                      message='6-64 symbols, required upper and lower case letters. Can contain !@#$%_')

        if UserModel.query.filter_by(username=username).first():
            raise ValidationException(error_field_name='username', message='This username is already exists')
'''        



@user_ns.route('/<user_id>')
class User(BaseResource):
    @user_ns.response(404, 'User Not Found')
    @user_ns.marshal_with(UserModel.resource_model)
    def get(self, user_id):
        """Get one User"""
        cid = get_jwt_claims()['customer_id']
        query = {'id': user_id}
        if cid:
            query.update({'customer_id': cid})

        result = UserModel.query.filter_by(**query).first_or_404

        return result


    @user_ns.response(404, 'User Not Found')
    @user_ns.response(204, 'User deleted')
    @user_ns.marshal_with(UserModel.resource_model)
    def delete(self, user_id):
        """Delete one User"""
        cid = get_jwt_claims()['customer_id']
        query = {'id': user_id}
        if cid:
            query.update({'customer_id': cid})

        result = UserModel.query.filter_by(**query).first_or_404()
        db.session.delete(result)
        db.session.commit()
        return result, 200


    @user_ns.expect(UserModel.register_model)  
    @user_ns.marshal_with(UserModel.resource_model)
    def put(self, user_id):
        """Edit User""" 
        data = api.payload
        cid = get_jwt_claims()['customer_id']
        query = {'id': user_id}
        if cid:
            query.update({'customer_id': cid})

        result = UserModel.query.filter_by(**query)
        result.update(data)
        db.session.commit()
        result = result.first()
        return result, 200
