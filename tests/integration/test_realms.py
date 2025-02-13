#!/usr/bin/env python3

import salt.client

client = salt.client.LocalClient()


def test_cleanup():
    # clean the slate
    client.cmd('test.minion', 'nexus3_realms.reset')

def test_update_realms():
    ret = client.cmd('test.minion', 'nexus3_realms.update', [['NexusAuthenticatingRealm','DockerToken']])
    # print(ret)
    assert ret['test.minion']['realms'] != {},'realms is empty'
    assert ret['test.minion']['realms']== ['NexusAuthenticatingRealm','DockerToken'],'realms is incorrect'


def test_active_realms():
    client.cmd('test.minion', 'nexus3_realms.update', [['NexusAuthenticatingRealm','DockerToken','NpmToken']])
    ret = client.cmd('test.minion', 'nexus3_realms.list_active')
    # print(ret)
    assert ret['test.minion']['realms'] != {},'realms is empty'
    assert ret['test.minion']['realms'] == ['NexusAuthenticatingRealm','DockerToken','NpmToken'],'realms is incorrect'
