#!/usr/bin/python3

import requests
from requests.auth import HTTPBasicAuth
import pprint
import json
import sys 
import argparse
from getpass import getpass

from defaults import setup


parser = argparse.ArgumentParser()
parser.add_argument("issue_nr", 
	help="display a square of a given number", 
	type=int)
parser.add_argument("-p", "--password", 
	help="Input for user's RM password",
	action="store_true")

args = parser.parse_args()

pp = pprint.PrettyPrinter(indent=3)

# input parameters
defs = setup()
source_base_url = defs['source_base_url']
issue_nr = args.issue_nr #172245
target_base_url = defs['target_base_url']
target_project_id = defs['target_project_id']
additional_custom_fields = defs['additional_custom_fields']
username = defs['username']
password = defs['password']
if args.password:
	password = getpass('Password:')


# setup RM connections and authentication
source_url = source_base_url + '/issues/' + str(issue_nr) + '.json'
target_url = target_base_url + '/issues.json'
rm_auth = HTTPBasicAuth(username, password)


# Get the issue as json
response = requests.get(source_url, auth=rm_auth)
if not response.ok:
	sys.exit('Cannot get the issue: ' + response.reason)
rm_issue = response.json()['issue']

### DEBUG ###
# print( 'SOURCE ISSUE:' )
# pp.pprint( { 'issue': rm_issue } )

# copy fields
new_issue = dict( 
	project_id = target_project_id,  
	tracker_id = rm_issue['tracker']['id'],
	priority_id = rm_issue['priority']['id'],
	subject = rm_issue['subject'],
	description = rm_issue['description'] + '\nReferenced issue: ' + source_url[:-5], # remove '.json'
	custom_fields = rm_issue['custom_fields']
)
new_issue['custom_fields'].extend(additional_custom_fields)

### DEBUG ###
# print( 'NEW ISSUE:' )
# print( target_url )
# pp.pprint( { 'issue': new_issue } )


# insert to the other RM
resp_create = requests.post(target_url, data=json.dumps({ 'issue': new_issue }), headers={'content-type': 'application/json'}, auth=rm_auth)


# echo target URL
if resp_create.ok:
	print( target_base_url + '/issues/' + str(resp_create.json()['issue']['id']) )
else:
	print( 'RESPONSE:' )
	print( resp_create.headers )
	print( resp_create.text )