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

    
    def paginate(self, model, validation={}, condition=True):
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

        return result

    def make_instance(self, model, payload):
        instance = model()

        for attr in payload.keys():
            setattr(instance, attr, payload[attr])

        return instance


    def insert_one(self, model, payload):
        instance = model()


        for attr in set(
            set(instance.register_model.keys()) & 
            set(payload.keys())
            ):
            setattr(instance, attr, payload[attr])

        soapid = payload.get('ox_id')
        if soapid:
            instance.ox_id = soapid 
            

        db.session.add(instance)
        db.session.commit()
        return instance, 201


    def delete_one(self, model, id):
        result = self.query_one(model, id)
        db.session.delete(result)
        db.session.commit()
        return result, 200


    def update_one(self, model, id, payload):
        query = {'id':id}
        result = model.query.filter_by(**query)
        result.update(payload)

        db.session.commit()
        result = result.first()
        return result, 200

    
    def query_one(self, model, id):
        query = {'id':id}
        result = model.query.filter_by(**query).first_or_404()
        return result


    def query_many(self, model):
        customer_id = get_jwt_claims()['customer_id']
        permited_contexts = get_jwt_claims()['contexts']
        
        query = eval(self.parse_args('filter', '{}'))
        

        pagination = {
            'per_page': int(self.parse_args('per_page', 10)),
            'page': int(self.parse_args('page', 1))
        }
        
        sort = self.parse_args('sort', 'id')
        order = self.parse_args('order', 'ASC')

        if sort in model.resource_model and order in ['ASC', 'DESC']:
            sorter = "%s %s" %(sort, order)
        else:    
            sorter = ""

        
        result = model.query
        

        if customer_id and model.resource_model.get('customer_id'):
            query = query.update({'customer_id': customer_id})
        if customer_id and model.resource_model.get('context_id'):
            result = result.filter(model.context_id.in_(permited_contexts))


        result = result.filter_by(**query).order_by(text(sorter)).paginate(**pagination)
        return result.items, {'X-Total-Count': result.total}
