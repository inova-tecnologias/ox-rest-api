from flask_restplus import Resource, Namespace, fields
from flask_jwt_extended import get_jwt_claims

from app import db
from .base import BaseResource
from .. import api
from ..models.resellers import Reseller as ResellerModel


reseller_ns = Namespace('Resellers',path='/resellers')


@reseller_ns.route('/')
class ResellerList(BaseResource):
    @reseller_ns.marshal_with(ResellerModel.resource_model)
    @reseller_ns.doc(
    params={
            'page': 'Default = 1',
            'per_page': 'Default = 10',
            'sort': '',
            'order': '',
            'filter': ''
    })
    def get(self):
        """Get the list of Resellers"""
        validation = self.validate(ResellerModel, roles=['admin'])
        return self.get_many(ResellerModel, validation=validation)

    @reseller_ns.expect(ResellerModel.register_model, validate=True)
    @reseller_ns.marshal_with(ResellerModel.resource_model)
    def post(self):
        """Insert a Reseller"""
        validation = self.validate(ResellerModel, roles=['admin'])
        data = api.payload   
        data.update(validation)
             
        return self.insert_one(ResellerModel, data)


@reseller_ns.route('/<int:reseller_id>')
class Reseller(BaseResource):
    @reseller_ns.response(404, 'Reseller Not Found')
    @reseller_ns.marshal_with(ResellerModel.resource_model)
    def get(self, reseller_id):
        """Get one Reseller"""
        validation = self.validate(ResellerModel, roles=['admin'])
        return self.get_one(ResellerModel, reseller_id, validation)


    @reseller_ns.marshal_with(ResellerModel.resource_model)
    @reseller_ns.response(404, 'Reseller Not Found')
    @reseller_ns.response(204, 'Reseller deleted')
    def delete(self, reseller_id):
        """Delete one Reseller"""
        validation = self.validate(ResellerModel, roles=['admin'])
        return self.delete_one(ResellerModel, reseller_id, validation)
    

    @reseller_ns.expect(ResellerModel.register_model)  
    @reseller_ns.marshal_with(ResellerModel.resource_model)
    def put(self, reseller_id):
        """Edit Reseller""" 
        validation = self.validate(ResellerModel, roles=['admin'])
        data = api.payload
        
        data.pop('customers', None) # TODO: update customers instead ignore
        data.pop('users', None) # TODO: update users instead ignore
        data.pop('contexts', None) # TODO: update contexts instead ignore

        return self.update_one(ResellerModel, reseller_id, data, validation)
