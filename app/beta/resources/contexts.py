from flask_restplus import Resource, Namespace, fields
from flask_jwt_extended import get_jwt_claims

from app import db
from app.util import random_password
from .base import BaseResource
from .. import api
from ..models.contexts import Context as ContextModel

context_ns = Namespace('Contexts', path='/contexts')
theme_ns = Namespace('Theme', path='/theme')


@context_ns.route('/')
class ContextList(BaseResource):
    @context_ns.marshal_with(ContextModel.resource_model)
    def get(self):
        """Get the list of Contexts"""
        validation = self.validate(ContextModel)
        return self.get_many(ContextModel, validation=validation)


    @context_ns.marshal_with(ContextModel.resource_model)
    @context_ns.expect(ContextModel.register_model, validate=True)
    def post(self):
        """Insert a Context"""
        validation = self.validate(ContextModel)
        data = api.payload   
        data.update(validation)
             
        return self.insert_one(ContextModel, data)


@context_ns.route('/<context_id>')
class Context(BaseResource):
    @context_ns.response(404, 'Context Not Found')
    @context_ns.marshal_with(ContextModel.resource_model)
    def get(self, context_id):
        """Get one Context"""
        validation = self.validate(ContextModel)
        return self.get_one(ContextModel, context_id, validation)


    @context_ns.marshal_with(ContextModel.resource_model)
    @context_ns.response(404, 'Context Not Found')
    @context_ns.response(204, 'Context deleted')
    def delete(self, context_id):
        """Delete Context"""
        validation = self.validate(ContextModel)
        return self.delete_one(ContextModel, context_id, validation)

        
    @context_ns.expect(ContextModel.register_model)  
    @context_ns.marshal_with(ContextModel.resource_model)
    def put(self, context_id):
        """Edit Context""" 
        validation = self.validate(ContextModel)
        data = api.payload

        return self.update_one(ContextModel, context_id, data, validation)


@context_ns.route('/<context_id>/theme')
class Theme(BaseResource):
    @context_ns.marshal_with(ContextModel.theme_model)
    @context_ns.expect(ContextModel.theme_model, validate=True)
    @context_ns.response(200, 'Theme updated')
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
    @context_ns.marshal_with(ContextModel.theme_model)
    @context_ns.expect(ContextModel.theme_model, validate=True)
    @context_ns.response(200, 'Theme updated')
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
