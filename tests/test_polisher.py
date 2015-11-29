#!/usr/bin/env python

"""
Tests for `polisher` module.
"""

import unittest

from libcloud.compute.types import NodeState

from plumbery.engine import PlumberyFittings
from plumbery.polisher import PlumberyPolisher


class FakeEngine():

    def get_shared_secret(self):
        return 'nuts'


class FakeFittings(PlumberyFittings):
    locationId = 'EU6'
    rub = [{'beachhead': '10.1.10.9'}, {'beachhead': '10.1.10.10'}]


class FakeFacility():
    fittings = FakeFittings()


class FakeNode():
    name = 'fake'
    id = '1234'
    state = NodeState.RUNNING
    private_ips = ['10.100.100.100']
    extra = {'datacenterId': 'EU6', 'description': '#fake description with #tags', 'status': {}}

fakeNodeSettings = {
    'name': 'stackstorm',
    'description': 'fake',
    'appliance': 'RedHat 6 64-bit 4 CPU',
    'rub': ['rub.update.sh', 'rub.docker.sh']}

fakeAnsibleConfiguration = {
    'reap': 'test_polisher_ansible.yaml'}

fakeRubConfiguration = {
    'reap': 'test_polisher_rub.yaml',
    'key': 'test_polisher.pub'}

fakeSpitConfiguration = {
    'reap': 'test_polisher_spit.yaml'}


class TestPlumberyPolisher(unittest.TestCase):

    def test_ansible(self):
        self.polisher = PlumberyPolisher.from_shelf('ansible', fakeAnsibleConfiguration)
        self.polisher.go(FakeEngine())
        self.polisher.move_to(FakeFacility())
        self.polisher.shine_node(FakeNode(), fakeNodeSettings)
        self.polisher.reap()

    def test_rub(self):
        self.polisher = PlumberyPolisher.from_shelf('rub', fakeRubConfiguration)
        self.polisher.go(FakeEngine())
        self.polisher.move_to(FakeFacility())
        self.polisher.shine_node(FakeNode(), fakeNodeSettings)
        self.polisher.reap()

    def test_spit(self):
        self.polisher = PlumberyPolisher.from_shelf('spit', fakeSpitConfiguration)
        self.polisher.go(FakeEngine())
        self.polisher.move_to(FakeFacility())
        self.polisher.shine_node(FakeNode(), fakeNodeSettings)
        self.polisher.reap()

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
