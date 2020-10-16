from flask_restplus import Resource, Namespace, fields
from flask_jwt_extended import get_jwt_claims

from app import db
from app.util import random_password
from .base import BaseResource
from .. import api
from ..models.contexts import Context as CtxModel

ctx_ns = Namespace('Contexts', path='/contexts')
theme_ns = Namespace('Theme', path='/theme')


@ctx_ns.route('/')
class CtxList(BaseResource):
    @ctx_ns.marshal_with(CtxModel.resource_model)
    def get(self):
        """Get the list of Contexts"""
        claims = get_jwt_claims()
        customer_id = claims['customer_id']
        reseller_id = claims['reseller_id']
        validation = {'customer_id': customer_id} if customer_id else {}
        if reseller_id: 
            validation.update({'reseller_id': reseller_id}) 
        result = self.paginate(CtxModel, validation=validation)
        return result.items, {'X-Total-Count': result.total}


    @ctx_ns.marshal_with(CtxModel.resource_model)
    @ctx_ns.expect(CtxModel.register_model, validate=True)
    def post(self):
        """Insert a Context"""
        data = api.payload
        instance = self.make_instance(CtxModel, data)
        db.session.add(instance)
        db.session.commit()
        return instance, 201


@ctx_ns.route('/<context_id>')
class Ctx(BaseResource):
    @ctx_ns.response(404, 'Context Not Found')
    @ctx_ns.marshal_with(CtxModel.resource_model)
    def get(self, context_id):
        """Get one Context"""
        cid = get_jwt_claims()['customer_id']
        query = {'id': context_id}
        if cid:
            query.update({'customer_id': cid})

        result = CtxModel.query.filter_by(**query).first_or_404


    @ctx_ns.marshal_with(CtxModel.resource_model)
    @ctx_ns.response(404, 'Context Not Found')
    @ctx_ns.response(204, 'Context deleted')
    def delete(self, context_id):
        """Delete Context"""
        claims = get_jwt_claims()
        cid = claims['customer_id']
        rid = claims['reseller_id']
        query = {'id': context_id}
        if cid:
            query.update({'customer_id': cid})
        if rid:
            query.update({'reseller_id': rid})

        result = CtxModel.query.filter_by(**query).first_or_404()
        db.session.delete(result)
        db.session.commit()
        return result, 
        
    @ctx_ns.expect(CtxModel.register_model)  
    @ctx_ns.marshal_with(CtxModel.resource_model)
    def put(self, context_id):
        """Edit Context""" 
        data = api.payload
        data.pop('mailboxes', None) # TODO: update mailboxes instead ignore
        data.pop('groups', None) # TODO: update groups instead ignore
        data.pop('ox_id', None) # ox_id is alias for id

        cid = get_jwt_claims()['customer_id']
        rid = get_jwt_claims()['reseller_id']
        query = {'id': context_id}
        if cid:
            query.update({'customer_id': cid})
        if rid:
            query.update({'reseller_id': rid})

        result = CtxModel.query.filter_by(**query)

        result.update(data)
        db.session.commit()
        result = result.first()
        return result, 200


@ctx_ns.route('/<context_id>/theme')
class Theme(BaseResource):
    @ctx_ns.marshal_with(CtxModel.theme_model)
    @ctx_ns.expect(CtxModel.theme_model, validate=True)
    @ctx_ns.response(200, 'Theme updated')
    def put(self, context_id):
        """Set Context theme"""
        data = api.payload
        entries = []
        for entrie in data:
            entries.append({'key' : 'io.ox/dynamic-theme//' + entrie, 'value': data[entrie]})
        context = {
            'id': context_id,
            "userAttributes": {
                "entries": {
                    "key": "config",
                    "value": {
                        "entries": entries 
                    }
                }
            }
        }


@theme_ns.route('/')
class ExtTheme(BaseResource):
    @ctx_ns.marshal_with(CtxModel.theme_model)
    @ctx_ns.expect(CtxModel.theme_model, validate=True)
    @ctx_ns.response(200, 'Theme updated')
    def post(self):
        """Set Context theme"""
        data = api.payload
        context_id = data.pop('context_id')
        
        entries = []
        for entrie in data:
            entries.append({'key' : 'io.ox/dynamic-theme//' + entrie, 'value': data[entrie]})
        context = {
            'id': context_id,
            "userAttributes": {
                "entries": {
                    "key": "config",
                    "value": {
                        "entries": entries 
                    }
                }
            }
        }
