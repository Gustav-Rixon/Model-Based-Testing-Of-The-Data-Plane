
import unittest
from scapy.all import *

# This paket will fail because the host is bad
packet = IP(dst="10.0.2.20")/TCP()


class RixonsVlanss(unittest.TestCase):

    ass = ""
    src = ""

    # Here is where a assert should check if expected outcome equels the simulated outcome
    def v23(self):
        # This will indecate for the model what the expected outcome is

        # Build packet (automatically done when sending)
        #    ans, unans = sr(IP(raw(packet)), timeout=2)
     #   self.assertEquals(ass, ans.show().__str__(), msg="ajajja")
        pass

    def v_drop(self):
        global ass
        ass = "None"  # If the paket is dropt assume no response

    def v_floodToAllPortsOnVlan(self):
        pass

    def v_forward(self):
        global ass
        ass = "None"

    def v_newPacket(self):
        global ass
        ass = ""  # No ass

    # TODO
    # NEEDS What host is sending
    # Cheks its own ip?
    def v_typeOfPort(self):
        # f = open('switchBehavior.json')
        # data = json.load(f)

        # try:
        #    tmp = data["h1"]["conPort"]
        #    print(tmp)
        # except KeyError:
        #    print("ID doesn't exist")
        pass

        # Activate Guard

    # ACTIONS

    def e_R_correctVlanTag(self):
        pass

    def e_R_h2AsSource(self):
        pass

    def e16(self):
        pass

    def e_R_sameAsNativVlan(self):
        pass

    def e14(self):
        pass

    def e_R_h4AsSource(self):
        pass

    def e_R_h3AsSource(self):
        pass

    def e_R_h1AsSource(self):
        pass

    def e_R_tagged(self):
        pass

    def e_R_broadcast(self):
        pass

    def e_R_untagged(self):
        pass

    def e_R_noVlanTag(self):
        pass

    def e_R_incorrectVlanTag(self):
        pass

    def e_R_tagged(self):
        pass

    def e_R_sameAsNativVlan(self):
        pass

    def e_R_h2AsSource(self):
        pass

    def e_R_incorrectVlanTag(self):
        pass

    def e_R_untagged(self):
        pass

    def e_R_h1AsSource(self):
        pass

    def e16(self):
        pass

    def e_R_h4AsSource(self):
        pass

    def e_R_noVlanTag(self):
        pass

    def e_R_correctVlanTag(self):
        pass

    def e14(self):
        pass

    def e_R_h3AsSource(self):
        pass

    def e_R_broadcast(self):
        pass

    def e_R_sameAsNativVlan(self):
        pass

    def e14(self):
        pass

    def e_R_h1AsSource(self):
        pass

    def e_R_h3AsSource(self):
        pass

    def e_R_tagged(self):
        pass

    def e16(self):
        pass

    def e_R_incorrectVlanTag(self):
        pass

    def e_R_correctVlanTag(self):
        pass

    def e_R_h4AsSource(self):
        pass

    def e_R_untagged(self):
        pass

    def e_R_broadcast(self):
        pass

    def e_R_h2AsSource(self):
        pass

    def e16(self):
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

    def v_addVlanTagAndFlood(self):
        pass

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
