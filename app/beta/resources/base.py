from flask_restplus import Resource
from flask import request
from sqlalchemy import text
from flask_jwt_extended import (
    jwt_required, get_jwt_claims
)

from app import db

class BaseResource(Resource):
    method_decorators = [jwt_required]


    def parse_args(self, arg, default):
        try:
            return request.args.to_dict()[arg]
        except KeyError:
            return default    


    def validate(self, model, roles=[
                                'admin',
                                'reseller',
                                'customer']):
        claims = get_jwt_claims()
        if claims['role'] not in roles:
            raise Exception("Role not permitted")
        
        validation = {}
        
        if bool(hasattr(model, 'reseller_id') and claims['reseller_id']):
            validation.update({'reseller_id': claims['reseller_id']})        
        if bool(hasattr(model, 'customer_id') and claims['customer_id']):
            validation.update({'customer_id': claims['customer_id']})

        return validation


    def get_many(self, model, validation={}, condition=True):
        pagination = {
            'per_page': int(self.parse_args('per_page', 10)),
            'page': int(self.parse_args('page', 1))
        }

        query = dict(eval(self.parse_args('filter', '{}')))
        query.pop('q', None) # TODO: Index Search using 'q' attr
        query.pop('id', None) # TODO: Workaround for frontend quering id list
        query.update(validation)

        sort = self.parse_args('sort', 'id')
        order = self.parse_args('order', 'ASC')

        if sort in model.resource_model and order in ['ASC', 'DESC']:
            sorter = "%s %s" %(sort, order)
        else:    
            sorter = ""

        result = model.query.filter(condition)
        result = result.filter_by(**query)
        result = result.order_by(text(sorter))
        result = result.paginate(**pagination)

        return result.items, {'X-Total-Count': result.total}

        
    def get_one(self, model, id, validation={}, condition=True):
        query = {'id':id}
        query.update(validation)
        result = model.query.filter(condition)
        result = result.filter_by(**query).first_or_404()
        return result


    def make_instance(self, model, payload):
        instance = model()
        
        for attr in set(
            set(instance.register_model.keys()) & 
            set(payload.keys())
            ):
            setattr(instance, attr, payload[attr])   
        
        return instance


    def insert_one(self, model, payload):
        instance = self.make_instance(model, payload)         

        db.session.add(instance)
        db.session.commit()
        return instance, 201


    def delete_one(self, model, id, validation={}):
        result = self.get_one(model, id, validation=validation)
        db.session.delete(result)
        db.session.commit()
        return result, 200


    def update_one(self, model, id, payload, validation={}):
        query = {'id': id}
        query.update(validation)
        payload.update(validation)
        result = model.query.filter_by(**query)
        result.update(payload)

        db.session.commit()
        result = result.first()
        return result, 200


    def delete_many(self):
        '''TODO'''
        pass


    def update_many(self):
        '''TODO'''
        pass

    

