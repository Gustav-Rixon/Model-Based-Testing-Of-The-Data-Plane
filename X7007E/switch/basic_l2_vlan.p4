#include <core.p4>
#include <v1model.p4>


/*************************************************************************
*********************** H E A D E R S ***********************************
*************************************************************************/

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

struct metadata {
    bit<32> egress_port;
    bit<1> is_trunk;
}

/*************************************************************************
*********************** P A R S E R ***********************************
*************************************************************************/

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

/*************************************************************************
************ C H E C K S U M V E R I F I C A T I O N *************
*************************************************************************/

control verifyChecksum(inout headers hdr, inout metadata meta) {
    apply {
    }
}


/*************************************************************************
************** I N G R E S S P R O C E S S I N G *******************
*************************************************************************/

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

    action allowd() {
    }

    action tagPkt(bit<12> native_vlan_id) {
        hdr.vlan.ether_type = 0x8100;
        hdr.vlan.vid = native_vlan_id;
        hdr.vlan.cfi = 0;
        hdr.vlan.pcp = 001;
    }

    table allowdVlan { // Contains what vlan tag is allowd on what port 
        key = {
            standard_metadata.ingress_port: exact;
            //AND
            hdr.vlan.vid: exact;
        }
        actions = {
            allowd;
            drop;
        }
        default_action = drop();
        size = 1024;
    }

    table applyNativeVlan {
            key = {
            standard_metadata.ingress_port: exact;
            //AND
            hdr.vlan.vid: exact;
        }
        actions = {
            tagPkt;
            _nop;
        }
        default_action = _nop(); //Will not apply VLAN if not configured to
        size = 1024;
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
            hdr.ethernet.srcAddr: 
            exact;
        }
        default_action = mac_learn();
        size = 512;
    }

    apply {
        applyNativeVlan.apply();
        if (hdr.vlan.isValid()) {
            allowdVlan.apply();
        }
        smac.apply();
        dmac.apply();
    }
}


/*************************************************************************
**************** E G R E S S P R O C E S S I N G ********************
*************************************************************************/

control egress(inout headers hdr, inout metadata meta, inout standard_metadata_t standard_metadata) {
    action set_trunk_mode(bit<1> trunk_mode) {
        meta.is_trunk = trunk_mode;
    }

    table trunk_mode_table {
            key = {
            meta.egress_port: exact;
        }
        actions = {
            set_trunk_mode;
        }
        default_action = set_trunk_mode(0); //Will not apply VLAN if not configured to
        size = 1024;
    }

    apply {
        trunk_mode_table.apply();
        if (meta.is_trunk == 1) {
            hdr.vlan.setInvalid();
        }
    }
}

/*************************************************************************
************* C H E C K S U M C O M P U T A T I O N ***************
*************************************************************************/

control computeChecksum(inout headers hdr, inout metadata meta) {
    apply {
    }
}


/*************************************************************************
*********************** D E P A R S E R *******************************
*************************************************************************/

control DeparserImpl(packet_out packet, in headers hdr) {
    apply {
        packet.emit(hdr.ethernet);
    }
}

/*************************************************************************
*********************** S W I T C H *******************************
*************************************************************************/

V1Switch
(   ParserImpl(), 
    verifyChecksum(), 
    ingress(), 
    egress(), 
    computeChecksum(), 
    DeparserImpl()
    ) main;