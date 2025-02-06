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

    # reset
    test_cleanup()

def test_error_anonymous_access():
    ret = client.cmd('test.minion', 'nexus3_anonymous_access.enable', ['enabled=f'])
    # print(ret)
    assert ret['test.minion']['error'] == '\"f\" is not a boolean value','error value is incorrect'

## States Integration Tests ##
state_test_data = {
    "results": {
        "changes": {
            "anonymous_access": {
                "enabled": True,
                "userId": "anonymous",
                "realmName": "NexusAuthorizingRealm"
            },
            "error": None
        },
        "result": True,
    }
}

def test_annonymous_access_state():
    test_cleanup()
    ret = client.cmd('test.minion', 'state.apply', ['nexus3.anonymous_access'])
#     # pp.pprint(ret['test.minion'])
    id = f"nexus3_security_|-set_anonymous_access_true_|-set_anonymous_access_true_|-anonymous_access"
    output = ret['test.minion'][id]
    assert state_test_data['results']['result'] == output['result'], f"wrong state result! expected: \"{state_test_data['results']['result']}\" got: \"{output['result']}\""
    assert state_test_data['results']['changes'] == output['changes'], f"wrong type result! expected: \"{state_test_data['results']['changes']['type']}\" got: \"{output['changes']['blobstore']['type']}\""
