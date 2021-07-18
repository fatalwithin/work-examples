import re
import os
import math
#import pandas


rx_dict = {
    'node_name': re.compile(r'Name: (?P<node_name>.*)\n'),
    'node_roles': re.compile(r'Roles: (?P<node_roles>.*)\n'),
    'node_namespace': re.compile(r'                    namespace=(?P<node_namespace>.*)\n'),
    'node_internal_ip': re.compile(r'  InternalIP: (?P<node_internal_ip>.*)\n'),
    'node_hostname': re.compile(r'  Hostname: (?P<node_hostname>.*)\n'),
    'node_capacity': re.compile(r'Capacity:\n'),
    'node_allocatable': re.compile(r'Allocatable:\n'),
    'node_cpu': re.compile(r' cpu: (?P<node_cpu>.*)\n'),
    'node_memory': re.compile(r' memory: (?P<node_memory>.*)\n'),
    'node_region': re.compile(r' region=(?P<node_region>.*)\n'),
    'node_zone': re.compile(r' zone=(?P<node_zone>.*)\n')
}

def _parse_line(line):
    """

    do a regex search against all defined regexes and return key and match of first matching regex

    """
    for key, rx in rx_dict.items():
        match = rx.search(line)
        if (match):
            return key, match

    # if no matches - return None
    return None, None


THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(THIS_FOLDER, r"Cluster_data/Alpha-master-PROM/alpha_prom_nodes_full.txt")

#filepath = r"~/Desktop/Sigma-Istio-DEV/cluster_nodes_full.txt"


def parse_file(filepath):
    """
    data : pd.DataFrame - parsed data

    """

    data = [] # create an empty list

    node = ""
    roles = ""
    namespace = ""
    internal_ip = ""
    hostname = ""
    capacity = ""
    allocatable = ""
    cpu = "100"
    cpu_fact = 0
    memory = ""
    region = ""
    zone = ""
    group = 0
    new_group = 0
    flag = 0

    with open(filepath, 'r', encoding='utf-8') as file_object:
        line = file_object.readline()

        while line:
            key, match = _parse_line(line)

            if key == 'node_name':
                # нашли ноду, проваливаемся дальше
                
                if (flag == 1 and new_group == 1 and region == "prom" and "compute" in roles and int(memory) < 25):
                    group += 1
                    data.append(str(group) + "\n" + node + "\n" + roles + "\n" + namespace + "\n" + internal_ip + "\n" +  hostname + "\n" +  capacity + "\n" +  allocatable + "\n" +  region + "\n" +  zone + "\n" +  "Node cpu:" + str(cpu_fact) + "\n" +  "Node memory:" + memory + "GB" + "\n")
                    flag = 0
                    node = ""
                    roles = ""
                    namespace = ""
                    internal_ip = ""
                    hostname = ""
                    capacity = ""
                    allocatable = ""
                    cpu = "100"
                    cpu_fact = 0
                    memory = ""
                    region = ""
                    zone = ""

                
                new_group = 1
                node = match.group('node_name')
                node = "Node name:" + str(node).strip()
                #data.append(node)
                # print(node)

            if (new_group == 1):
                if key == 'node_roles':
                    roles = match.group('node_roles')
                    roles = "Node roles:" + str(roles).strip()
                    #data.append(roles)
                
                if key == 'node_namespace':
                    namespace = match.group('node_namespace')
                    namespace = "Node namespace:" + str(namespace).strip()

                if key == 'node_internal_ip':
                    internal_ip = match.group('node_internal_ip')
                    internal_ip = "Internal IP:" + str(internal_ip).strip()
                    #data.append(internal_ip)

                if key == 'node_hostname':
                    hostname = match.group('node_hostname')
                    hostname = "Node hostname:" + str(hostname).strip()
                    #data.append(hostname)

                if key == 'node_capacity':
                    capacity = match.string
                    capacity = str(capacity).strip()
                    #data.append(capacity)

                if key == 'node_allocatable':
                    allocatable = match.string
                    allocatable = str(allocatable).strip()
                    #data.append(allocatable)
                
                if key == 'node_region':
                    region = match.group('node_region')
                    region = str(region).strip()
                    #data.append(region)

                if key == 'node_zone':
                    zone = match.group('node_zone')
                    zone = "Node zone:" + str(zone).strip()
                    #data.append(zone)

                if key == 'node_cpu':
                    cpu = match.group('node_cpu')
                    cpu = str(cpu).strip()
                    #data.append(cpu)

                if key == 'node_memory':
                    mem = match.group('node_memory')
                    mem = str(mem).strip()
                    if mem[len(mem)-2:len(mem)] == "Ki":
                        memory = str(math.ceil(int(mem[:-2])/1024/1024))
                    #data.append(memory)

                try: 
                    (int(cpu, base=0))
                except (ValueError):
                    i = 0
                else:
                    if int(cpu, base=0) < 8:
                        flag = 1
                        cpu_fact = int(cpu, base=0)
                    
                    # append dictionary to data list
            
                  

            line = file_object.readline()

        # # create a Dataframe object from list of dicts
        # data = pandas.DataFrame(data)
        # data.set_index(['Node'], inplace=True)
        # data = data.groupby(level=data.index.names).first()
    return data





data = parse_file(filepath)
for line in data:
    print(line)



