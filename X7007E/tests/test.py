
import unittest
import json
from scapy.all import *

import Pyro5.api

import pynng
import logging

logger = logging.getLogger('my_logger')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('my_log_file.log')

formatter = logging.Formatter('%(asctime)s %(levelname)s:%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


# logger = logging.basicConfig(filename='test.log', level=logging.INFO,
#                             format='%(asctime)s %(levelname)s:%(message)s')

class RixonsVlanss(unittest.TestCase):
    # Implemented
    srcT = ""
    dstT = ""
    pktType = ""
    vlanTag = ""
    typeOfPort = ""
    nativVlanTagOnSwPort = ""
    expectedOutCome = False

    # Not Implemented

    # Here is where a assert should check if expected outcome equels the simulated outcome

    # This function should send the packet and assert it to the expected outcome

    def v23(self):
        # global src, dstT, expectedOutCome, pktType, vlanTag
        global src, dstT, expectedOutCome, pktType

        dstIPA = GetInfo(dstT, "ip")
        srcIPA = GetInfo(src, "ip")

        dstMACA = GetInfo(dstT, "mac")
        srcMACA = GetInfo(src, "mac")

        # dstIPA = "10.0.0.10"
        # srcIPA = "10.0.1.10"
        # dstMACA = "00:00:00:00:00:00:01"
        # srcMACA = "00:00:00:00:00:00:02"

        data = {
            "dstIP": dstIPA,
            "dstMAC": dstMACA,
            "srcMAC": srcMACA
        }

        data = json.dumps(data)

        t = threading.Thread(target=StartPub, args=(dstIPA, "tjaa", 1))
        # tt = threading.Thread(target=Sub, args=(dstIPA, 5))
        tt = threading.Thread(target=SendPkt, args=(srcIPA, data))
        # t.start()
        # tt.start()
        # time.sleep(1)  # RACE CONDITION ahhhhhhhhhhhhhhhhhhhhhh
        # s = Test()  # send multiple pkt to ensure delivery
        # time.sleep(2)  # sleep as to not overload the tinyRPC server ;)
        # SendPkt(srcIPA, data)
        # SendPkt(srcIPA, data)
        # SendPkt(srcIPA, data)
        # SendPkt(srcIPA, data)
        aw = Sub(dstIPA, 0)
        # tt.join()
        # t.join()
        # aw = ""
        logger.info("---SIMDATA---")
        logger.info("dst address %s", dstIPA)
        logger.info("src address %s", srcIPA)
        logger.info("dst mac %s", dstMACA)
        logger.info("src mac %s", srcMACA)
        logger.info("pktType %s", pktType)

        try:
            self.assertEqual(expectedOutCome, aw)
        except AssertionError as e:
            logger.error(f"Assertion FAILED: {e}")
        else:
            logger.info(
                "Assertion PASSED: arg1 = %s, arg2 = %s", aw, "arg2")

    def v_drop(self):
        global expectedOutCome
        expectedOutCome = False  # If the paket is dropt assume no response

    # TODO
    # This need to check more!
    # Ex: expect multiple responses!
    def v_floodToAllPortsOnVlan(self):
        global expectedOutCome
        expectedOutCome = True

    def v_addVlanTagAndFlood(self):
        global expectedOutCome, vlanTag, nativVlanTagOnSwPort
        vlanTag = nativVlanTagOnSwPort
        expectedOutCome = True

    def v_forward(self):
        global expectedOutCome
        expectedOutCome = True

    def v_newPacket(self):
        pass

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
        src = "h4"

    def e_R_h3AsSource(self):
        global src, typeOfPort, nativVlanTagOnSwPort
        nativVlanTagOnSwPort = 30
        typeOfPort = "untagged"
        src = "h3"

    def e_R_h2AsSource(self):
        global src, typeOfPort, nativVlanTagOnSwPort
        nativVlanTagOnSwPort = 20
        typeOfPort = "tagged"
        src = "h2"

    def e_R_h1AsSource(self):
        global src, typeOfPort, nativVlanTagOnSwPort
        nativVlanTagOnSwPort = 10
        typeOfPort = "untagged"
        src = "h1"

    def e_R_h4AsDst(self):
        global dstT
        dstT = "h4"

    def e_R_h3AsDst(self):
        global dstT
        dstT = "h3"

    def e_R_h2AsDst(self):
        global dstT
        dstT = "h2"

    def e_R_h1AsDst(self):
        global dstT
        dstT = "h1"

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


def GetInfo(hostname, info):
    f = open('networkInfo.json')
    data = json.load(f)
    try:
        host = data[hostname][info]
        f.close()
        return host
    except KeyError:
        print(hostname + " Host doesn't exist")
        f.close()
    pass


# def StartPub(hostIP, pattern, timeout):
#     rpc_client = RPCClient(
#         JSONRPCProtocol(),
#         HttpPostClientTransport('http://%s' % hostIP)
#     )

#     str_server = rpc_client.get_proxy()

#     str_server.pub(pattern, timeout)

def StartPub(hostIP, pattern, timeout):
    greeting_maker = Pyro5.api.Proxy(
        "PYRONAME:example.greeting@%s:9090" % hostIP)
    greeting_maker.pub(pattern, timeout)


def Test():
    greeting_maker = Pyro5.api.Proxy(
        "PYRONAME:example.greeting@10.0.0.10:9090")
    res = greeting_maker.get_fortune()
    return res


def SendPkt(hostIP, data):
    greeting_maker = Pyro5.api.Proxy(
        "PYRONAME:example.greeting@%s:9090" % hostIP)
    greeting_maker.sendPkt(data)


def Sub(target, max_timeouts):
    address = f'tcp://{target}:65432'
    timeouts = 0

    try:
        with pynng.Sub0(dial=address, recv_timeout=1) as socket:
            socket.subscribe(b'')

            while timeouts <= max_timeouts:
                try:
                    if socket.recv().decode() == 'True':
                        return True
                except pynng.Timeout:
                    timeouts += 1
    except pynng.exceptions.NNGException as e:  # This is a problem
        print(f"Connection error: {e}")
        return (f"Connection error: {e}")

    return False


def GetVlan(type):
    pass


def CreatePkt():
    pass

# TODO send the pkt lamo
