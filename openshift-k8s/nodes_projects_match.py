import re
import os
import math
import json
import sys
import argparse

# Create the parser
my_parser = argparse.ArgumentParser(description='Check openshift nodes with needed replacement')

# Add the arguments
my_parser.add_argument('CPU',
                       metavar='cpu',
                       type=int,
                       help='Bottom range of vCPU on nodes. e.g. cpu=8 means all nodes with 8 or lesss vCPU need replacement')

my_parser.add_argument('RAM',
                       metavar='ram',
                       type=int,
                       help='Bottom range of RAM on nodes. e.g. ram=32 means all nodes with 32GB or less RAM need replacement')

my_parser.add_argument('--tainted',
                       action = "store_true",
                       dest='tainted',
                       default = False,
                       help='If set to true - show tainted nodes (with pinned projects). If set to false - show nodes free to replace')

my_parser.add_argument('--show_projects',
                       action = "store_true",
                       dest='show_projects',
                       default = False,
                       help='If set to true - show list of pinned projects for each tainted nodes')

my_parser.add_argument('--show_deployments',
                       action = "store_true",
                       dest='show_deployments',
                       default = False,
                       help='If set to true - show list of pinned deployments for each tainted nodes')

my_parser.add_argument('--show_pods',
                       action = "store_true",
                       dest='show_pods',
                       default = False,
                       help='If set to true - show list of pinned pods for each tainted nodes')                  

# Execute the parse_args() method
args = my_parser.parse_args()

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
filepath_nodes = os.path.join(THIS_FOLDER, r"Cluster_data/Alpha-master-PROM/alpha_prom_nodes.json")
filepath_projects = os.path.join(THIS_FOLDER, r"Cluster_data/Alpha-master-PROM/alpha_prom_projects.json")
filepath_deployments = os.path.join(THIS_FOLDER, r"Cluster_data/Alpha-master-PROM/alpha-prom-deployments.json")
filepath_pods = os.path.join(THIS_FOLDER, r"Cluster_data/Alpha-master-PROM/alpha_prom_pods.json")

def json_deserialize(filepath):
    with open(filepath, "r") as read_file:
        data = read_file.read()
        return json.loads(data)

json_nodes = json_deserialize(filepath_nodes)
json_projects = json_deserialize(filepath_projects)
json_deployments = json_deserialize(filepath_deployments)
json_pods = json_deserialize(filepath_pods)


# сериализируем данные по нодам, фильтруя по параметрам и кладем результат в новый словарь
def node_serialize(json_set):
    node_set = []
    for node in json_set['items']:
        try:
            # добавляем тут исходные фильтры по выборке
            node['metadata']['labels']['node-role.kubernetes.io/compute'] == "true"
            node['metadata']['labels']['region'] == "prom"
            node['metadata']['labels']['shared'] == "true"
        except:
            pass
        else:
            if (int(node['status']['capacity']['cpu']) <= args.CPU
            and math.ceil(int(node['status']['capacity']['memory'][:-2])/1024/1024) <= args.RAM
            and node['metadata']['labels']['region'] == "prom" 
            and node['metadata']['labels']['shared'] == "true"
            and node['metadata']['labels']['node-role.kubernetes.io/compute'] == "true"
            ):
                node_set.append(node)
                # print (node['metadata']['name'])
                # print (node['metadata']['labels'])
                # print (node['status']['capacity']['cpu'])
    return node_set


# сериализируем данные по проектам, делаем из списка селекторов словарь и кладем результат в пустой новый словарь
def find_project(json_set, labels_set):
    project_set = []
    for project in json_set['items']:
        try:
            selectors = project['metadata']['annotations']['openshift.io/node-selector']
        except KeyError:
            pass
        else:
            if (selectors.__len__() > 0):
                selectors_dict = dict(selector.split('=') for selector in selectors.split(','))

                # фильтруем дополнительно по лейблам которые не нужны типа регион, shared
                for excluded_label in labels_set:
                    selectors_dict.pop(excluded_label, None)

                if (selectors_dict.__len__() > 0):
                    project['sorted_labels'] = selectors_dict
                    project_set.append(project)
                # print ("<<< Project: " + project['metadata']['name'] + " >>>")
                # print (project['sorted_labels'])
    return project_set
# print ("set of projects:")
# print (set_projects)


# сериализируем данные по деплойментам, делаем из списка селекторов словарь и кладем результат в пустой новый словарь
def find_deployment(json_set, labels_set):
    deployment_set = []
    for deployment in json_set['items']:
        try:
            selectors = deployment['spec']['selector']['matchLabels']
        except KeyError:
            pass
        else:
            if (selectors.__len__() > 0):
                selectors_dict = dict(selectors.items())

                # фильтруем дополнительно по лейблам которые не нужны типа регион, shared
                for excluded_label in labels_set:
                    selectors_dict.pop(excluded_label, None)

                if (selectors_dict.__len__() > 0):
                    deployment['sorted_labels'] = selectors_dict
                    deployment_set.append(deployment)
                # print ("<<< Project: " + project['metadata']['name'] + " >>>")
                # print (project['sorted_labels'])
                # for deployment in deployment_set:
                #     print(deployment['metadata']['name'])
                #     print(deployment['sorted_labels'])
    return deployment_set

