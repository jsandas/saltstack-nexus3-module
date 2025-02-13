#!/usr/bin/env python3

import salt.client

client = salt.client.LocalClient()


def test_cleanup():
    # clean the slate
    client.cmd('test.minion', 'nexus3_roles.delete', ['testing1'])
    client.cmd('test.minion', 'nexus3_roles.delete', ['testing2'])
    
def test_create_roles():
    ret = client.cmd('test.minion', 'nexus3_roles.create', ["name=testing1", "description='test role 1'", "roles=['nx-admin']"])
    # print(ret)
    assert ret['test.minion']['role'] != {},'roles is empty'
    assert ret['test.minion']['role']['name'] == 'testing1','role name is incorrect'
    assert ret['test.minion']['role']['roles'] == ['nx-admin'],'roles is incorrect'

    ret = client.cmd('test.minion', 'nexus3_roles.create', ["name=testing2", "description='test role 2'",
                "privileges=['nx-healthcheck-read','nx-search-read','nx-repository-view-*-*-read','nx-repository-view-*-*-browse']"])
    # print(ret)
    assert ret['test.minion']['role'] != {},'roles is empty'
    assert ret['test.minion']['role']['name'] == 'testing2','role name is incorrect'
    assert len(ret['test.minion']['role']['privileges']) == 4,'privileges is incorrect'

def test_update_roles():
    ret = client.cmd('test.minion', 'nexus3_roles.update', ["name=testing1", "description='test role 1'", "roles=['nx-anonymous']"])
    # print(ret)
    assert ret['test.minion']['role'] != {},'roles is empty'
    assert ret['test.minion']['role']['roles'] == ['nx-anonymous'],'roles is incorrect'
