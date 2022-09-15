#!/usr/bin/env python3

import salt.client

client = salt.client.LocalClient()

def test_describe_readonly():
    ret = client.cmd('test.minion', 'nexus3_readonly.describe')
    print(ret)
    assert ret['test.minion']['read-only'] != {},'read-only is empty'
    assert ret['test.minion']['read-only']['frozen'] == False,'read-only should be disabled'


def test_enable_readonly():
    ret = client.cmd('test.minion', 'nexus3_readonly.enabled', ['state=True'])
    print(ret)
    assert ret['test.minion']['read-only'] != {},'read-only is empty'
    assert ret['test.minion']['read-only'] == True,'read-only should be enabled'


def test_disable_readonly():
    ret = client.cmd('test.minion', 'nexus3_readonly.enabled', ['state=False'])
    print(ret)
    assert ret['test.minion']['read-only'] != {},'read-only is empty'
    assert ret['test.minion']['read-only'] == False,'read-only should be disabled'

# clean the slate
client.cmd('test.minion', 'nexus3_readonly.enabled', ['state=False'])

test_describe_readonly()

test_enable_readonly()

test_disable_readonly()