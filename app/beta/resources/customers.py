from flask_restplus import Resource, Namespace, fields
from flask_jwt_extended import get_jwt_claims

from app import db
from .base import BaseResource
from .. import api
from ..models.customers import Customer as CustomerModel


customer_ns = Namespace('Customers',path='/customers')


@customer_ns.route('/')
class CustomerList(BaseResource):
    @customer_ns.marshal_with(CustomerModel.resource_model)
    @customer_ns.doc(
    params={
            'page': 'Default = 1',
            'per_page': 'Default = 10',
            'sort': '',
            'order': '',
            'filter': ''
    })
    def get(self):
        """Get the list of Customers"""
        validation = self.validate(CustomerModel, roles=['admin', 'reseller'])
        return self.get_many(CustomerModel, validation=validation)

    @customer_ns.expect(CustomerModel.register_model, validate=True)
    @customer_ns.marshal_with(CustomerModel.resource_model)
    def post(self):
        """Insert a Customer"""
        validation = self.validate(CustomerModel, roles=['admin', 'reseller'])
        data = api.payload   
        data.update(validation)
             
        return self.insert_one(CustomerModel, data)


@customer_ns.route('/<int:customer_id>')
class Customer(BaseResource):
    @customer_ns.response(404, 'Customer Not Found')
    @customer_ns.marshal_with(CustomerModel.resource_model)
    def get(self, customer_id):
        """Get one Customer"""
        validation = self.validate(CustomerModel, roles=['admin', 'reseller'])
        return self.get_one(CustomerModel, customer_id, validation)


    @customer_ns.response(404, 'Customer Not Found')
    @customer_ns.response(204, 'Customer deleted')
    def delete(self, customer_id):
        """Delete one Customer"""
        validation = self.validate(CustomerModel, roles=['admin', 'reseller'])
        return self.delete_one(CustomerModel, customer_id, validation)
    

    @customer_ns.expect(CustomerModel.register_model)  
    @customer_ns.marshal_with(CustomerModel.resource_model)
    def put(self, customer_id):
        """Edit Customer""" 
        validation = self.validate(CustomerModel, roles=['admin', 'reseller'])
        data = api.payload
        
        data.pop('users', None) # TODO: update users instead ignore
        data.pop('contexts', None) # TODO: update contexts instead ignore

        return self.update_one(CustomerModel, customer_id, data, validation)
