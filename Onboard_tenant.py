
import json, os, sys
import requests

from colorama import init
#from colorama import Fore, Back, Style

init()


 
sg_endpoint="https://dc1-adm1.demo.netapp.com/api/v3"


gmi_user="root"
gmi_pwd="Netapp1!"


from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
def sg_info(sg_endpoint, auth_token):
	return requests.get(sg_endpoint,headers={'accept': 'application/json', 'authorization': 'Bearer {}'.format(auth_token)},verify=False).json()['data']

auth_body = {
        "username": 	gmi_user,
        "password": 	gmi_pwd
      	}


auth_token = requests.post(sg_endpoint + "/authorize",data=json.dumps(auth_body),  headers={'Content-Type':'application/json','accept':'application/json'},verify=False).json()['data'] 

sg_version = sg_info(sg_endpoint+'/grid/config/product-version', auth_token)
print('###################################################\n')
print('Connected to GRID:', sg_version)
print('###################################################\n')
sg_tenants = sg_info(sg_endpoint+ '/grid/accounts', auth_token)

def sg_post(sg_endpoint, body, auth_token):
	return requests.post(sg_endpoint,data=json.dumps(body), headers={'accept': 'application/json', 'authorization': 'Bearer {}'.format(auth_token)},verify=False).json()['data']


sgtenant="""{
  "name": "RESTAPI_demo1",
  "capabilities": [
    "management",
    "s3"
  ],
  "policy": {
    "useAccountIdentitySource": false,
    "allowPlatformServices": true,
    "quotaObjectBytes": 100000000000
  },
  "password": "Netapp123",
  "grantRootAccessToGroup": "federated-group/sgtenantadmins"
}
"""

tenantjson= json.loads(sgtenant)
print(tenantjson)


sg_tenants_creation = sg_post(sg_endpoint+ '/grid/accounts', tenantjson, auth_token)

print('OUTput########',sg_tenants_creation)
