from flask_restplus import Resource, Namespace, fields
from flask_jwt_extended import get_jwt_claims

from .base import BaseResource
from .. import api
from ..models.groups import Group as GroupModel


group_ns = Namespace('Groups', path='/groups')

@group_ns.route('')
class GroupList(BaseResource):
    @group_ns.marshal_with(GroupModel.resource_model)
    def get(self):
        """Get the list of groups"""
        customer_id = get_jwt_claims()['customer_id']
        permited_contexts = get_jwt_claims()['contexts']

        if customer_id:
            condition = GroupModel.ctx_id.in_(permited_contexts)
        else:
            condition = True
        
        result = self.paginate(GroupModel, condition=condition)
        return result.items, {'X-Total-Count': result.total}


    @group_ns.marshal_with(GroupModel.resource_model)
    @group_ns.expect(GroupModel.register_model, validate=True)
    def post(self):
        """Insert a Group"""
        data = api.payload
        data.update({'ox_id': mbxid})
        instance = self.make_instance(GroupModel, data)
        db.session.add(instance)
        db.session.commit()
        return instance


@group_ns.route('/<mbx_id>')
class Group(BaseResource):
    @group_ns.marshal_with(GroupModel.resource_model)
    def get(self, mbx_id):
        customer_id = get_jwt_claims()['customer_id']
        permited_contexts = get_jwt_claims()['contexts']

        if customer_id:
            condition = GroupModel.ctx_id.in_(permited_contexts)
        else:
            condition = True
        
        result = GroupModel.query.filter(condition).filter_by(id=mbx_id).first_or_404()
        return result


    @group_ns.marshal_with(GroupModel.resource_model)
    @group_ns.response(404, 'group Not Found')
    @group_ns.response(204, 'group deleted')
    def delete(self, mbx_id):
        """Delete group"""
        result = self.delete_one(GroupModel, mbx_id)
        return result