# сериализируем данные по подам, делаем из списка селекторов словарь и кладем результат в пустой новый словарь
def find_pod(json_set, labels_set):
    pod_set = []
    for pod in json_set['items']:
        try:
            selectors = pod['spec']['nodeSelector']
        except KeyError:
            pass
        else:
            if (selectors.__len__() > 0):
                selectors_dict = dict(selectors.items())

                # фильтруем дополнительно по лейблам которые не нужны типа регион, shared
                for excluded_label in labels_set:
                    selectors_dict.pop(excluded_label, None)

                if (selectors_dict.__len__() > 0):
                    pod['sorted_labels'] = selectors_dict
                    pod_set.append(pod)
    return pod_set


# считаем пересечения нод по объектам
def node_object_intersect(node_set, project_set, deployment_set, pod_set):
    set_result_nodes = []
    for node in node_set:
        tainted_node = 0

        if (args.show_projects == True):
            for project in project_set:
                
                intersect_labels = dict(node['metadata']['labels'].items() & project['sorted_labels'].items())
                # print ("Intersect labels:")
                # print (intersect_labels)
                if (intersect_labels.__len__() > 0):
                    tainted_node = 1

        if (args.show_deployments == True):
            for deployment in deployment_set:
                
                intersect_labels = dict(node['metadata']['labels'].items() & deployment['sorted_labels'].items())
                # print ("Intersect labels:")
                # print (intersect_labels)
                if (intersect_labels.__len__() > 0):
                    tainted_node = 1

        if (args.show_pods == True):
            for pod in pod_set:

                intersect_labels = dict(node['metadata']['labels'].items() & pod['sorted_labels'].items())
                # print ("Intersect labels:")
                # print (intersect_labels)
                if (intersect_labels.__len__() > 0):
                    tainted_node = 1
                
    # добавляем ноды с закрепленными проектами (кастомными селекторами)
        if (tainted_node == 1 and args.tainted == True):
            set_result_nodes.append(node)

            if (args.show_projects == True):
                print ("<<< Node: " + node['metadata']['name'] + " >>>")
                for project in project_set:
                    intersect_labels = dict(node['metadata']['labels'].items() & project['sorted_labels'].items())
                    if (intersect_labels.__len__() > 0):
                        print ("Project: " + project['metadata']['name'])
                        print ("Labels intersection:")
                        for (k, v) in intersect_labels.items(): 
                            print (k + ": " + v)
            
            if (args.show_deployments == True):
                print ("<<< Node: " + node['metadata']['name'] + " >>>")
                for deployment in deployment_set:

                    intersect_labels = dict(node['metadata']['labels'].items() & deployment['sorted_labels'].items())
                    if (intersect_labels.__len__() > 0):
                        print ("Deployment: " + deployment['metadata']['name'])
                        print ("Labels intersection:")
                        for (k, v) in intersect_labels.items(): 
                            print (k + ": " + v)

            if (args.show_pods == True):
                print ("<<< Node: " + node['metadata']['name'] + " >>>")
                for pod in pod_set:

                    intersect_labels = dict(node['metadata']['labels'].items() & pod['sorted_labels'].items())
                    if (intersect_labels.__len__() > 0):
                        print ("Pod: " + pod['metadata']['name'])
                        print ("of Namespace: " + pod['metadata']['namespace'])
                        print ("Labels intersection:")
                        for (k, v) in intersect_labels.items(): 
                            print (k + ": " + v)
            
        if (tainted_node == 0 and args.tainted == False):
            set_result_nodes.append(node)
    return set_result_nodes

# ищем поды на выбранных нодах
def find_projects_by_pods(node_set, excluded_pod_list):
    found_pod_list = []
    found_project_list = []

    # заполняем наборы с подами и проектами без фильтрации
    project_set = find_project(json_projects, {})
    pod_set = find_pod(json_pods, {})

    for node in node_set:    
        for pod in pod_set:
            #print (pod['metadata']['name'], pod['spec']['nodeName'])
            try:
                if (pod['spec']['nodeName'] == node['metadata']['name']):
                    found_pod_list.append(pod)
            except KeyError:
                pass

    for pod in found_pod_list:
        # print (pod['metadata']['name'])
        for project in project_set:
            if (project['metadata']['name'] == pod['metadata']['namespace']
            and not project in found_project_list):
                found_project_list.append(project)
    return found_project_list



excluded_labels = {'zone', 'region', 'shared'}
excluded_pods = {'openshift'}

set_nodes = node_serialize(json_nodes)
set_projects = find_project(json_projects, excluded_labels)
set_deployments = find_deployment(json_deployments, {'app'})
set_pods = find_pod(json_pods, {'region', 'shared', 'zone', 'logging-infra-fluentd', 'beta.kubernetes.io/os'})

set_result_nodes = node_object_intersect(set_nodes, set_projects, set_deployments, set_pods)

# find_pod(set_pods, json_pods, {'region', 'shared', 'zone', 'logging-infra-fluentd', 'beta.kubernetes.io/os'})

# выводим ноды с закрепленными проектами
for node in set_result_nodes:
    print (node['metadata']['name'])

print (set_result_nodes.__len__())

# ищем проекты, поды которых сидят на наших найденных нодах:
found_project_list = find_projects_by_pods(set_nodes, excluded_pods)

print ("Found projects: \n")
for project in found_project_list:
    print (project['metadata']['name'])
