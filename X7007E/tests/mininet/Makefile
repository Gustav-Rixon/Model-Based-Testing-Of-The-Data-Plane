startMininet:
	sudo mn -c
	sudo python3 main_l2.py --behavioral-exe simple_switch --json ../../switch/basic_l2_vlan.json

popTable:
	simple_switch_CLI --thrift-port 9090 < commands_l2.txt

confVlan:
	simple_switch_CLI --thrift-port 9090 < commands_vlan.txt

#######Client stuff###########
startRPC:
#	LOCAL_IP=$$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $$2}');
	pyro5-ns --host 0.0.0.0 &
	python3 host/RPC_Server/serverPyro5.py &

startPup:
	python3 host/RPC_Server/pup.py &