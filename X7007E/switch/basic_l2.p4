/*
Comments addapted from https://github.com/jafingerhut/p4-guide/blob/master/demo1/demo1-heavily-commented.p4_16.p4
*/


/*
 * standard #include in just about every P4 program.  You can see its
 * (short) contents here:
 *
 * https://github.com/p4lang/p4c/blob/master/p4include/core.p4
 */
#include <core.p4>

/* v1model.p4 defines one P4_16 'architecture', i.e. is there an
 * ingress and an egress pipeline, or just one?  Where is parsing
 * done, and how many parsers does the target device have?  etc.
 *
 * You can see its contents here:
 * https://github.com/p4lang/p4c/blob/master/p4include/v1model.p4
 *
 * The standard P4_16 architecture called PSA (Portable Switch
 * Architecture) version 1.1 was published on November 22, 2018 here:
 *
 * https://p4.org/specs/
 *
 * P4_16 programs written for the PSA architecture should include the
 * file psa.p4 instead of v1model.p4, and several parts of the program
 * after that would use different extern objects and functions than
 * this example program shows.
 *
 * In the v1model.p4 architecture, ingress consists of these things,
 * programmed in P4.  Each P4 program can name these things as they
 * choose.  The name used in this program for that piece is given in
 * parentheses:
 *
 * + a parser (parserImpl)
 * + a specialized control block intended for verifying checksums
 *   in received headers (verifyChecksum)
 * + ingress match-action pipeline (ingressImpl)
 *
 * Then there is a packet replication engine and packet buffer, which
 * are not P4-programmable.
 *
 * Egress consists of these things, programmed in P4:
 *
 * + egress match-action pipeline (egressImpl)
 * + a specialized control block intended for computing checksums in
 *   transmitted headers (updateChecksum)
 * + deparser (also called rewrite in some networking chips, deparserImpl)
 */
#include <v1model.p4>

/*************************************************************************
*********************** H E A D E R S  ***********************************
*************************************************************************/


/* bit<48> is just an unsigned integer that is exactly 48 bits wide.
 * P4_16 also has int<N> for 2's complement signed integers, and
 * varbit<N> for variable length header fields with a maximum size of
 * N bits. */

/* header types are required for all headers you want to parse in
 * received packets, or transmit in packets sent. */

header ethernet_t {
    bit<48> dstAddr;
    bit<48> srcAddr;
    bit<16> etherType;
}

/* "Metadata" is the term used for information about a packet, but
 * that might not be inside of the packet contents itself, e.g. a
 * bridge domain (BD) or VRF (Virtual Routing and Forwarding) id.
 * They can also contain copies of packet header fields if you wish,
 * which can be useful if they can be filled in from one of several
 * possible places in a packet, e.g. an outer IPv4 destination address
 * for non-IP-tunnel packets, or an inner IPv4 destination address for
 * IP tunnel packets.
 *
 * You can define as many or as few structs for metadata as you wish.
 * Some people like to have more than one struct so that metadata for
 * a forwarding feature can be grouped together, but separated from
 * unrelated metadata. */

struct metadata {
}

/* The v1model.p4 and psa.p4 architectures require you to define one
 * type that contains instances of all headers you care about, which
 * will typically be a struct with one member for each header instance
 * that your parser code might parse.
 *
 * You must also define another type that contains all metadata fields
 * that you use in your program.  It is typically a struct type, and
 * may contain bit vector fields, nested structs, or any other types
 * you want.
 *
 * Instances of these two types are then passed as parameters to the
 * top level controls defined by the architectures.  For example, the
 * ingress parser takes a parameter that contains your header type as
 * an 'out' parameter, returning filled-in headers when parsing is
 * complete, whereas the ingress control block takes that same
 * parameter with direction 'inout', since it is initially filled in
 * by the parser, but the ingress control block is allowed to modify
 * the contents of the headers during packet processing.
 *
 */

struct headers {
    ethernet_t ethernet;
}

/*************************************************************************
*********************** P A R S E R  ***********************************
*************************************************************************/

