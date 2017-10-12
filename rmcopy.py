#!/usr/bin/python3

import requests
from requests.auth import HTTPBasicAuth
import pprint
import json

from defaults import setup

pp = pprint.PrettyPrinter(indent=3)

# input parameters
defs = setup()
source_base_url = defs['source_base_url']
issue_nr = 172245
target_base_url = defs['target_base_url']
target_project_id = defs['target_project_id']
username = defs['username']
password = defs['password']

# setup RM connections and authentication
source_url = source_base_url + '/issues/' + str(issue_nr) + '.json'
target_url = target_base_url + '/issues.json'
rm_auth = HTTPBasicAuth(username, password)


# Get the issue as json
response = requests.get(source_url, auth=rm_auth)
rm_issue = response.json()['issue']


# copy fields
new_issue = dict( 
	project_id = target_project_id,  
	tracker_id = rm_issue['tracker']['id'],
	priority_id = rm_issue['priority']['id'],
	subject = rm_issue['subject'],
	description = rm_issue['description'],
	custom_fields = rm_issue['custom_fields']
)


# insert to the other RM
print( 'NEW ISSUE:' )
print( target_url )
#pp.pprint( { 'issue': new_issue } )
print( json.dumps({ 'issue': new_issue }) )

resp_create = requests.post(target_url, data=json.dumps({ 'issue': new_issue }), headers={'content-type': 'application/json'}, auth=rm_auth)

# echo target URL
print( 'RESPONSE:' )
print( resp_create.headers )
print( resp_create.text )