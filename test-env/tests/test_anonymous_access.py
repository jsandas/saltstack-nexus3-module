#!/usr/bin/env python3

import salt.client

client = salt.client.LocalClient()


def test_cleanup():
    # clean the slate
    client.cmd('test.minion', 'nexus3_anonymous_access.enable', ['enabled=False'])

def test_describe_anonymous_access():
    ret = client.cmd('test.minion', 'nexus3_anonymous_access.describe')
    # print(ret)
    assert ret['test.minion']['anonymous_access'] != {},'anonymous_access is empty'
    assert ret['test.minion']['anonymous_access']['enabled'] == False,'anonymous_access should be disabled'

def test_update_anonymous_access():
    ret = client.cmd('test.minion', 'nexus3_anonymous_access.enable', ['enabled=True'])
    # print(ret)
    assert ret['test.minion']['anonymous_access'] != {},'anonymous_access is empty'
    assert ret['test.minion']['anonymous_access']['enabled'] == True,'anonymous_access should be enabled'

def test_error_anonymous_access():
    ret = client.cmd('test.minion', 'nexus3_anonymous_access.enable', ['enabled=f'])
    # print(ret)
    assert ret['test.minion']['error'] == '\"f\" is not a boolean value','error value is incorrect'
