from flask_restplus import Resource, Namespace, fields
from flask_jwt_extended import get_jwt_claims
from app import db
from .base import BaseResource
from .. import api
from ..models.mailboxes import Mailbox as MailboxModel
from ..models.plans import Plan as PlanModel


mailbox_ns = Namespace('Mailboxes', path='/mailboxes')

@mailbox_ns.route('')
class MailboxList(BaseResource):
    @mailbox_ns.marshal_with(MailboxModel.resource_model)
    def get(self):
        """Get the list of Mailboxes"""
        validation = self.validate(MailboxModel)
        return self.get_many(MailboxModel, validation=validation)


    @mailbox_ns.marshal_with(MailboxModel.resource_model)
    @mailbox_ns.expect(MailboxModel.register_model, validate=True)
    def post(self):
        """Insert a Mailbox"""
        validation = self.validate(MailboxModel)
        data = api.payload   
        data.update(validation)
             
        return self.insert_one(MailboxModel, data)


@mailbox_ns.route('/<mailbox_id>')
class Mailbox(BaseResource):
    @mailbox_ns.response(404, 'Mailbox Not Found')
    @mailbox_ns.marshal_with(MailboxModel.resource_model)
    def get(self, mailbox_id):
        """Get one Mailbox"""
        validation = self.validate(MailboxModel)
        return self.get_one(MailboxModel, mailbox_id, validation)


    @mailbox_ns.marshal_with(MailboxModel.resource_model)
    @mailbox_ns.response(404, 'Mailbox Not Found')
    @mailbox_ns.response(204, 'Mailbox deleted')
    def delete(self, mailbox_id):
        """Delete Mailbox"""
        validation = self.validate(MailboxModel)
        return self.delete_one(MailboxModel, mailbox_id, validation)


    @mailbox_ns.expect(MailboxModel.edit_model)  
    @mailbox_ns.marshal_with(MailboxModel.resource_model)
    def put(self, mailbox_id):
        """Edit Mailbox"""
        validation = self.validate(MailboxModel)
        data = api.payload

        return self.update_one(MailboxModel, mailbox_id, data, validation)
        
        