
import unittest
import json
from scapy.all import *

# This paket will fail because the host is bad
packet = IP(dst="10.0.2.20")/TCP()


class RixonsVlanss(unittest.TestCase):
    # Implemented
    src = ""
    dst = ""
    pktType = ""
    vlanTag = ""
    typeOfPort = ""
    nativVlanTagOnSwPort = ""

    # Not Implemented

    # Here is where a assert should check if expected outcome equels the simulated outcome

    def v23(self):
        global src
        # This will indecate for the model what the expected outcome is

        # Build packet (automatically done when sending)
        #    ans, unans = sr(IP(raw(packet)), timeout=2)
     #   self.assertEquals(ass, ans.show().__str__(), msg="ajajja")
        print("----------SRC-------------")
        print(src)
        print("--------------------------")

    def v_drop(self):
        global ass
        ass = "fail"  # If the paket is dropt assume no response

    # TODO
    # This need to check more!
    # Ex: expect multiple responses!
    def v_floodToAllPortsOnVlan(self):
        global ass
        ass = "succ"

    def v_addVlanTagAndFlood(self):
        global ass, vlanTag, nativVlanTagOnSwPort
        vlanTag = nativVlanTagOnSwPort
        ass = "succ"

    def v_forward(self):
        global ass
        ass = "succ"

    def v_newPacket(self):
        global ass
        ass = ""  # No ass

    # TODO
    # NEEDS What host is sending
    # Cheks its own ip?
    def v_typeOfPort(self):
        pass

        # Activate Guard

    def v_choose_dst(self):
        pass

    # ACTIONS

    def e_R_correctVlanTag(self):
        pass

    def e16(self):
        pass

    def e_R_sameAsNativVlan(self):
        pass

    def e14(self):
        pass

    def e_R_h4AsSource(self):
        global src, typeOfPort, nativVlanTagOnSwPort
        nativVlanTagOnSwPort = 40
        typeOfPort = "tagged"
        src = GetHost("h4")

    def e_R_h3AsSource(self):
        global src, typeOfPort, nativVlanTagOnSwPort
        nativVlanTagOnSwPort = 30
        typeOfPort = "untagged"
        src = GetHost("h3")

    def e_R_h2AsSource(self):
        global src, typeOfPort, nativVlanTagOnSwPort
        nativVlanTagOnSwPort = 20
        typeOfPort = "tagged"
        src = GetHost("h2")

    def e_R_h1AsSource(self):
        global src, typeOfPort, nativVlanTagOnSwPort
        nativVlanTagOnSwPort = 10
        typeOfPort = "untagged"
        src = GetHost("h1")

    def e_R_h4AsDst(self):
        global dst
        dst = "h4"

    def e_R_h3AsDst(self):
        global dst
        dst = "h3"

    def e_R_h2AsDst(self):
        global dst
        dst = "h2"

    def e_R_h1AsDst(self):
        global dst
        dst = "h1"

    def e_R_tagged(self):
        global pktType
        pktType = "tagged"

    def e_R_untagged(self):
        global pktType
        pktType = "untagged"

    def e_R_broadcast(self):
        global pktType
        pktType = "broadcast"

    def e_R_br_tagged(self):
        global pktType
        pktType = "broadcast_tagged"

    def e_R_br_untagged(self):
        global pktType
        pktType = "broadcast_untagged"

    def e_R_noVlanTag(self):
        global vlanTag
        vlanTag = ""

    def e_R_incorrectVlanTag(self):
        global vlanTag
        vlanTag = "incorrect"

    def e_R_sameAsNativVlan(self):
        global vlanTag
        vlanTag = "sameAsNativVlan"

    def e_R_correctVlanTag(self):
        global vlanTag
        vlanTag = "correct"

    def e16(self):
        pass

    def e14(self):
        pass

    def e7(self):
        pass

    def v_pkt_type(self):
        pass

    def e44(self):
        pass

    def e_init(self):
        pass

    def e_untaggedPKT(self):
        pass

    def e30(self):
        pass

    def e_notSameAsNativeVlan(self):
        pass

    def e_untaggedPort(self):
        pass

    def v_addVlanTag(self):
        pass

    def v_choose_source_start(self):
        pass

    def e45(self):
        pass

    def e_taggedPort(self):
        pass

    def v_init(self):
        print("-----NEWTEST-----")

    def e42(self):
        pass

    def v_taggedOrUntaggedPacket(self):
        pass

    def v_tagged_or_untagged(self):
        pass

    def e48(self):
        pass

    def e_broadcastPKT(self):
        pass

    def e_yes(self):
        pass

    def e43(self):
        pass

    def v_typeOfPacket(self):
        pass

    def v_allowd(self):
        pass

    def v_addNativeVlanTag(self):
        pass

    def e46(self):
        pass

    def v_vlanConf(self):
        pass

    def v_checkVlan(self):
        pass

    def v_ifTagSameAsPort(self):
        pass

    def v_checkIfAllowd(self):
        pass

    def e_sameAsNativeVlan(self):
        pass

    def e_no(self):
        pass

    def e31(self):
        pass

    def e6(self):
        pass

    def e_taggedPKT(self):
        pass

    def e19(self):
        pass

# ----helper functions-----#


def GetHost(hostname):
    f = open('networkInfo.json')
    data = json.load(f)

    try:
        host = data[hostname]["ip"]
        return host
    except KeyError:
        print("Host doesn't exist")
    pass


def CreatePkt():
    pass

# TODO send the pkt lamo


def SendPkt():
    pass
