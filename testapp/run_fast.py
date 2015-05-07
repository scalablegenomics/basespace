#!/usr/bin/python
import os
import fnmatch 
import sys
import json
import subprocess

subprocess.call("cp /data/input/AppSession.json /data/output")
jsonfile = open('/data/input/AppSession.json')
jsonObject = json.load(jsonfile)
numberOfPropertyItems = len( jsonObject['Properties']['Items'])

for index in range(numberOfPropertyItems):
	if jsonObject['Properties']['Items'][index]['Name'] == 'Input.sample-id':
        	parameter = jsonObject['Properties']['Items'][index]['Content']
