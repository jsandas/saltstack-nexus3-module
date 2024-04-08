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
        "apt": {
            "result": True,
            "changes": {
                "type": "File",
                "softQuota": None
            },
            "comment": "",
        },
        "docker": {
            "result": True,
            "changes": {
                "type": "File",
                "softQuota": None
            },
            "comment": "",
        },
        "maven": {
            "result": True,
            "changes": {
                "type": "File",
                "softQuota": {
                    "limit": 1000000000,
                    "type": "spaceRemainingQuota"
                },
            },
            "comment": "",
        },
        "s3blobstore": {
            "result": True,
            "changes": {
                "type": "S3",
                "softQuota": None,
            },
            "comment": "",
        },
    }
}

def test_annonymous_access_state():
    ret = client.cmd('test.minion', 'state.apply', ['nexus3.anonymous_access'])
    # pp.pprint(ret['test.minion'])
    for key, values in state_test_data['results'].items():
        id = f"nexus3_blobstores_|-create_blobstore_{key}_|-{key}_|-present"
        output = ret['test.minion'][id]
        assert values['result'] == output['result'], f"wrong state result! expected: \"{values['result']}\" got: \"{output['result']}\""
        assert values['comment'] == output['comment'], f"wrong state comment! expected: \"{values['comment']}\" got: \"{output['comment']}\""
        assert values['changes']['type'] == output['changes']['blobstore']['type'], f"wrong type result! expected: \"{values['changes']['type']}\" got: \"{output['changes']['blobstore']['type']}\""
        assert values['changes']['softQuota'] == output['changes']['blobstore']['softQuota'], f"wrong type result! expected: \"{values['changes']['softQuota']}\" got: \"{output['changes']['blobstore']['softQuota']}\""
