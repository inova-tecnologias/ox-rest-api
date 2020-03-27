from flask_restplus import Resource, Namespace, fields
from flask_jwt_extended import get_jwt_claims

from app import db
from .base import BaseResource
from .. import api
from ..models.costumers import Costumer as CostumerModel


costumer_ns = Namespace('Costumers',path='/costumers')


@costumer_ns.route('/')
class CostumerList(BaseResource):
    @costumer_ns.marshal_with(CostumerModel.resource_model)
    @costumer_ns.doc(
    params={
            'page': 'Default = 1',
            'per_page': 'Default = 10',
            'sort': '',
            'order': '',
            'filter': ''
    })
    def get(self):
        """Get the list of Costumers"""
        costumer_id = get_jwt_claims()['costumer_id']
        validation = {'id': costumer_id} if costumer_id else {}    
        result = self.paginate(CostumerModel, validation=validation)
        return result.items, {'X-Total-Count': result.total}

    @costumer_ns.expect(CostumerModel.register_model, validate=True)
    @costumer_ns.marshal_with(CostumerModel.resource_model)
    def post(self):
        """Insert a Costumer"""
        data = api.payload        
        costumer = self.make_instance(CostumerModel, data)
        db.session.add(costumer)
        db.session.commit()
        return costumer


@costumer_ns.route('/<int:costumer_id>')
class Costumer(BaseResource):
    @costumer_ns.response(404, 'Costumer Not Found')
    @costumer_ns.marshal_with(CostumerModel.resource_model)
    def get(self, costumer_id):
        """Get one Costumer"""
        cid = get_jwt_claims()['costumer_id']
        query = {'id': costumer_id}
        if ((cid) and (cid != costumer_id)):
            query.update({'id': False})

        result = CostumerModel.query.filter_by(**query).first_or_404()
        return result


    @costumer_ns.response(404, 'Costumer Not Found')
    @costumer_ns.response(204, 'Costumer deleted')
    def delete(self, costumer_id):
        """Delete one Costumer"""
        cid = get_jwt_claims()['costumer_id']
        query = {'id': costumer_id}
        if ((cid) and (cid != costumer_id)):
            query.update({'id': False})

        result = CostumerModel.query.filter_by(**query).first_or_404()
        db.session.delete(result)
        db.session.commit()
        return result, 200
    

    @costumer_ns.expect(CostumerModel.register_model)  
    @costumer_ns.marshal_with(CostumerModel.resource_model)
    def put(self, costumer_id):
        """Edit Costumer""" 
        data = api.payload
        data.pop('users', None) # TODO: update users instead ignore
        data.pop('contexts', None) # TODO: update contexts instead ignore
        cid = get_jwt_claims()['costumer_id']
        query = {'id': costumer_id}
        if ((cid) and (cid != costumer_id)):
            query.update({'id': False})

        result = CostumerModel.query.filter_by(**query)
        result.update(data)
        db.session.commit()
        result = result.first()
        return result, 200
