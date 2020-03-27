from flask import Blueprint
from flask_restplus import Api

version = __name__.split(".")[-1]
authorizations = {
    'jwt': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'**, where JWT is the token"
    }
}


blueprint = Blueprint(version + __name__, __name__)
api = Api(blueprint,
               ordered=True,
               title="OX REST API",
               version=version,
               description='',
               security='jwt',
               authorizations=authorizations)

from .resources.auth import auth_ns
from .resources.users import user_ns
from .resources.costumers import costumer_ns
from .resources.contexts import ctx_ns
from .resources.mailboxes import mbx_ns
from .resources.groups import group_ns


api.add_namespace(auth_ns)
api.add_namespace(user_ns)
api.add_namespace(costumer_ns)
api.add_namespace(ctx_ns)
api.add_namespace(mbx_ns)
api.add_namespace(group_ns)

