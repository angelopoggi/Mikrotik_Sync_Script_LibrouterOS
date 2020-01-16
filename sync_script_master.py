
##############################
#Mikrotik Sync Script
#by: Angelo Poggi
#Angelo.poggi@webair.com
#
#This Script uses Librouter OS to read primary firewall
#and send the difference to the secondary firewall
#
#################################


############
#All packages required for firewall stuff
import email_report
import compare_file
import write_firewall
import connection

###############
#Arbitrary modules needed for little odds and ends
from json2html import *
import json
import sys
import ssl
import configparser
import os





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
#VPN Info (Peers/policies

#todo: create a more robust way to adding firewalls, possilby INI files?

#Using this as per API's documenation - Might need to be changed?
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.set_ciphers ('ADH:@SECLEVEL=0')

config = configparser.ConfigParser()
config.read('config.ini')




primary_firewall= {
    'host':  config.get('firewalls','primary_firewall'),
    'username': config.get('credentials', 'fw1_username') ,
    'password': config.get('credentials', 'fw1_password'),
    'enconding': 'utf-16',
    'ssl_wrapper': ctx.wrap_socket ,
    'port': '8729'

}
secondary_firewall= {
    'host': config.get('firewalls', 'secondary_firewall'),
    'username': config.get('credentials', 'fw2_username'),
    'password': config.get('credentials', 'fw2_password'),
    'enconding': 'utf-16',
    'ssl_wrapper': ctx.wrap_socket ,
    'port': '8729'

}

firewalls = [
    primary_firewall,
    secondary_firewall
]

firewall_one_files = [
    '{}_address_list.txt'.format(primary_firewall['host']),
    '{}_filter.txt'.format(primary_firewall['host']),
    '{}_nat.txt'.format(primary_firewall['host']),
    '{}_ipsec_profile.txt'.format(primary_firewall['host']),
    '{}_ipsec_peer.txt'.format(primary_firewall['host']),
    '{}_ipsec_identity.txt'.format(primary_firewall['host']),
    '{}_ipsec_proposal.txt'.format(primary_firewall['host']),
    '{}_ipsec_policy.txt'.format(primary_firewall['host'])
    
    
]

firewall_two_files = [
    '{}_address_list.txt'.format(secondary_firewall['host']),
    '{}_filter.txt'.format(secondary_firewall['host']),
    '{}_nat.txt'.format(secondary_firewall['host']),
    '{}_ipsec_profile.txt'.format(secondary_firewall['host']),
    '{}_ipsec_peer.txt'.format(secondary_firewall['host']),
    '{}_ipsec_identity.txt'.format(secondary_firewall['host']),
    '{}_ipsec_proposal.txt'.format(secondary_firewall['host']),
    '{}_ipsec_policy.txt'.format(secondary_firewall['host'])
]

compared_files = [
    'compared_address',
    'compared_filter',
    'compared_nat',
    'compared_profile',
    'compared_peer',
    'compared_identity',
    'compared_proposal',
    'compared_policy'
    
    
]

######################
#When it comes to writing IPSEC, Peer msut come before Identity, as Peer is required for Identity configuration
#####################
paths = [
    '/ip/firewall/address-list',
    '/ip/firewall/filter',
    '/ip/firewall/nat',
    '/ip/ipsec/profile',
    '/ip/ipsec/peer',
    '/ip/ipsec/identity',
    '/ip/ipsec/proposal',
    '/ip/ipsec/policy',




]

##############################
#Connect to each firewall
##############################
for device in firewalls:
     try:
        connection.firewall_connect(device)
     except:
         email_report.message('''
         Error connecting to {}\n
         The Script has now quit and the firewalls are no longer in sync\n
         Please check the firewall is online or configuraiton in the script!'''.format(device['host']))
         sys.exit(1)
##############################################
#Compare files and write/Create the comparison
###############################################
for fw1,fw2,comp in zip(firewall_one_files, firewall_two_files, compared_files):
    try:
        compare_file.compare_file(fw1,fw2,comp)
    except:

        email_report.message('There was an error comparing {} {} {}'.format(fw1,fw2,comp))
        sys.exit(1)

##################################
#Write to the firewall
##################################
for comp,path in zip(compared_files, paths):
    try:
         write_firewall.write_firewall(secondary_firewall, comp, path)

    except:
        email_report.message('there was an issue writing {} to {}'.format(comp, secondary_firewall['host']))
        sys.exit(1)



############################
#Send a summary email
############################

#Wrting all changes made to a single file
with open('final_report', 'w+') as report:
    for comp in compared_files:
        with open(comp, 'r') as comp_file:
            for line in comp_file:
                report.write(line)

#IM sure there is an easier way to do this, but thisis the best I could come up with
#Read final_report, load it as JSON and then conver to html, send to email report
with open('final_report', 'r') as html:
    payload = []
    for line in html:
        table = json.loads(line)
        payload.append(table)
    final_payload = json2html.convert(json=payload)
    email_report.message('Script has Finished, please review any changes listed below. If no list is present, nothing was changed\n {}'.format(final_payload))





















