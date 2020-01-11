############################################
# Mikrotik Sync Script Function
# By: Angelo Poggi
#
#
# This is the main code that creates connections to the firewall
# Pulls data, reads it and creates files
#############################################

# todo: add error handling if firewalls are not online!
# todo: rename this function to something more fitting on what it is doing
# todo: add DHCP sync,
# Import all of Librouter
from librouteros import *
import json
import ssl


def firewall_connect(firewall) :
    ctx = ssl.create_default_context ()
    ctx.check_hostname = False
    ctx.set_ciphers ( 'ADH:@SECLEVEL=0' )

    firewall_object = connect(**firewall)


    # this will return a dictionary
    firewall_object_object_address_list = firewall_object.path ( '/ip/firewall/address-list' )
    # firewall rules
    firewall_object_filter = firewall_object.path ( '/ip/firewall/filter' )
    # NAT Rules
    firewall_object_nat = firewall_object.path ( '/ip/firewall/nat' )
    # IPSec PEER
    firewall_object_ipsecpeer = firewall_object.path ( '/ip/ipsec/peer' )
    # IPSec Policy
    firewall_object_ipsecpolicy = firewall_object.path ( '/ip/ipsec/policy' )
    # IPSec Proposal
    firewall_object_ipsecproposal = firewall_object.path ( '/ip/ipsec/proposal' )
    # IPSec Identity (for new firmwares)
    firewall_object_identity = firewall_object.path ( '/ip/ipsec/identity' )


    # todo: more testing with Key valu pairs, feel as though I am removing to many?
    # todo: create a function that does all this, outside of firewall_connect (?)
    ################################################
    # Filter Rules
    ################################################
    with open ( '{}_filter.txt'.format(firewall['host']) , 'w' ) as fw_filter :
        for item in firewall_object_filter :
            item.pop ( '.id' )
            item.pop ( 'bytes' )
            item.pop ( 'packets' )
            item.pop ( 'dynamic' )
            item.pop ( 'invalid' )
            json.dump ( item , fw_filter )
            fw_filter.write ( '\n' )


    ################################################
    # NAT
    ################################################

    with open ( '{}_nat.txt'.format(firewall['host']) , 'w+' ) as fw_nat :
        for item in firewall_object_nat :
            item.pop ( '.id' )
            item.pop ( 'bytes' )
            item.pop ( 'packets' )
            item.pop ( 'invalid' )
            item.pop ( 'dynamic' )
            json.dump ( item , fw_nat )
            fw_nat.write ( '\n' )



    ################################################
    # ADDRESS LISTS
    ################################################
    with open ( '{}_address_list.txt'.format(firewall['host']) , 'w+' ) as fw_file :
        for item in firewall_object_object_address_list :
            item.pop ( 'creation-time' )
            item.pop ( '.id' )
            item.pop ( 'disabled' )
            item.pop ( 'dynamic' )
            json.dump ( item , fw_file )
            fw_file.write ( '\n' )



    ################################################
    # IPSEC STUFF
    ################################################
    # PEER
    with open ( '{}_ipsec_peer.txt'.format(firewall['host']) , 'w+' ) as fw_file :
        for item in firewall_object_ipsecpeer :
            item.pop ( '.id' )
            json.dump ( item , fw_file )
            fw_file.write ( '\n' )

    # POLICY
    with open ( '{}_ipsec_policy.txt'.format(firewall['host']) , 'w+' ) as fw_file :
        for item in firewall_object_ipsecpolicy :
            item.pop ( '.id' )
            item.pop ( 'disabled' )
            item.pop ( 'dynamic' )
            json.dump ( item , fw_file )
            fw_file.write ( '\n' )

    # Proposal
    with open ( '{}_ipsec_proposal.txt'.format(firewall['host']) , 'w+' ) as fw_file :
        for item in firewall_object_ipsecproposal :
            item.pop ( '.id' )
            json.dump ( item , fw_file )
            fw_file.write ( '\n' )

    # Identity
    with open ( '{}_ipsec_identity.txt'.format(firewall['host']) , 'w+' ) as fw_file :
        for item in firewall_object_identity :
            item.pop ( '.id' )
            json.dump ( item , fw_file )
            fw_file.write ( '\n' )






















