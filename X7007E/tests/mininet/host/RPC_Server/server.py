from scapy.all import *
import gevent
import gevent.pywsgi
import gevent.queue

from tinyrpc.server.gevent import RPCServerGreenlets
from tinyrpc.dispatch import RPCDispatcher
from tinyrpc.protocols.jsonrpc import JSONRPCProtocol
from tinyrpc.transports.wsgi import WsgiServerTransport


dispatcher = RPCDispatcher()
transport = WsgiServerTransport(queue_class=gevent.queue.Queue)

# start wsgi server as a background-greenlet
wsgi_server = gevent.pywsgi.WSGIServer(('', 80), transport.handle)
gevent.spawn(wsgi_server.serve_forever)


rpc_server = RPCServerGreenlets(
    transport,
    JSONRPCProtocol(),
    dispatcher
)


@dispatcher.public
def sendPkt():
    return "s"


# in the main greenlet, run our rpc_server
rpc_server.serve_forever()
