from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import OVSBridge

from p4_mininet import P4Switch, P4Host

import argparse
from time import sleep

parser = argparse.ArgumentParser(description='Mininet demo')
parser.add_argument('--behavioral-exe', help='Path to behavioral executable',
                    type=str, action="store", required=True)
parser.add_argument('--thrift-port', help='Thrift server port for table updates',
                    type=int, action="store", default=9090)
parser.add_argument('--num-hosts', help='Number of hosts to connect to switch',
                    type=int, action="store", default=4)
parser.add_argument('--mode', choices=['l2', 'l3'], type=str, default='l2')
parser.add_argument('--json', help='Path to JSON config file',
                    type=str, action="store", required=True)
parser.add_argument('--pcap-dump', help='Dump packets on interfaces to pcap files',
                    type=str, action="store", required=False, default=False)
parser.add_argument('--enable-debugger', help='Enable debugger (Please ensure debugger support is enabled in behavioral exe, as it is disabled by default)',
                    action="store_true", required=False, default=False)

args = parser.parse_args()


def main():
    num_hosts = args.num_hosts
    mode = args.mode

    net = Mininet(topo=None,
                  host=P4Host,
                  controller=None
                  )

    s0 = net.addSwitch('s0', cls=P4Switch,
                       sw_path=args.behavioral_exe,
                       json_path=args.json,
                       thrift_port=9090,
                       pcap_dump=args.pcap_dump,
                       enable_debugger=args.enable_debugger)

    s1 = net.addSwitch('s1', cls=OVSBridge)
    s2 = net.addSwitch('s2', cls=OVSBridge)
    s3 = net.addSwitch('s3', cls=OVSBridge)
    s4 = net.addSwitch('s4', cls=OVSBridge)

    for h in range(num_hosts):
        net.addHost('h%d' % (h + 1),
                    ip="10.0.%d.10/24" % h,
                    mac='00:00:00:00:00:%02x' % (h+1))

    net.addLink("h1", s1)
    net.addLink("h2", s2)
    net.addLink("h3", s3)
    net.addLink("h4", s4)

    net.addLink(s0, s1)
    net.addLink(s0, s2)
    net.addLink(s0, s3)
    net.addLink(s0, s4)

    h1NAT = net.addNAT('h1NAT', ip='10.0.0.11/24',
                       mac='00:04:00:00:00:10', inNamespace=False, connect=False)
    h2NAT = net.addNAT('h2NAT', ip='10.0.1.11/24',
                       mac='00:04:00:00:00:20', inNamespace=False, connect=False)
    h3NAT = net.addNAT('h3NAT', ip='10.0.2.11/24',
                       mac='00:04:00:00:00:30', inNamespace=False, connect=False)
    h4NAT = net.addNAT('h4NAT', ip='10.0.3.11/24',
                       mac='00:04:00:00:00:40', inNamespace=False, connect=False)

    net.addLink(h1NAT, s1)
    net.addLink(h2NAT, s2)
    net.addLink(h3NAT, s3)
    net.addLink(h4NAT, s4)

    net.start()

    hub = net.get('s1')
    hub.cmd(
        'ovs-vsctl set Bridge s1 protocols=OpenFlow10,OpenFlow11,OpenFlow12,OpenFlow13')
    hub.cmd('ovs-ofctl -O OpenFlow13 add-flow s1 action=flood')

    hub2 = net.get('s2')
    hub2.cmd(
        'ovs-vsctl set Bridge s2 protocols=OpenFlow10,OpenFlow11,OpenFlow12,OpenFlow13')
    hub2.cmd('ovs-ofctl -O OpenFlow13 add-flow s2 action=flood')

    hub3 = net.get('s3')
    hub3.cmd(
        'ovs-vsctl set Bridge s3 protocols=OpenFlow10,OpenFlow11,OpenFlow12,OpenFlow13')
    hub3.cmd('ovs-ofctl -O OpenFlow13 add-flow s3 action=flood')

    hub4 = net.get('s4')
    hub4.cmd(
        'ovs-vsctl set Bridge s4 protocols=OpenFlow10,OpenFlow11,OpenFlow12,OpenFlow13')
    hub4.cmd('ovs-ofctl -O OpenFlow13 add-flow s4 action=flood')

    sw_mac = ["00:aa:bb:00:00:%02x" % n for n in range(num_hosts)]

    sw_addr = ["10.0.%d.1" % n for n in range(num_hosts)]

    for n in range(num_hosts):
        h = net.get('h%d' % (n + 1))
        if mode == "l2":
            h.setDefaultRoute("dev eth0")
            h.cmd("make startRPC")
        else:
            h.setARP(sw_addr[n], sw_mac[n])
            h.setDefaultRoute("dev eth0 via %s" % sw_addr[n])
            print

    for n in range(num_hosts):
        h = net.get('h%d' % (n + 1))
        h.describe()

    sleep(1)

    print("Ready !")

    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    main()
