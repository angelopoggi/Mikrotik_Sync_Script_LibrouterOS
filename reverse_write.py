#####################################
#Reverse/Remove from Firewall
#By: Angelo Poggi
#
#This removes config not present on firewall one from firewall two
#####################################


from librouteros import *
from librouteros.query import Key
import json
import re

def reverse_write(firewall, file,path):

    api = connect(**firewall)
    with open(file, 'r') as write_file:
        firewall_path = api.path(path)
        for config in write_file:
            #write it back to json/dict
            config = json.loads(config)
            for item in firewall_path:
                some_new_varible = config | item
                print(some_new_varible)
                with open('some_test_file', 'a+') as this_file:
                    this_file.write(item)
                    this_file.write('\n')