from flask_restplus import Resource, Namespace, fields
from flask_jwt_extended import get_jwt_claims
from app import db
from .base import BaseResource
from .. import api
from ..models.mailboxes import Mailbox as MbxModel
from ..soap.ox import (
    oxaasadmctx, 
    credentials as oxcreds,
    User as OXMbx,
    OxaaSService as OXaaS
)

mbx_ns = Namespace('Mailboxes', path='/mailboxes')

@mbx_ns.route('')
class MbxList(BaseResource):
    @mbx_ns.marshal_with(MbxModel.resource_model)
    def get(self):
        """Get the list of Mailboxes"""
        customer_id = get_jwt_claims()['customer_id']
        permited_contexts = get_jwt_claims()['contexts']

        if customer_id:
            condition = MbxModel.ctx_id.in_(permited_contexts)
        else:
            condition = True
        result = self.paginate(MbxModel, condition=condition)
        return result.items, {'X-Total-Count': result.total}


    @mbx_ns.marshal_with(MbxModel.resource_model)
    @mbx_ns.expect(MbxModel.register_model, validate=True)
    def post(self):
        """Insert a Mailbox"""
        data = api.payload
        aliases = data.pop('aliases', [])
        mailbox = {
            'name': data['email'],
            'aliases': aliases,
            'password': data['password'],
            'display_name': "%s %s" %(
                data['given_name'], 
                data['last_name']
            ),
            'given_name': data['given_name'],
            'sur_name': data['last_name'],
            'primaryEmail': data['email'],
            'email1': data['email'],
            'defaultSenderAddress': data['email'],
            'language': 'en_US',
            'timezone': 'America/Sao_Paulo',
        }

        mbxid = OXMbx.service.createByModuleAccessName(
            auth=oxcreds,
            usrdata=mailbox,
            ctx={'id': data['ctx_id']},
            access_combination_name='groupware_premium'
        )['id']

        OXaaS.service.setMailQuota(
            ctxid = data['ctx_id'],
            usrid = mbxid,
            quota = data['maxQuota'],
            creds = oxcreds
        )

        data.update({'ox_id': mbxid})
        instance = self.make_instance(MbxModel, data)
        db.session.add(instance)
        db.session.commit()
        return instance


@mbx_ns.route('/<mbx_id>')
class Mbx(BaseResource):
    @mbx_ns.response(404, 'Mailbox Not Found')
    @mbx_ns.marshal_with(MbxModel.resource_model)
    def get(self, mbx_id):
        """Get one Mailbox"""
        customer_id = get_jwt_claims()['customer_id']
        permited_contexts = get_jwt_claims()['contexts']

        if customer_id:
            condition = MbxModel.ctx_id.in_(permited_contexts)
        else:
            condition = True
        
        result = MbxModel.query.filter(condition).filter_by(id=mbx_id).first_or_404()
        return result


    @mbx_ns.marshal_with(MbxModel.resource_model)
    @mbx_ns.response(404, 'Mailbox Not Found')
    @mbx_ns.response(204, 'Mailbox deleted')
    def delete(self, mbx_id):
        """Delete Mailbox"""
        customer_id = get_jwt_claims()['customer_id']
        permited_contexts = get_jwt_claims()['contexts']

        if customer_id:
            condition = MbxModel.ctx_id.in_(permited_contexts)
        else:
            condition = True
        
        result = MbxModel.query.filter(condition).filter_by(id=mbx_id).first_or_404()
        OXMbx.service.delete(
            auth=oxcreds,
            ctx={'id': result.ctx_id},
            user={'id': result.ox_id}
            )
        return result

    @mbx_ns.expect(MbxModel.register_model)  
    @mbx_ns.marshal_with(MbxModel.resource_model)
    def put(self, mbx_id):
        """Edit Mailbox"""
        data = api.payload
        data.pop('display_name', None) # TODO: remove display_name
        customer_id = get_jwt_claims()['customer_id']
        permited_contexts = get_jwt_claims()['contexts']

        if customer_id:
            condition = MbxModel.ctx_id.in_(permited_contexts)
        else:
            condition = True
        
        result = MbxModel.query.filter(condition).filter_by(id=mbx_id)
        
        result.update(data)
        db.session.commit()
        result = result.first()
        return result, 200
        
        