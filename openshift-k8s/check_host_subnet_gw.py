#!/usr/bin/python

import os
import subprocess
import json
import argparse
import getpass

print('Enter API URL:')
api_url = str(raw_input())
print('Enter username:')
api_username = str(raw_input())
api_password = str(getpass.getpass(prompt='Enter password:', stream=None))

ip_for_ping = []

subprocess.call(["oc login ", api_url, "--username=", api_username, "--password=", api_password], shell=True)

output = subprocess.check_output('oc get hostsubnet', shell=True).split()


for index, item in enumerate(output):
    if index < len(output) - 2:
        if output[index+1] == '[]' and output[index+2] == '[]':
            ip_for_ping.append(item[:-4] + '1')


hostnames = []
for index, item in enumerate(output):
    if index == 0:
      continue
    if output[index-1] == 'IPS' and output[index-2] == 'EGRESS':
      hostnames.append(item)
    if index < len(output):
        if output[index-1] == '[]' and item != '[]':
            hostnames.append(item)
# for host, ip in zip(hostnames, ip_for_ping):
#               print host, ip


ping_results = {}
for index, ip in enumerate(ip_for_ping):
   response = os.system("ping -c 1 -w2 " + ip + " > /dev/null 2>&1")
   ping_results[hostnames[index]] = "FAILED" if response else "SUCCESS"

print json.dumps(ping_results, indent=4)
 
with open('ping_results.json', 'w') as f:
   f.write(json.dumps(ping_results, indent=4))