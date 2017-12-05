#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import unittest
import configparser

from ippbxpy.confgens import asterisk_pjsip_user_config
from ippbxpy.confgens import asterisk_sip_user_config
from ippbxpy.confgens import yealink_phone_config


class ConfigGeneratorsTests(unittest.TestCase):
    cfg = configparser.ConfigParser()
    cfg.read('etc/ippbx.cfg-dist')
    cfg['DEFAULT']['debug'] = "False"

    def test_pjsip(self):
        """asterisk_pjsip_user_config(
            cfg,
            phonenum,
            username,
            userpass,
            pickupgroup)
        """
        self.maxDiff = None
        r1 = """; AUTOGENERATED, do not modify manually
; 1001 <User Name> pass


[1001]
type=auth
auth_type=userpass
username=1001
password=pass

[1001]
type=aor
max_contacts=1
remove_existing=yes
qualify_frequency=5

[1001]
type=endpoint
callerid=User Name <1001>
transport=transport-udp
context=user-context
disallow=all
allow=g722,g729,alaw,ulaw
aors=1001
auth=1001
rtp_symmetric=yes
rtp_ipv6=yes
rewrite_contact=yes
send_rpid=yes
named_call_group=p1
named_pickup_group=p1
tos_audio=ef
cos_audio=5

"""
        self.assertEqual(
            asterisk_pjsip_user_config(
                self.cfg,
                "1001",
                "User Name",
                "pass",
                "p1"),
            r1)

    def test_sip(self):
        """asterisk_sip_user_config(
            cfg,
            phonenum,
            username,
            userpass,
            pickupgroup)
        """
        self.maxDiff = None
        r1 = """; AUTOGENERATED, do not modify manually
; 1001 <User Name> pass

[1001]
type=friend
host=dynamic
username=1001
secret=pass
fullname=1001
callerid=User Name
context=user-context
transport=udp
disallow=all
allow=g722,g729,alaw,ulaw
canreinvite=no
nat=yes
qualify=yes
hassip=yes
hasiax=no
hash323=no
hasmanager=no
namedcallgroup=p1
namedpickupgroup=p1

"""
        self.assertEqual(
            asterisk_sip_user_config(
                self.cfg,
                "1001",
                "User Name",
                "pass",
                "p1"),
            r1)

    def test_yealink(self):
        """yealink_phone_config(
            cfg,
            phonetype,
            phonehwmac,
            phonenum,
            username,
            userpass)
        """
        self.maxDiff = None
        r1 = """[ account ]
path = /config/voip/sipAccount0.cfg
Enable = 1
Label = 1001 - User Name
DisplayName = 1001
AuthName = 1001
UserName = 1001
password = pass
SIPServerHost = 192.168.0.1
SIPServerPort = 5060
Transport = 0

[ LocalTime ]
path = /config/Network/Network.cfg
local_time.time_zone = +3
local_time.summer_time = 0

[ Network ]
path = /config/Network/Network.cfg
eWANType = 2

[ LLDP ]
path = /config/Network/Network.cfg
EnableLLDP = 1

[ QOS ]
path = /config/Network/Network.cfg
RTPTOS = 46
SIGNALTOS = 26

[ AdminPassword ]
path = /config/Setting/autop.cfg
password = ADMIN_PASSWORD

"""
        self.assertEqual(
            yealink_phone_config(
                self.cfg,
                "1",
                "123123123",
                "1001",
                "User Name",
                "pass"),
            r1)
        r2 = """[ account ]
path = /config/voip/sipAccount0.cfg
Enable = 1
Label = 1001 - User Name
DisplayName = 1001
AuthName = 1001
UserName = 1001
password = pass
SIPServerHost = 192.168.0.1
SIPServerPort = 5060
Transport = 0

[ LocalTime ]
path = /config/Network/Network.cfg
local_time.time_zone = +3
local_time.summer_time = 0

[ Network ]
path = /config/Network/Network.cfg
eWANType = 2

[ LLDP ]
path = /config/Network/Network.cfg
EnableLLDP = 1

[ QOS ]
path = /config/Network/Network.cfg
RTPTOS = 46
SIGNALTOS = 26

[ AdminPassword ]
path = /config/Setting/autop.cfg
password = ADMIN_PASSWORD

"""
        self.assertEqual(
            yealink_phone_config(
                self.cfg,
                "2",
                "123123123",
                "1001",
                "User Name",
                "pass"),
            r2)
        r5 = """#!version:1.0.0.1
account.1.enable = 1
account.1.label = 1001-User Name
account.1.display_name = 1001
account.1.auth_name = 1001
account.1.user_name = 1001
account.1.password = pass
account.1.sip_server.1.address = 192.168.0.1
account.1.sip_server.1.port = 5060

local_time.time_zone = +3
local_time.summer_time = 0

network.ip_address_mode = 2

network.lldp.enable = 1

network.qos.rtptos = 46
network.qos.signaltos = 26

security.user_password = ADMIN_PASSWORD

"""
        self.assertEqual(
            yealink_phone_config(
                self.cfg,
                "5",
                "123123123",
                "1001",
                "User Name",
                "pass"),
            r5)


# EOF
