
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



primary_firewall= {
    'host': '10.255.20.193',
    'username': 'admin',
    'password': 'password1',
    'enconding': 'utf-16',
    'ssl_wrapper': ctx.wrap_socket ,
    'port': '8729'

}
secondary_firewall= {
    'host': '10.255.20.191',
    'username': 'admin',
    'password': 'password1',
    'enconding': 'utf-16',
    'ssl_wrapper': ctx.wrap_socket ,
    'port': '8729'

}

##############################
#Connection to Firewalls and#
##############################
try:
    connection.firewall_connect(primary_firewall)
except:
    email_report.message('{} appears to be offline!\n The firewalls are no longer in sync'.format(primary_firewall['host']))
    sys.exit(1)

try:
    connection.firewall_connect(secondary_firewall)
except:
    email_report.message('{} appears to be offline!\n The firewalls are no longer in sync!'.format(secondary_firewall['host']))
    sys.exit(1)


##########################
#File comparisons
##########################
try:
    compare_file.compare_file('{}_address_list.txt'.format(primary_firewall['host']),
                              '{}_address_list.txt'.format(secondary_firewall['host']),
                              'compared_list')
except:
    email_report.message('There was an issue Comparing the Address lists for both firewalls')
    sys.exit(1)

try:
    compare_file.compare_file('{}_filter.txt'.format(primary_firewall['host']),
                              '{}_filter.txt'.format(secondary_firewall['host']),
                              'compared_filter')
except:
    email_report.message('There was an issue comparing the filter rules for both firewalls!')

try:










#
# try
#
#     email_report.message('Please check to ensure the following firewalls are online!{} and {}'.format(primary_firewall['host'],
#                                                                                                       secondary_firewall['host']))
#     print('Error Connecting to firewall')
#     sys.exit ( 1 )
#
#
#
# try:
#     compare_file.compare_file ( 'firewall_one_address_list.txt' , 'firewall_two_address_list.txt' , 'compared_lists' )
#     compare_file.compare_file ( 'firewall_one_filter.txt' , 'firewall_two_filter.txt' , 'compared_filter' )
#     compare_file.compare_file ( 'firewall_one_nat.txt' , 'firewall_two_nat.txt' , 'compared_nat' )
#     compare_file.compare_file ( 'firewall_one_ipsec_peer.txt', 'firewall_two_ipsec_peer.txt', 'compared_peer')
#     compare_file.compare_file ( 'firewall_one_ipsec_policy.txt' , 'firewall_two_ipsec_policy.txt' , 'compared_policy' )
#     compare_file.compare_file ( 'firewall_one_ipsec_proposal.txt' , 'firewall_two_ipsec_proposal.txt' , 'compared_proposal' )
#     compare_file.compare_file ( 'firewall_one_ipsec_identity.txt' , 'firewall_two_ipsec_identity.txt' , 'compared_identity' )
# except:
#
#     email_report.message('There was an issue Comparing files! Please check the Sync Script')
#     sys.exit ( 1 )
#
#
#
#
# try:
#     write_firewall.write_firewall ( secondary_firewall , 'compared_lists.txt' , '/ip/firewall/address-list' )
#
#     write_firewall.write_firewall ( secondary_firewall , 'compared_filter.txt' , 'ip/firewall/filter' )
#
#     write_firewall.write_firewall ( secondary_firewall , 'compared_nat.txt' , '/ip/firewall/nat' )
#
#     # write_firewall.write_firewall(secondary_firewall, 'compared_peer.txt', '/ip/ipsec/peer')
#
# except:
#     email_report.message('There was an issue Writing changes to the firewall! Please Check the Sync Script!')
#     sys.exit ( 1 )
#
# #Clean up
#
#
#
#








