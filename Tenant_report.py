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

for tenant in sg_tenants:
	print('\033[33m'  +  'Tenant Name: {}'.format(tenant['name']))
	print('\033[33m' +  'ID: {}'.format(tenant['id']))
	print('\033[39m'  +  'Capabilities: {}'.format(tenant['capabilities']))
	print('\033[39m'  +  'Policy: {}'.format('policy'))
	tenantid=tenant['id']
	prometheus_query1="storagegrid_tenant_usage_data_bytes"
	prometheus_query2='tenant_id="{}"'.format(tenantid)
	print(prometheus_query2)
	prometheus_query=prometheus_query1+'{'+prometheus_query2 +'}'
	sg_tenants_space = sg_info(sg_endpoint+ '/grid/metric-query?query='+ prometheus_query, auth_token)
	usage=sg_tenants_space.get('result')
	print('Space consumed(MB) ->', int(usage[0]['value'][1])/1000/1000)
	for mypolicy in tenant['policy']:
		print(mypolicy, '->', tenant['policy'][mypolicy])
	
	print('*************************************************************************\n')



