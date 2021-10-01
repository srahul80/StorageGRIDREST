import json, os, sys
import requests

from colorama import init
#from colorama import Fore, Back, Style

init()

 
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
sg_endpoint="https://dc1-adm1.demo.netapp.com/api/v3"


gmi_user="root"
gmi_pwd="Netapp1!"


def sg_info(sg_endpoint, auth_token):
	return requests.get(sg_endpoint,headers={'accept': 'application/json', 'authorization': 'Bearer {}'.format(auth_token)},verify=False).json()['data']

auth_body = {
        "username": 	gmi_user,
        "password": 	gmi_pwd
      	}

auth_token = requests.post(sg_endpoint + "/authorize",data=json.dumps(auth_body),  headers={'Content-Type':'application/json','accept':'application/json'},verify=False).json()['data'] 

sg_version = sg_info(sg_endpoint+'/grid/config/product-version', auth_token)
print(sg_version)
sg_topology = sg_info(sg_endpoint+ '/grid/health/topology', auth_token)

print(sg_topology['name'])

for site in sg_topology['children']:
	print('\033[33m'  +  'Data Center: {}'.format(site['name']))
	for sgnode in site['children']:	
		print('\033[39m'+ ' Node Name: {0:20}  	Type: {1}'.format(sgnode['name'], sgnode['type']),  '\033[33m' + 'State: {}'.format(sgnode['state']))
	print('*************************************************************************\n')


sg_alerts= sg_info(sg_endpoint+ '/grid/alerts', auth_token)
print(sg_alerts)