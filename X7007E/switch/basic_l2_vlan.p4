#include <core.p4>
#include <v1model.p4>

const bit<16> ETHERTYPE_TPID = 0x8100;

header ethernet_t {
    bit<48> dstAddr;
    bit<48> srcAddr;
    bit<16> ether_type;
}

header vlan_t {
    bit<3>   pcp;
    bit<1>   cfi;
    bit<12>  vid;
    bit<16>  ether_type;
}

struct headers {
    ethernet_t ethernet;
    vlan_t vlan;
}

struct metadata {}


parser ParserImpl(packet_in pkt, out headers hdr, inout metadata meta, inout standard_metadata_t standard_metadata) {

    state start {
        transition parse_ethernet;
    }

    state parse_ethernet {
        pkt.extract(hdr.ethernet);
        // transition parse_vlan_tag;
        transition select(hdr.ethernet.ether_type) {
            ETHERTYPE_TPID: parse_vlan_tag;
            default: accept;
        }
    }

    state parse_vlan_tag {
        pkt.extract(hdr.vlan);
        transition accept;
        }
}

control egress(inout headers hdr, inout metadata meta, inout standard_metadata_t standard_metadata) {
    apply {
    }
}

struct mac_learn_digest {
    bit<48> srcAddr;
    bit<9>  ingress_port;
}

control ingress(inout headers hdr, inout metadata meta, inout standard_metadata_t standard_metadata) {
    action forward(bit<9> port) {
        standard_metadata.egress_spec = port;
    }

    action bcast() {
        standard_metadata.mcast_grp = 1;
    }

    action mac_learn() {
        digest<mac_learn_digest>((bit<32>)1024, { hdr.ethernet.srcAddr, standard_metadata.ingress_port });
    }

    action drop() {
        mark_to_drop( standard_metadata );
        exit;
    }

    action _nop() {
    }

    table dmac {
        actions = {
            forward;
            bcast;
            drop;
        }
        key = {
            hdr.ethernet.dstAddr: exact;
        }
        default_action = bcast();
        size = 512;
    }

    table smac {
        actions = {
            mac_learn;
            _nop;
            drop;
        }
        key = {
            hdr.ethernet.srcAddr: exact;
        }
        default_action = mac_learn();
        size = 512;
    }

    // Note to self that this is not standard pracis and should be done using tabels insted.
    apply {
        // If the packet is of type 8100 then it is a tagged packet
        if (hdr.vlan.isValid()) {
            if (standard_metadata.ingress_port == 1 || standard_metadata.ingress_port == 2) {
                // If packet does not have its vlan tag set to 10: drop
                if (hdr.vlan.vid != 10) {
                    drop();
                    exit;
                } 
                // Else we need to invalidate/remove the vlan header
                else {
                    hdr.vlan.setInvalid();
                }
            }
        }
        else {
            // Apply nativ vlan for port 1 and 2
            if (standard_metadata.ingress_port == 1 || standard_metadata.ingress_port == 2) {
                hdr.vlan.vid = 10;
            }
        }
        smac.apply();
        dmac.apply();
    }
}

control DeparserImpl(packet_out packet, in headers hdr) {
    apply {
        packet.emit(hdr.ethernet);
    }
}

control verifyChecksum(inout headers hdr, inout metadata meta) {
    apply {
    }
}

control computeChecksum(inout headers hdr, inout metadata meta) {
    apply {
    }
}

V1Switch
(   ParserImpl(), 
    verifyChecksum(), 
    ingress(), 
    egress(), 
    computeChecksum(), 
    DeparserImpl()
    ) main;