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

def reverse_write(firewall, reference_file, file):
#Ref file is the file WITH ID
#File is the one without ID
    api = connect(**firewall)
    match_tuple = []
    with open(reference_file, 'r') as ref_file:
        #ref_file is the one with the ID value
        with open(file, 'r') as file:

            for ref_item in ref_file:

                for item in file:
                    if re.search(item, ref_item):#Then we try to do a match
                        match_tuple.append(ref_item)
                        print(match_tuple)
                    else:
                        print('no match')
                        continue






            # for item, ref_items in zip(file, ref_file):
            #     #taking the item and converting it back to jason - per line
            #     item = json.loads(item)
            #     ref_items = json.loads(ref_items)
            #     if re.search(r'.*ref_items.items()', item.items()):
            #         print(item['.id'])



        # firewall_path = api.path(path)
        # for config in write_file:
        #     #write it back to json/dict
        #     config = json.loads(config)
        #     for item in firewall_path:
        #         some_new_varible = config | item
        #         print(some_new_varible)
        #         with open('some_test_file', 'a+') as this_file:
        #             this_file.write(item)
        #             this_file.write('\n')