
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
import sync_script
import compare_file
import write_firewall
import sys




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


try:
    sync_script.firewall_connect(primary_firewall, secondary_firewall)

except :

    email_report.message('Please checkt to ensure the follwing firewalls are online!{} and {}'.format(primary_firewall['host'],
                                                                                                      secondary_firewall['host']))
    sys.exit ( 1 )



try:
    compare_file.compare_file ( 'firewall_one_address_list.txt' , 'firewall_two_address_list.txt' , 'compared_lists' )
    compare_file.compare_file ( 'firewall_one_filter.txt' , 'firewall_two_filter.txt' , 'compared_filter' )
    compare_file.compare_file ( 'firewall_one_nat.txt' , 'firewall_two_nat.txt' , 'compared_nat' )
except:

    email_report.message('There was an issue Comparing files! Please check the Sync Script')
    sys.exit ( 1 )




try:
    write_firewall.write_firewall ( secondary_firewall , 'compared_lists.txt' , '/ip/firewall/address-list' )

    write_firewall.write_firewall ( secondary_firewall , 'compared_filter.txt' , 'ip/firewall/filter' )

    write_firewall.write_firewall ( secondary_firewall , 'compared_nat.txt' , '/ip/firewall/nat' )
except:
    email_report.message('There was an issue Writing changes to the firewall! Please Check the Sync Script!')
    sys.exit ( 1 )












