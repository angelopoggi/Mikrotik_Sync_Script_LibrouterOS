#####################################
#Write Firewall Function
#By: Angelo Poggi
#
#This is a function that connects to the firewall reads the difference file
#And sends that to the secondary firewall
#####################################


from librouteros import *
import json

def write_firewall(firewall, file,path):
    api = connect(**firewall)
    with open(file, 'r') as write_file:
        firewall_path = api.path(path)
        for line in write_file:
            #need to convert this back to JSON
            config = json.loads(line)
            #write the data to firewall



            firewall_path.add(**config)