
##############################
#Mikrotik Sync Script
#by: Angelo Poggi
#Angelo.poggi@webair.com
#
#This Script uses Librouter OS to read primary firewall
#and send the difference to the secondary firewall
#
#################################

#Import all of Librouter
from librouteros import *

import json

import email_report




#to be removed
logo = '''
|￣￣￣￣￣￣￣ |  
|   MIKROTIK   |
|  SYNC SCRIPT |
|  **WEBAIR**  |
| By: Angelo P.| 
|＿＿＿＿＿ _＿_|
(\__/) || 
(•ㅅ•) || 
/ 　 づ  '''

print('=-=' *20)
print(logo)
print('=-=' *20)

#Creating an UNECRYPTED CONNECTION to the firewalls
#should consider renaming this, as it does more than just connect

#address-list - GOOD
#Firewall rules - Good
#NAT rules - Good
#VPN Info (Peers/policies)




#todo: add error handling if firewalls are not online!
#todo: rename this function to something more fitting on what it is doing
def firewall_connect(primary_firewall, Secondary_firewall):
    firewall_one = connect(**primary_firewall)
    firewall_two = connect(**secondary_firewall)

    try:
        #this will return a dictionary
        firewall_one_address_list = firewall_one.path('/ip/firewall/address-list')
        firewall_two_address_list = firewall_two.path('/ip/firewall/address-list')

        #firewall rules
        firewall_one_filter = firewall_one.path('/ip/firewall/filter')
        firewall_two_filter = firewall_two.path ('/ip/firewall/filter')

        #NAT Rules
        firewall_one_nat = firewall_one.path('/ip/firewall/nat')
        firewall_two_nat = firewall_two.path('/ip/firewall/nat')

        #IPSec PEER
        firewall_one_ipsecpeer = firewall_one.path('/ip/ipsec/peer')
        firewall_two_ipsecpeer = firewall_two.path('/ip/ipsec/peer')

        #IPSec Policy
        firewall_one_ipsecpolicy = firewall_one.path('/ip/ipsec/policy')
        firewall_two_ipsecpolicy = firewall_two.path('/ip/ipsec/policy')

        #IPSec Proposal
        firewall_one_ipsecproposal = firewall_one.path('/ip/ipsec/proposal')
        firewall_two_ipsecproposal = firewall_two.path('/ip/ipsec/proposal')
    except:
        print('Firewall May be offline!')




    #todo: more testing with Key valu pairs, feel as though I am removing to many?
    #todo: create a function that does all this, outside of firewall_connect (?)
    ################################################
    # Filter Rules
    ################################################
    with open('firewall_one_filter.txt','w+') as fw_filter:
        for item in firewall_one_filter:
            item.pop ( '.id' )
            item.pop('bytes')
            item.pop ( 'packets' )
            item.pop ( 'dynamic' )
            item.pop('invalid')
            json.dump(item, fw_filter)
            fw_filter.write('\n')

    with open ( 'firewall_two_filter.txt' , 'w+' ) as fw2_filter :
        for item in firewall_two_filter :
            item.pop ( '.id' )
            item.pop ( 'bytes' )
            item.pop('packets')
            item.pop ( 'invalid' )
            json.dump ( item , fw2_filter )
            fw2_filter.write ( '\n' )

    ################################################
    # NAT
    ################################################

    with open('firewall_one_nat.txt','w+') as fw_nat:
        for item in firewall_one_nat:
            item.pop ( '.id' )
            item.pop('bytes')
            item.pop('packets')
            item.pop ( 'invalid' )
            item.pop('dynamic')
            json.dump(item, fw_nat)
            fw_nat.write('\n')


    with open ( 'firewall_two_nat.txt' , 'w+' ) as fw2_nat :
        for item in firewall_two_nat :
            item.pop ( '.id' )
            item.pop('bytes')
            item.pop('packets')
            item.pop ( 'invalid' )
            item.pop('dynamic')
            json.dump ( item , fw2_nat )
            fw2_nat.write ( '\n' )



    ################################################
    # ADDRESS LISTS
    ################################################
    with open('firewall_one_address_list.txt', 'w+') as fw_file:
        for item in firewall_one_address_list:
            item.pop('creation-time')
            item.pop('.id')
            item.pop('disabled')
            item.pop('dynamic')
            json.dump(item, fw_file)
            fw_file.write('\n')

    with open('firewall_two_address_list.txt', 'w+') as fw2_file:
        for item in firewall_two_address_list:
            item.pop('creation-time')
            item.pop('.id')
            item.pop ( 'disabled' )
            item.pop ( 'dynamic' )
            json.dump(item, fw2_file)
            fw2_file.write('\n')

    ################################################
    # IPSEC STUFF
    ################################################
    #PEER
    with open('firewall_one_ipsec_peer.txt', 'w+') as fw_file:
        for item in firewall_one_ipsecpeer:
        #     item.pop('creation-time')
        #     item.pop('.id')
        #     item.pop('disabled')
        #     item.pop('dynamic')
            json.dump(item, fw_file)
            fw_file.write('\n')

    with open('firewall_two_ipsec_peer.txt', 'w+') as fw2_file:
        for item in firewall_two_ipsecpeer:
            # item.pop('creation-time')
            # item.pop('.id')
            # item.pop ( 'disabled' )
            # item.pop ( 'dynamic' )
            json.dump(item, fw2_file)
            fw2_file.write('\n')

        #POLICY
        with open ( 'firewall_one_ipsec_policy.txt' , 'w+' ) as fw_file :
            for item in firewall_one_ipsecpolicy :
                # item.pop ( 'creation-time' )
                # item.pop ( '.id' )
                # item.pop ( 'disabled' )
                # item.pop ( 'dynamic' )
                json.dump ( item , fw_file )
                fw_file.write ( '\n' )

        with open ( 'firewall_two_ipsec_policy.txt' , 'w+' ) as fw2_file :
            for item in firewall_two_ipsecpolicy :
                # item.pop ( 'creation-time' )
                # item.pop ( '.id' )
                # item.pop ( 'disabled' )
                # item.pop ( 'dynamic' )
                json.dump ( item , fw2_file )
                fw2_file.write ( '\n' )

        # Proposal
        with open ( 'firewall_one_ipsec_proposal.txt' , 'w+' ) as fw_file :
            for item in firewall_one_ipsecproposal :
                # item.pop ( 'creation-time' )
                # item.pop ( '.id' )
                # item.pop ( 'disabled' )
                # item.pop ( 'dynamic' )
                json.dump ( item , fw_file )
                fw_file.write ( '\n' )

        with open ( 'firewall_two_ipsec_proposal.txt' , 'w+' ) as fw2_file :
            for item in firewall_two_ipsecproposal :
                # item.pop ( 'creation-time' )
                # item.pop ( '.id' )
                # item.pop ( 'disabled' )
                # item.pop ( 'dynamic' )
                json.dump ( item , fw2_file )
                fw2_file.write ( '\n' )


