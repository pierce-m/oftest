# Distributed under the OpenFlow Software License (see LICENSE)
# Copyright (c) 2010 The Board of Trustees of The Leland Stanford Junior University
# Copyright (c) 2012, 2013 Big Switch Networks, Inc.
"""
Wrap scapy to satisfy pylint
"""
from oftest import config
import sys

try:
    import scapy.config
    import scapy.route
    import scapy.layers.l2
    import scapy.layers.inet
    import scapy.main
    if not config["disable_ipv6"]:
        import scapy.route6
        import scapy.layers.inet6
except ImportError:
    sys.exit("Need to install scapy for packet parsing")

Ether = scapy.layers.l2.Ether
LLC = scapy.layers.l2.LLC
SNAP = scapy.layers.l2.SNAP
Dot1Q = scapy.layers.l2.Dot1Q
GRE = scapy.layers.l2.GRE
IP = scapy.layers.inet.IP
IPOption = scapy.layers.inet.IPOption
ARP = scapy.layers.inet.ARP
TCP = scapy.layers.inet.TCP
UDP = scapy.layers.inet.UDP
ICMP = scapy.layers.inet.ICMP

if not config["disable_ipv6"]:
    IPv6 = scapy.layers.inet6.IPv6
    ICMPv6Unknown = scapy.layers.inet6.ICMPv6Unknown
    ICMPv6EchoRequest = scapy.layers.inet6.ICMPv6EchoRequest

if config["enable_vxlan"]:
    print "VXLAN enabled"
    scapy.main.load_contrib("vxlan")
    VXLAN = scapy.contrib.vxlan.VXLAN

if config["enable_erspan"]:
    print "ERSPAN enabled"
    scapy.main.load_contrib("erspan")
    ERSPAN = scapy.contrib.erspan.ERSPAN
    ERSPAN_III = scapy.contrib.erspan.ERSPAN_III

if config["enable_geneve"]:
    print "Geneve enabled"
    scapy.main.load_contrib("geneve")
    GENEVE = scapy.contrib.geneve.GENEVE

if config["enable_mpls"]:
    print "Mpls enabled"
    scapy.main.load_contrib("mpls")
    MPLS = scapy.contrib.mpls.MPLS

if config["enable_nvgre"]:
    print "Nvgre enabled"
    scapy.main.load_contrib("nvgre")
    NVGRE = scapy.contrib.nvgre.NVGRE
