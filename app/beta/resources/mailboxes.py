from flask_restplus import Resource, Namespace, fields
from flask_jwt_extended import get_jwt_claims
from app import db
from app.config import app_config
from .base import BaseResource
from .. import api
from ..models.mailboxes import Mailbox as MbxModel
from ..models.plans import Plan as PlanModel
if app_config.USE_OX:
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
        claims = get_jwt_claims()
        customer_id = claims['customer_id']
        reseller_id = claims['reseller_id']
        permited_contexts = claims['contexts']

        if customer_id or reseller_id:
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
        plan = PlanModel.query.filter_by(id=api.payload['plan_id']).first_or_404()
        maxQuota = plan.quota * 1024
        oxplan =  plan.oxid
        aliases = data.pop('aliases', [])
        userAttributes = {
            "userAttributes": {
                "entries": {
                    "key": "config",
                    "value": {
                        "entries": {
                            "key": "com.openexchange.unifiedquota.enabled",
                            "value": "true"
                        } 
                    }
                }
            }
        }
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
            'maxQuota': maxQuota,
            'defaultSenderAddress': data['email'],
            'language': 'pt_BR',
            'timezone': 'America/Sao_Paulo',
        }

        mailbox.update(userAttributes)
        
        if app_config.USE_OX:
            mbxid = OXMbx.service.createByModuleAccessName(
                auth=oxcreds,
                usrdata=mailbox,
                ctx={'id': data['ctx_id']},
                access_combination_name=oxplan
            )['id']
            OXaaS.service.setMailQuota(
                ctxid = data['ctx_id'],
                usrid = mbxid,
                quota = maxQuota,
                creds = oxcreds
            )
        else:
            mbxid = -1

        data.update({'ox_id': mbxid, 'maxQuota': maxQuota})
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
        if app_config.USE_OX:
            OXMbx.service.delete(
                auth=oxcreds,
                ctx={'id': result.ctx_id},
                user={'id': result.ox_id}
                )        
        
        db.session.delete(result)
        db.session.commit()
        return result

    @mbx_ns.expect(MbxModel.edit_model)  
    @mbx_ns.marshal_with(MbxModel.resource_model)
    def put(self, mbx_id):
        """Edit Mailbox"""
        data = api.payload
        data = {key: data[key] for key in MbxModel.edit_model.keys() & data}
        customer_id = get_jwt_claims()['customer_id']
        permited_contexts = get_jwt_claims()['contexts']

        if customer_id:
            condition = MbxModel.ctx_id.in_(permited_contexts)
        else:
            condition = True
        
        result = MbxModel.query.filter(condition).filter_by(id=mbx_id).first_or_404()
        
        plan_id = data.pop('plan_id', None)
        if plan_id:
            plan = PlanModel.query.filter_by(id=plan_id).first_or_404()
            maxQuota = plan.quota * 1024
            oxplan =  plan.oxid
            if app_config.USE_OX:
                OXMbx.service.changeByModuleAccessName(
                    auth=oxcreds,
                    user={
                        'id': result.ox_id,
                        'maxQuota': maxQuota
                        },
                    ctx={'id': result.ctx_id},
                    access_combination_name=oxplan
                )

                OXaaS.service.setMailQuota(
                    ctxid = result.ctx_id,
                    usrid = result.ox_id,
                    quota = maxQuota,
                    creds = oxcreds
                )
            result.maxQuota=maxQuota
            result.plan_id=plan_id  

        oxdata = data.copy()
        oxdata['id'] = result.ox_id
        if data.get('enabled') != None:
            oxdata['mailenabled'] = oxdata.pop('enabled')

        if app_config.USE_OX:
            OXMbx.service.change(
                auth=oxcreds,
                usrdata=oxdata,
                ctx={'id': result.ctx_id}
            )

        db.session.commit()
        return result, 200
        
        