def compare_file(file1, file2, filename):
    #create a new file
    with open('{}.txt'.format(filename), 'w+') as filename:
        with open(file1, 'r') as file1:
            with open(file2, 'r') as file2:
                diff = set(file1).difference(file2)
        for line in diff:
            filename.write(line)

#todo: need to add error hadnling when trying to write a bad parameter
#todo: with said error handling, actually tell what section of firewall it failed on!
def write_firewall(firewall, file,path):
    api = connect(**firewall)
    with open(file, 'r') as write_file:
        address_list = api.path(path)
        for line in write_file:
            #need to convert this back to JSON
            config = json.loads(line)
            #write the data to firewall
            address_list.add(**config)


#todo: create a more robust way to adding firewalls, possilby INI files?
primary_firewall= {
    'host': '10.255.20.193',
    'username': 'admin',
    'password': 'password1',
    'enconding': 'utf-16'
}
secondary_firewall= {
    'host': '10.255.20.191',
    'username': 'admin',
    'password': 'password1',
    'enconding': 'utf-16'
}

firewall_connect(primary_firewall, secondary_firewall)

compare_file('firewall_one_address_list.txt', 'firewall_two_address_list.txt', 'compared_lists')
compare_file('firewall_one_filter.txt', 'firewall_two_filter.txt', 'compared_filter')
compare_file('firewall_one_nat.txt', 'firewall_two_nat.txt','compared_nat')

#comparing filter rules

write_firewall(secondary_firewall, 'compared_lists.txt','/ip/firewall/address-list')

write_firewall(secondary_firewall, 'compared_filter.txt','ip/firewall/filter')

write_firewall(secondary_firewall, 'compared_nat.txt', '/ip/firewall/nat')

# email_report.email_report('angelo.poggi@webair.com',
#                           '',
#                           'rickie.harripersaud@webair.com',
#                           'Can you see me? This came from P Y T H O N')










