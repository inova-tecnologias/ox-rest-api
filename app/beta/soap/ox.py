from os import getenv
from dotenv import load_dotenv
from requests import Session
from zeep import Client

def removePort80(client):
    client.service._binding_options['address'] = client.service._binding_options['address'].replace(":80","")
    return client


load_dotenv()

oxaashost = getenv('OXAASADMHOST')
oxaasadmctx = getenv('OXAASADMCTX', default=getenv('OXAASADMNAME'))

credentials = {
    'login': getenv('OXAASADMNAME'),
    'password': getenv('OXAASADMPASS')
}


Context = removePort80(
    Client('https://' + oxaashost + '/webservices/OXResellerContextService?wsdl')
)

User = removePort80(
    Client('https://' + oxaashost + '/webservices/OXResellerUserService?wsdl')
)
Group = removePort80(
    Client('https://' + oxaashost + '/webservices/OXResellerGroupService?wsdl')
)
Resource = removePort80(
    Client('https://' + oxaashost + '/webservices/OXResellerResourceService?wsdl')
)
OxaaSService = removePort80(
    Client('https://' + oxaashost + '/webservices/OXaaSService?wsdl'))