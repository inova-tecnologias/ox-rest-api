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
        return self.get_many(PlanModel)



    @plan_ns.marshal_with(PlanModel.resource_model)
    @plan_ns.expect(PlanModel.register_model, validate=True)
    def post(self):
        """Insert a Plan"""
        validation = self.validate(PlanModel, roles=['admin'])
        data = api.payload   
        data.update(validation)
             
        return self.insert_one(PlanModel, data)



@plan_ns.route('/<plan_id>')
class Plan(BaseResource):
    @plan_ns.response(404, 'Plan Not Found')
    @plan_ns.marshal_with(PlanModel.resource_model)
    def get(self, plan_id):
        """Get one Plan"""
        return self.get_one(PlanModel, plan_id)



    @plan_ns.marshal_with(PlanModel.resource_model)
    @plan_ns.response(404, 'Plan Not Found')
    @plan_ns.response(204, 'Plan deleted')
    def delete(self, plan_id):
        """Delete Plan"""
        validation = self.validate(PlanModel, roles=['admin'])
        return self.delete_one(PlanModel, plan_id, validation)
        
    @plan_ns.expect(PlanModel.register_model)  
    @plan_ns.marshal_with(PlanModel.resource_model)
    def put(self, plan_id):
        """Edit Plan""" 
        validation = self.validate(PlanModel, roles=['admin'])
        data = api.payload
        return self.update_one(PlanModel, plan_id, data, validation)