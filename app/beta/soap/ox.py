from os import getenv
from dotenv import load_dotenv
from requests import Session
from zeep import Client
from zeep.transports import Transport


load_dotenv()

oxaashost = getenv('OXAASADMHOST')
oxaasadmctx = getenv('OXAASADMCTX', default=getenv('OXAASADMNAME'))

credentials = {
    'login': getenv('OXAASADMNAME'),
    'password': getenv('OXAASADMPASS')
}


session = Session()
session.verify = False
transport = Transport(session=session)

Context = Client('https://' + oxaashost + '/webservices/OXResellerContextService?wsdl', transport=transport)
User = Client('https://' + oxaashost + '/webservices/OXResellerUserService?wsdl', transport=transport)
Group = Client('https://' + oxaashost + '/webservices/OXResellerGroupService?wsdl', transport=transport)
Resource = Client('https://' + oxaashost + '/webservices/OXResellerResourceService?wsdl', transport=transport)
OxaaSService = Client('https://' + oxaashost + '/webservices/OXaaSService?wsdl', transport=transport)