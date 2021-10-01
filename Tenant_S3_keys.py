import json, os, sys
import requests

from colorama import init
#from colorama import Fore, Back, Style

init()


 
sg_endpoint="https://dc1-adm1.demo.netapp.com/api/v3"


gmi_user="root"
gmi_pwd="netapp01"
taccountid="01404112463146563881"

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
def sg_info(sg_endpoint, auth_token):
	return requests.get(sg_endpoint,headers={'accept': 'application/json', 'authorization': 'Bearer {}'.format(auth_token)},verify=False).json()['data']

auth_body = {
		"accountId":  taccountid , 
        "username": 	gmi_user,
        "password": 	gmi_pwd
      	}


auth_token = requests.post(sg_endpoint + "/authorize",data=json.dumps(auth_body),  headers={'Content-Type':'application/json','accept':'application/json'},verify=False).json()['data'] 
print (auth_token)

print('###################################################\n')
print('Connected to Tenant:', taccountid, ' token ', auth_token)
print('###################################################\n')
sg_tenants_keys = sg_info(sg_endpoint+ '/org/users/current-user/s3-access-keys', auth_token)

for s3keys in sg_tenants_keys:
	print('S3 Access key: ',s3keys['id'])
	print('Expiry :', s3keys['expires'])
	print ('################################')
