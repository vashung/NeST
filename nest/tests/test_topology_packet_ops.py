# SPDX-License-Identifier: GPL-2.0-only
# Copyright (c) 2019-2022 NITK Surathkal
"""Test APIs from topology packet operations"""

import os
import unittest
from os.path import exists
from nest.topology import Node, connect
from nest.clean_up import delete_namespaces
from nest.topology_map import TopologyMap

# pylint: disable=invalid-name
# pylint: disable=missing-docstring


class TestTopologyPacketOps(unittest.TestCase):
    # Add rate in percent to get packet duplicated.
    def setUp(self):
        self.n0 = Node("n0")
        self.n1 = Node("n1")

        (self.n0_n1, self.n1_n0) = connect(self.n0, self.n1)

        self.n0_n1.set_address("10.0.0.1/24")
        self.n1_n0.set_address("10.0.0.2/24")

    # Add rate in percent to get packet duplicated.
    def test_packet_duplication(self):
        self.n0_n1.set_packet_duplication("20%")
        status = self.n0.ping("10.0.0.2")

        self.assertTrue(status)

    def test_packet_reordering(self):
        self.n0_n1.set_attributes("10mbit", "10ms")
        self.n1_n0.set_attributes("10mbit", "5ms")

        self.n0_n1.set_packet_reordering("10ms", "25%", gap=5)

        self.n0.ping("10.0.0.2", packets=1)  # build ARP table before preload is used.
        status = self.n0.ping("10.0.0.2", preload=10, packets=10)

        self.assertTrue(status)

    def test_packet_capture(self):
        self.n0_n1.set_attributes("10mbit", "10ms")
        initial_status = exists("packet_capture.pcap")
        self.n1.capture_packets(
            interface=self.n1_n0, packet_count=10, output_file="packet_capture.pcap"
        )
        self.n0.ping("10.0.0.2", packets=10)

        status = exists("packet_capture.pcap")
        self.assertTrue(status)
        if initial_status is False and status is True:
            os.remove("packet_capture.pcap")

    def tearDown(self):
        delete_namespaces()
        TopologyMap.delete_all_mapping()


if __name__ == "__main__":
    unittest.main()
