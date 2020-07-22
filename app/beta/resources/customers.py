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
        customer_id = get_jwt_claims()['customer_id']
        validation = {'id': customer_id} if customer_id else {}    
        result = self.paginate(CustomerModel, validation=validation)
        return result.items, {'X-Total-Count': result.total}

    @customer_ns.expect(CustomerModel.register_model, validate=True)
    @customer_ns.marshal_with(CustomerModel.resource_model)
    def post(self):
        """Insert a Customer"""
        data = api.payload        
        customer = self.make_instance(CustomerModel, data)
        db.session.add(customer)
        db.session.commit()
        return customer


@customer_ns.route('/<int:customer_id>')
class Customer(BaseResource):
    @customer_ns.response(404, 'Customer Not Found')
    @customer_ns.marshal_with(CustomerModel.resource_model)
    def get(self, customer_id):
        """Get one Customer"""
        cid = get_jwt_claims()['customer_id']
        query = {'id': customer_id}
        if ((cid) and (cid != customer_id)):
            query.update({'id': False})

        result = CustomerModel.query.filter_by(**query).first_or_404()
        return result


    @customer_ns.response(404, 'Customer Not Found')
    @customer_ns.response(204, 'Customer deleted')
    def delete(self, customer_id):
        """Delete one Customer"""
        cid = get_jwt_claims()['customer_id']
        query = {'id': customer_id}
        if ((cid) and (cid != customer_id)):
            query.update({'id': False})

        result = CustomerModel.query.filter_by(**query).first_or_404()
        db.session.delete(result)
        db.session.commit()
        return result, 200
    

    @customer_ns.expect(CustomerModel.register_model)  
    @customer_ns.marshal_with(CustomerModel.resource_model)
    def put(self, customer_id):
        """Edit Customer""" 
        data = api.payload
        data.pop('users', None) # TODO: update users instead ignore
        data.pop('contexts', None) # TODO: update contexts instead ignore
        cid = get_jwt_claims()['customer_id']
        query = {'id': customer_id}
        if ((cid) and (cid != customer_id)):
            query.update({'id': False})

        result = CustomerModel.query.filter_by(**query)
        result.update(data)
        db.session.commit()
        result = result.first()
        return result, 200