/*
    This function is the main packet parser. 
    It takes a packet as input and extracts the headers to populate the headers struct. 
    The parser begins at the start state and transitions to the parse_ethernet state to extract 
    Ethernet header fields. After that, the parser transitions to the accept state, which signals
    the end of the parsing process.
*/
parser parserImpl(packet_in packet, out headers hdr, inout metadata meta, inout standard_metadata_t standard_metadata) {

     /* A parser is specified as a finite state machine, with a 'state'
     * definition for each state of the FSM.  There must be a state
     * named 'start', which is the starting state.  'transition'
     * statements indicate what the next state will be.  There are
     * special states 'accept' and 'reject' indicating that parsing is
     * complete, where 'accept' indicates no error during parsing, and
     * 'reject' indicates some kind of parsing error. */
    state start {
        transition parse_ethernet;
    }

    state parse_ethernet {
        /* extract() is the name of a method defined for packets,
         * declared in core.p4 #include'd above.  The parser's
         * execution model starts with a 'pointer' to the beginning of
         * the received packet.  Whenever you call the extract()
         * method, it takes the size of the argument header in bits B,
         * copies the next B bits from the packet into that header
         * (making that header valid), and advances the pointer into
         * the packet by B bits.  Some P4 targets, such as the
         * behavioral model called BMv2 simple_switch, restrict the
         * headers and pointer to be a multiple of 8 bits. */
        packet.extract(hdr.ethernet);
        /* The 'select' keyword introduces an expression that is like
         * a C 'switch' statement, except that the expression for each
         * of the cases must be a state name in the parser.  This
         * makes convenient the handling of many possible Ethernet
         * types or IPv4 protocol values. */
        transition accept;
    }

}

/*************************************************************************
************   C H E C K S U M    V E R I F I C A T I O N   *************
*************************************************************************/

/*
This function is a control block for verifying checksums. 
In the given code, it does not perform any operation
*/
control verifyChecksum(inout headers hdr, inout metadata meta) {
    apply {
    }
}

/* This program is for a P4 target architecture that has an ingress
 * and an egress match-action 'pipeline' (nothing about the P4
 * language requires that the target hardware must have a pipeline in
 * it, but 'pipeline' is the word often used since the current highest
 * performance target devices do have one).
 *
 */

/*************************************************************************
**************  I N G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

struct mac_learn_digest {
    bit<48> srcAddr;
    bit<9>  ingress_port;
}

/*
This function is responsible for ingress processing, 
including learning source MAC addresses, forwarding packets based on destination MAC addresses, 
broadcasting packets if necessary, and handling packet drops. It defines multiple actions 
(forward, bcast, mac_learn, drop, and _nop) and two tables (dmac and smac) to perform these operations.
*/

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


    /* Every control block must contain an 'apply' block.  The
     * contents of the apply block specify the sequential flow of
     * control of packet processing, including applying the tables you
     * wish, in the order you wish.
     *
     * This one is particularly simple -- always apply the ipv4_da_lpm
     * table, and regardless of the result, always apply the mac_da
     * table.  It is definitely possible to have 'if' statements in
     * apply blocks that handle many possible cases differently from
     * each other, based upon the values of packet header fields or
     * metadata fields. */
    apply {
        smac.apply();
        dmac.apply();
    }
}

/*************************************************************************
****************  E G R E S S   P R O C E S S I N G   ********************
*************************************************************************/

/*
This function is responsible for egress processing. In the given code, it does not perform any operation.
*/
control egress(inout headers hdr, inout metadata meta, inout standard_metadata_t standard_metadata) {
    apply {
    }
}

/*************************************************************************
*************   C H E C K S U M    C O M P U T A T I O N   ***************
*************************************************************************/


/*
This function is a control block for computing checksums. In the given code, it does not perform any operation.
*/
control computeChecksum(inout headers hdr, inout metadata meta) {
    apply {
    }
}

/* The deparser controls what headers are created for the outgoing
 * packet. */

/*************************************************************************
***********************  D E P A R S E R  *******************************
*************************************************************************/

/*
This function is the main deparser that takes the headers struct and emits the packet. In this case, it emits the Ethernet header.
*/
control deparserImpl(packet_out packet, in headers hdr) {
    apply {
         /* The emit() method takes a header.  If that header's hidden
         * 'valid' bit is true, then emit() appends the contents of
         * the header (which may have been modified in the ingress or
         * egress pipelines above) into the outgoing packet.
         *
         * If that header's hidden 'valid' bit is false, emit() does
         * nothing. */
        packet.emit(hdr.ethernet);
    }
}

/* This is a "package instantiation".  There must be at least one
 * named "main" in any complete P4_16 program.  It is what specifies
 * which pieces to plug into which "slot" in the target
 * architecture. */
V1Switch(   
    parserImpl(), 
    verifyChecksum(), 
    ingress(), 
    egress(), 
    computeChecksum(), 
    deparserImpl()
    ) main;