from flask_restplus import Resource, Namespace, fields
from flask_jwt_extended import get_jwt_claims
from app import db
from .base import BaseResource
from .. import api
from ..models.mailboxes import Mailbox as MbxModel
from ..models.plans import Plan as PlanModel


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
            condition = MbxModel.context_id.in_(permited_contexts)
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
            condition = MbxModel.context_id.in_(permited_contexts)
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
            condition = MbxModel.context_id.in_(permited_contexts)
        else:
            condition = True
        
        result = MbxModel.query.filter(condition).filter_by(id=mbx_id).first_or_404()     
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
            condition = MbxModel.context_id.in_(permited_contexts)
        else:
            condition = True
        
        result = MbxModel.query.filter(condition).filter_by(id=mbx_id).first_or_404()
        
        plan_id = data.pop('plan_id', None)
        if plan_id:
            plan = PlanModel.query.filter_by(id=plan_id).first_or_404()
            maxQuota = plan.quota * 1024
            oxplan =  plan.oxid
            result.maxQuota=maxQuota
            result.plan_id=plan_id  

        oxdata = data.copy()
        oxdata['id'] = result.ox_id
        if data.get('enabled') != None:
            oxdata['mailenabled'] = oxdata.pop('enabled')

        db.session.commit()
        return result, 200
        
        