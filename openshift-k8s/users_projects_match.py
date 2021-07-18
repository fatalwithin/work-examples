import re
import os
import math
import json
import sys
import argparse

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
filepath_nodes = os.path.join(THIS_FOLDER, r"Cluster_data/project_users")
json_list = {}

project_list = {}

unique_users_list = []

def json_deserialize(filepath):
    with open(filepath, "r") as read_file:
        data = read_file.read()
        return json.loads(data)

for current_dir, dirs, files in os.walk(filepath_nodes):
    dirs.sort()
    files.sort()
    for file in files:
        if (str(file).endswith("json")):
            json_list[str(file)[:-5]] = (filepath_nodes + "/" + str(file))
            # break

for (project, path) in json_list.items():
    project_list[str(project)] = json_deserialize(str(path))

for (project, users) in project_list.items():
    # print (project + '\n')
    # project_list[str(project)] = project_set[pod['metadata']['namespace']]

    for user in users['items']:
        try:
            role = user['roleRef']['name']
            usernames = user['userNames']
        except KeyError:
            pass
        else:
            if str(role) == "admin-as":
                for username in usernames:
                    if (str(username) + "@ca.sbrf.ru") not in unique_users_list:
                        unique_users_list.append(str(username) + "@ca.sbrf.ru")
    # print ('')
for user in unique_users_list:
    print (user)