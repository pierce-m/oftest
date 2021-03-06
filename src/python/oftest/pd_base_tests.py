"""
Base classes for test cases

Tests will usually inherit from one of these classes to have the controller
and/or dataplane automatically set up.
"""

import importlib
import os
import logging
import unittest


import oftest
from oftest import config
import oftest.dataplane as dataplane

################################################################
#
# Thrift interface base tests
#
################################################################

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.protocol import TMultiplexedProtocol


class ThriftBaseTest(unittest.TestCase):
    def __str__(self):
        return self.id().replace('.runTest', '')

    def setUp(self):
        oftest.open_logfile(str(self))
        logging.info("** START TEST CASE " + str(self))

    def tearDown(self):
        logging.info("** END TEST CASE " + str(self))

class ThriftInterface(ThriftBaseTest):
    def __init__(self, p4_name):
        ThriftBaseTest.__init__(self)
        self.p4_name = p4_name
        self.p4_client_module = importlib.import_module(".".join(["p4_pd_rpc", p4_name]))
        self.mc_client_module = importlib.import_module(".".join(["mc_pd_rpc", "mc"]))
        self.conn_mgr_client_module = importlib.import_module(".".join(["conn_mgr_pd_rpc", "conn_mgr"]))

    def setUp(self):
        ThriftBaseTest.setUp(self)

        # Set up thrift client and contact server
        self.transport = TSocket.TSocket('localhost', 9090)
        self.transport = TTransport.TBufferedTransport(self.transport)
        bprotocol = TBinaryProtocol.TBinaryProtocol(self.transport)

        self.mc_protocol = TMultiplexedProtocol.TMultiplexedProtocol(bprotocol, "mc")
        self.conn_mgr_protocol = TMultiplexedProtocol.TMultiplexedProtocol(bprotocol, "conn_mgr")
        self.p4_protocol = TMultiplexedProtocol.TMultiplexedProtocol(bprotocol, self.p4_name)

        self.client = self.p4_client_module.Client(self.p4_protocol)
        self.mc = self.mc_client_module.Client(self.mc_protocol)
        self.conn_mgr = self.conn_mgr_client_module.Client(self.conn_mgr_protocol)
        self.transport.open()

    def tearDown(self):
        if config["log_dir"] != None:
            self.dataplane.stop_pcap()
        ThriftBaseTest.tearDown(self)
        self.transport.close()

class ThriftInterfaceDataPlane(ThriftInterface):
    """
    Root class that sets up the thrift interface and dataplane
    """
    def __init__(self, p4_name):
        ThriftInterface.__init__(self, p4_name)

    def setUp(self):
        ThriftInterface.setUp(self)
        self.dataplane = oftest.dataplane_instance
        self.dataplane.flush()
        if config["log_dir"] != None:
            filename = os.path.join(config["log_dir"], str(self)) + ".pcap"
            self.dataplane.start_pcap(filename)

    def tearDown(self):
        if config["log_dir"] != None:
            self.dataplane.stop_pcap()
        ThriftInterface.tearDown(self)
