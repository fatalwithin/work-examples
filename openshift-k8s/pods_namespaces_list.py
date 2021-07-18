import re
import os
import math
import json
import sys
import argparse

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
filepath_nodes = os.path.join(THIS_FOLDER, r"Cluster_data/small_nodes_prom-ose/nodes")
json_list = {}
pod_list = {}
excluded_pods = {'openshift'}

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

#print (json_list)

for (node, path) in json_list.items():
    pod_list[str(node)] = json_deserialize(str(path))

for (node, pods) in pod_list.items():
    print (node + '\n')
    for pod in pods['items']:
        try:
            # добавляем тут исходные фильтры по выборке
            namespace = pod['metadata']['namespace']
        except KeyError:
            print ("Key Error!")
        else:
            for keyword in excluded_pods:
                if str(keyword) not in str(namespace):
                    print (namespace)
    print("")