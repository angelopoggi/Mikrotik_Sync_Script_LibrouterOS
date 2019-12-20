############################################
#Mikrotik Sync Script Function
#By: Angelo Poggi
#
#
#This is the main code that creates connections to the firewall
#Pulls data, reads it and creates files
#############################################

#todo: add error handling if firewalls are not online!
#todo: rename this function to something more fitting on what it is doing
#Import all of Librouter
from librouteros import *
import json

def firewall_connect(primary_firewall, secondary_firewall):

    firewall_one = connect(**primary_firewall)
    firewall_two = connect(**secondary_firewall)


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
