from flask_restplus import Resource, Namespace, fields
from flask_jwt_extended import get_jwt_claims

from app import db
from app.util import random_password
from .base import BaseResource
from .. import api
from ..models.contexts import Context as CtxModel
from ..soap.ox import (
    oxaasadmctx, 
    credentials as oxcreds,
    Context as OXCtx
)

ctx_ns = Namespace('Contexts', path='/contexts')


@ctx_ns.route('/')
class CtxList(BaseResource):
    @ctx_ns.marshal_with(CtxModel.resource_model)
    def get(self):
        """Get the list of Contexts"""
        customer_id = get_jwt_claims()['customer_id']
        validation = {'customer_id': customer_id} if customer_id else {}    
        result = self.paginate(CtxModel, validation=validation)
        return result.items, {'X-Total-Count': result.total}


    @ctx_ns.marshal_with(CtxModel.resource_model)
    @ctx_ns.expect(CtxModel.register_model, validate=True)
    def post(self):
        """Insert a Context"""
        data = api.payload

        name = data['name']
        password = random_password()
        sur_name = "Context Admin"

        ctxname = (oxaasadmctx, name)
        mail = "oxadmin@%s_%s" %ctxname
        
        admin_user = {
            'name': "oxadmin+%s_%s" %ctxname,
            'password': password,
            'display_name': "%s %s" %(name, sur_name),
            'given_name': name,
            'sur_name': sur_name,
            'primaryEmail': mail,
            'email1': mail
        }
        ctx = {
            'maxQuota': 500,
            'name': "%s_%s" %ctxname
        } 
        ctxid = OXCtx.service.create(auth=oxcreds, ctx=ctx, admin_user=admin_user)['id']
        data.update({'ox_id': ctxid})
        instance = self.make_instance(CtxModel, data)
        db.session.add(instance)
        db.session.commit()
        return instance, 201


@ctx_ns.route('/<ctx_id>')
class Ctx(BaseResource):
    @ctx_ns.response(404, 'Context Not Found')
    @ctx_ns.marshal_with(CtxModel.resource_model)
    def get(self, ctx_id):
        """Get one Context"""
        cid = get_jwt_claims()['customer_id']
        query = {'id': ctx_id}
        if cid:
            query.update({'customer_id': cid})

        result = CtxModel.query.filter_by(**query).first_or_404


    @ctx_ns.marshal_with(CtxModel.resource_model)
    @ctx_ns.response(404, 'Context Not Found')
    @ctx_ns.response(204, 'Context deleted')
    def delete(self, ctx_id):
        """Delete Context"""
        cid = get_jwt_claims()['customer_id']
        query = {'id': ctx_id}
        if cid:
            query.update({'customer_id': cid})

        result = CtxModel.query.filter_by(**query).first_or_404()
        db.session.delete(result)
        db.session.commit()
        OXCtx.service.delete(auth=oxcreds, ctx={'id': ctx_id})
        return result, 
        
    @ctx_ns.expect(CtxModel.register_model)  
    @ctx_ns.marshal_with(CtxModel.resource_model)
    def put(self, ctx_id):
        """Edit Context""" 
        data = api.payload
        data.pop('mailboxes', None) # TODO: update mailboxes instead ignore
        data.pop('groups', None) # TODO: update groups instead ignore
        data.pop('ox_id', None) # ox_id is alias for id

        cid = get_jwt_claims()['customer_id']
        query = {'id': ctx_id}
        if cid:
            query.update({'customer_id': cid})

        result = CtxModel.query.filter_by(**query)

        result.update(data)
        db.session.commit()
        result = result.first()
        return result, 200