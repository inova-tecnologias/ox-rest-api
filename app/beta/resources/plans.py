from flask_restplus import Resource, Namespace, fields
from flask_jwt_extended import get_jwt_claims

from app import db

from .base import BaseResource
from .. import api
from ..models.plans import Plan as PlanModel


plan_ns = Namespace('Plan', path='/plans')


@plan_ns.route('/')
class PlanList(BaseResource):
    @plan_ns.marshal_with(PlanModel.resource_model)
    def get(self):
        """Get the list of Plans"""
        return result.items, {'X-Total-Count': result.total}


    @plan_ns.marshal_with(PlanModel.resource_model)
    @plan_ns.expect(PlanModel.register_model, validate=True)
    def post(self):
        """Insert a Plan"""
        data = api.payload
        instance = self.make_instance(PlanModel, data)
        db.session.add(instance)
        db.session.commit()
        return instance, 201


@plan_ns.route('/<ctx_id>')
class Plan(BaseResource):
    @plan_ns.response(404, 'Plan Not Found')
    @plan_ns.marshal_with(PlanModel.resource_model)
    def get(self, ctx_id):
        """Get one Plan"""
        result = PlanModel.query.filter_by().first_or_404


    @plan_ns.marshal_with(PlanModel.resource_model)
    @plan_ns.response(404, 'Plan Not Found')
    @plan_ns.response(204, 'Plan deleted')
    def delete(self, ctx_id):
        """Delete Plan"""
        result = PlanModel.query.filter_by().first_or_404()
        db.session.delete(result)
        db.session.commit()
        return result, 204
        
    @plan_ns.expect(PlanModel.register_model)  
    @plan_ns.marshal_with(PlanModel.resource_model)
    def put(self, ctx_id):
        """Edit Plan""" 
        data = api.payload
        result = PlanModel.query.filter_by()
        result.update(data)
        db.session.commit()
        result = result.first()
        return result, 200