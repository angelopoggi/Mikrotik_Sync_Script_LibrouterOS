
##############################
#Mikrotik Sync Script
#by: Angelo Poggi
#Angelo.poggi@webair.com
#
#This Script uses Librouter OS to read primary firewall
#and send the difference to the secondary firewall
#
#################################



import email_report
import compare_file
import write_firewall
import sys
import ssl
import connection
import configparser
import json2html
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
    '{}_ipsec_identity.txt'.format(primary_firewall['host']),
    '{}_ipsec_policy.txt'.format(primary_firewall['host']),
    '{}_ipsec_proposal.txt'.format(primary_firewall['host']),
    '{}_ipsec_peer.txt'.format(primary_firewall['host'])
]

firewall_two_files = [
    '{}_address_list.txt'.format(secondary_firewall['host']),
    '{}_filter.txt'.format(secondary_firewall['host']),
    '{}_nat.txt'.format(secondary_firewall['host']),
    '{}_ipsec_identity.txt'.format(secondary_firewall['host']),
    '{}_ipsec_policy.txt'.format(secondary_firewall['host']),
    '{}_ipsec_proposal.txt'.format(secondary_firewall['host']),
    '{}_ipsec_peer.txt'.format(secondary_firewall['host'])
]

compared_files = [
    'compared_address.txt',
    'compared_filter.txt',
    'compared_nat.txt',
    'compared_identity.txt',
    'compared_policy.txt',
    'compared_proposal.txt',
    'compared_peer.txt'
]

paths = [
    '/ip/firewall/address-list',
    '/ip/firewall/filter',
    '/ip/firewall/nat',
    '/ip/ipsec/identity',
    '/ip/ipsec/policy',
    '/ip/ipsec/proposal',
    '/ip/ipsec/peer'


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
    write_firewall.write_firewall ( secondary_firewall , comp , path )

    # try:
    #      write_firewall.write_firewall(secondary_firewall, comp, path)
    #
    # except:
    #     email_report.message('there was an issue writing {} to {}'.format(comp, secondary_firewall['host']))
    #     sys.exit(1)

############################
#Send a summary email
############################

for compared in compared_files:
    compared = json2html.convert(json=compared)
    email_report.message('Below is a summary of what was written to the {}\n{}'.format(secondary_firewall['host'], compared))

















