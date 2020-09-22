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
        reseller_id = get_jwt_claims()['reseller_id']
        validation = {'id': reseller_id} if reseller_id else {}    
        result = self.paginate(ResellerModel, validation=validation)
        return result.items, {'X-Total-Count': result.total}

    @reseller_ns.expect(ResellerModel.register_model, validate=True)
    @reseller_ns.marshal_with(ResellerModel.resource_model)
    def post(self):
        """Insert a Reseller"""
        data = api.payload        
        reseller = self.make_instance(ResellerModel, data)
        db.session.add(reseller)
        db.session.commit()
        return reseller


@reseller_ns.route('/<int:reseller_id>')
class Reseller(BaseResource):
    @reseller_ns.response(404, 'Reseller Not Found')
    @reseller_ns.marshal_with(ResellerModel.resource_model)
    def get(self, reseller_id):
        """Get one Reseller"""
        cid = get_jwt_claims()['reseller_id']
        query = {'id': reseller_id}
        if ((cid) and (cid != reseller_id)):
            query.update({'id': False})

        result = ResellerModel.query.filter_by(**query).first_or_404()
        return result


    @reseller_ns.response(404, 'Reseller Not Found')
    @reseller_ns.response(204, 'Reseller deleted')
    def delete(self, reseller_id):
        """Delete one Reseller"""
        cid = get_jwt_claims()['reseller_id']
        query = {'id': reseller_id}
        if ((cid) and (cid != reseller_id)):
            query.update({'id': False})

        result = ResellerModel.query.filter_by(**query).first_or_404()
        db.session.delete(result)
        db.session.commit()
        return result, 200
    

    @reseller_ns.expect(ResellerModel.register_model)  
    @reseller_ns.marshal_with(ResellerModel.resource_model)
    def put(self, reseller_id):
        """Edit Reseller""" 
        data = api.payload
        data.pop('users', None) # TODO: update users instead ignore
        data.pop('contexts', None) # TODO: update contexts instead ignore
        cid = get_jwt_claims()['reseller_id']
        query = {'id': reseller_id}
        if ((cid) and (cid != reseller_id)):
            query.update({'id': False})

        result = ResellerModel.query.filter_by(**query)
        result.update(data)
        db.session.commit()
        result = result.first()
        return result, 200
