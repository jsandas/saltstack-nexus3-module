#!/usr/bin/env python3

import salt.client

client = salt.client.LocalClient()


# clean the slate
def test_cleanup():
    client.cmd('test.minion', 'nexus3_repositories.delete', ['name=test-yum-hosted'])
    client.cmd('test.minion', 'nexus3_repositories.delete', ['name=test-yum-group'])
    client.cmd('test.minion', 'nexus3_repositories.delete', ['name=test-yum-proxy'])
    client.cmd('test.minion', 'nexus3_repositories.delete', ['name=test-apt-proxy'])
    client.cmd('test.minion', 'nexus3_repositories.delete', ['name=test-yum-proxy_auth'])

def test_list_all():
    ret = client.cmd('test.minion', 'nexus3_repositories.list_all')
    # print(ret)
    assert len(ret['test.minion']['repositories']) >= 7,'not enough repositories found'

def test_hosted():
    ret = client.cmd('test.minion', 'nexus3_repositories.hosted', ['name=test-yum-hosted','format=yum','yum_repodata_depth=3','yum_deploy_policy=permissive'])
    # print(ret)
    data = ret['test.minion']['repository']
    assert data['name'] == 'test-yum-hosted','repo name is incorrect'
    assert data['yum']['deployPolicy'] == 'PERMISSIVE','deployPolicy is incorrect'
    assert data['yum']['repodataDepth'] == 3,'repodataDepth is incorrect'
    
    ret = client.cmd('test.minion', 'nexus3_repositories.hosted', ['name=test-apt-hosted','format=apt','apt_gpg_priv_key=LS0tLS1CRUdJTiBQR1AgUFJJVkFURSBLRVkgQkxPQ0stLS0tLQoKbFFIWUJHTWY1YU1CQkFETlgyRTBVZlcvUHdEczB6bGNIRnExeVhaMFppS2ZXRTgyU0lURU51UHcwVzRuc1o2dgpKRnNzMk96MWlrZWpNOEN1SFNmZXVkWkE5TkFsRjJHbDQ3R2xOQzlORlFxWHVLMlh2Z0F3UXFFWkkvaWhXRzlmCmxxdFBDS2tHTHFzSnFjTmU1LzRlVklmUWxSdUl4R0tlbWRLV3htUFlaNkcvcEY5Zng4aENyQ1ViQVFBUkFRQUIKQUFQOUZTaWVleVYyakIyUm10U29ORFUzbzBMK1VUKzBrWFluc3hBRm5iR0tDbVdKVTgyWTY3SnpNa3VuSGlVQQovRzk0aW5lMmc5dmhsdytoNGpCbWZ4RFdYRitpcm83K1AzaE9MSUxQVDhiNWpVN1BQV3lzSi8wc3hieDJ5bXR4CkdkQWdobTFNd1FIUEVYQkx1dkpQQmlZeUhlOVNEa0FtM1J2Ymx6eWVEV05xTjRFQ0FPRVBPRlNnVUV4YXpEdTEKRGlYZkNhWGZLN1liQy90ZGIzNjNvNkpZOGVCVmlUeHhSRmdQdW9DMENFOGxqZzJBRmJMMXc2OEwzbUZ2TzZRTApkVDlpdk5NQ0FPbWJTK1JUNUVzTVBpQXRUMThpV21YM0Jpc1EwRGc5L1lVNHRQZENId1VZRFBUVkd2TmQ0TGhOCm1NdzNTTVJ0Q2g3MDJKU1puNlJHeGN6SnhPQldsRnNDQU1TN2pCQytwQTEreUlwbC9FWjdmWElWNm8rRGZPQ3oKdzBaekg2TE9jMXpnbDRZZVhoTmR6SWVTcE1KaTg2bTArQlM0TW9IR1gwbGFhRnI4ZGVhZmVpNlprclFNZEdWegpkQzFuY0djdGEyVjVpTTRFRXdFS0FEZ1dJUVI0WWdNS2Z0TGMzZ3VVaE1mejR0U3lkOFdzVlFVQ1l4L2xvd0liCkF3VUxDUWdIQWdZVkNna0lDd0lFRmdJREFRSWVBUUlYZ0FBS0NSRHo0dFN5ZDhXc1ZRYWRBLzBmYlFYeE1MTjkKZ1dIeDZTVElRbElNN3prL2diQ2k4WFlVNVd3Zmt5bDR0bHdUWUMrUXVOb0luZ1ZXakQ3L0IzYUFQdEt3VGVOSwppck5tTnNNczNuTXZNdXgzQk9WYWdJREpqLy9YZ0gyOHE4WEt1VTlmTnJ4NnRQUkJVMWIxTjhTRld3OHcwMmplCm9mdE9ZbzhrUUFWSDR1cGZYekZvQldhNHdjVU0weEtPeUowQjJBUmpIK1dqQVFRQXBwMDFDMVAxb3ZFcjdaYTkKeTZTdWU2eFc2UHFpazJiM0dKWFJ4SGxpN1AzWEw5ZGtEWFNtZjVHOEtSdU5GMGRnY0J3ZTVtVEJNRjhta21kSApmZytQY3phUUNzY3FvS0I2b0JVTUlYWTArZWE1eWRYb2NTNytURmt0UWVNUjZEenR4d1RndC9SWHBwY3B5N3B4CmtBZktWYnV3a2RzUUg1bkJFajlORUtXdDZja0FFUUVBQVFBRC9SdFhUK1dRZlE0a21tdE9JYzRoczVwSzRTWXgKUHUyR1o0VUt6Tlg3ZjI3Wmh1N3NYeGhRTEtSaGcybVJnbGt3RnRTKzRKazVMblNrSUozRXdmZ2ZVSkE1S29zVgpNaUppUnpvK1U3L0Y2Mk45SHdHbHVCTGkrODdBV1BRYzc5WjZoQnA0eDBGZ1NCWWVLVWhvUytnZEI3TG5GWm5LCjRZbk5FbWdaQUY2aE1rS3BBZ0RGcmNsQ01Xc2pWZ3I3RnZuaVIvWWJOQmxIa05EckpkaEtwc1AvbUhlVXg3ejAKVzdZMU9jeEVMR0VsTjllZjA0QnJZTzdMcUE4UUk2QWFpcUwyRmVmZEFnRFh4U3htUy85UUk0alhUb0FmNmNxawpNcm4wQnhVdFRHdTR2aWlIc3dNVUlpallqUXlFV0cvVXhZanJVU2hTY3luQWFuZU1BelBvWEtLdW52NDc2OERkCkFnQzFmeDZDU1RDTUxNQXUwZlliSHdDaXNWMTNVZEJrbXhraThLdnEwMG5vVGRhY1lWMG0vU1IzOUhVWmNYcUIKRkNYbTQ4eDlsZVU4ZDNkdjV0SjFsOGp0bk5HSXRnUVlBUW9BSUJZaEJIaGlBd3ArMHR6ZUM1U0V4L1BpMUxKMwp4YXhWQlFKakgrV2pBaHNNQUFvSkVQUGkxTEozeGF4VlEwc0QvUlJJK3U2QkFHOHE0d0E4KzN6OFI5R3JCSlROCmhHTktiNHpDMU1PaklYbkVselNWWm1FTWFIVVlzajRqY3FsT2hBNFBzQ0JZM2dMSUc4cWsrMlpGcytSMFowREYKRTltaGJ5QVBWUEQxU0QyandHSTNINDhLcHVMSzVTZUhOWHZkdWxGaUdWRXlyczE2V3N6bG5sMmxPWjkzb0ovNApFUGtNc0FrWHhjUmRFVkJCCj10c2YxCi0tLS0tRU5EIFBHUCBQUklWQVRFIEtFWSBCTE9DSy0tLS0tCg=='])

def test_group():
    ret = client.cmd('test.minion', 'nexus3_repositories.group', ['name=test-yum-group','format=yum','group_members=["test-yum-hosted"]'])
    # print(ret)
    data = ret['test.minion']['repository']
    assert data['name'] == 'test-yum-group','repo name is incorrect'
    assert data['group']['memberNames'] == ['test-yum-hosted'],'memberNames is incorrect'

def test_proxy():
    ret = client.cmd('test.minion', 'nexus3_repositories.proxy', ['name=test-yum-proxy','format=yum','remote_url=https://randomurl.com'])
    # print(ret)
    data = ret['test.minion']['repository']
    assert data['name'] == 'test-yum-proxy','repo name is incorrect'
    assert data['proxy']['remoteUrl'] == 'https://randomurl.com','remoteUrl is incorrect'
    assert data['httpClient']['authentication'] is None,'authentication is incorrect'

    ret = client.cmd('test.minion', 'nexus3_repositories.proxy', ['name=test-apt-proxy','format=apt','remote_url=https://randomurl.com'])
    # print(ret)
    data = ret['test.minion']['repository']
    assert data['name'] == 'test-apt-proxy','repo name is incorrect'
    assert data['proxy']['remoteUrl'] == 'https://randomurl.com','remoteUrl is incorrect'
    assert data['apt']['flat'] == False,'apt flat is incorrect'

def test_proxy_with_auth():
    ret = client.cmd('test.minion', 'nexus3_repositories.proxy', ['name=test-yum-proxy_auth','format=yum','remote_url=https://randomurlauth.com','remote_username=test_user','remote_password=test_password'])
    # print(ret)
    data = ret['test.minion']['repository']
    assert data['name'] == 'test-yum-proxy_auth','repo name is incorrect'
    assert data['proxy']['remoteUrl'] == 'https://randomurlauth.com','remoteUrl is incorrect'
    assert data['httpClient']['authentication']['type'] == 'username','authentication type is incorrect'
    assert data['httpClient']['authentication']['username'] == 'test_user','authentication username is incorrect'

def test_describe():
    ret = client.cmd('test.minion', 'nexus3_repositories.describe', ['name=test-yum-hosted'])
    # print(ret)
    assert ret['test.minion']['repository'] != {},'data is empty'
    assert ret['test.minion']['repository']['name'] == 'test-yum-hosted','repository test-yum-hosted not found'
    assert ret['test.minion']['repository']['format'] == 'yum','wrong format found'
    assert ret['test.minion']['repository']['type'] == 'hosted','wrong type found'

    ret = client.cmd('test.minion', 'nexus3_repositories.describe', ['name=test-apt-proxy'])
    # print(ret)
    assert ret['test.minion']['repository'] != {},'data is empty'
    assert ret['test.minion']['repository']['name'] == 'test-apt-proxy','repository test-apt-proxy not found'
    assert ret['test.minion']['repository']['format'] == 'apt','wrong format found'
    assert ret['test.minion']['repository']['type'] == 'proxy','wrong type found'
    assert ret['test.minion']['repository']['apt']['flat'] == False,'apt flat is incorrect'


## States Integration Tests ##
state_test_apt_data = {
    "pillar": {
        "nexus3": {
            "repositories": {
                "apt-hosted": [
                    {"format": "apt"},
                    {"type": "hosted"},
                    {"apt_gpg_priv_key": "LS0tLS1CRUdJTiBQR1AgUFJJVkFURSBLRVkgQkxPQ0stLS0tLQoKbFFIWUJHTWY1YU1CQkFETlgyRTBVZlcvUHdEczB6bGNIRnExeVhaMFppS2ZXRTgyU0lURU51UHcwVzRuc1o2dgpKRnNzMk96MWlrZWpNOEN1SFNmZXVkWkE5TkFsRjJHbDQ3R2xOQzlORlFxWHVLMlh2Z0F3UXFFWkkvaWhXRzlmCmxxdFBDS2tHTHFzSnFjTmU1LzRlVklmUWxSdUl4R0tlbWRLV3htUFlaNkcvcEY5Zng4aENyQ1ViQVFBUkFRQUIKQUFQOUZTaWVleVYyakIyUm10U29ORFUzbzBMK1VUKzBrWFluc3hBRm5iR0tDbVdKVTgyWTY3SnpNa3VuSGlVQQovRzk0aW5lMmc5dmhsdytoNGpCbWZ4RFdYRitpcm83K1AzaE9MSUxQVDhiNWpVN1BQV3lzSi8wc3hieDJ5bXR4CkdkQWdobTFNd1FIUEVYQkx1dkpQQmlZeUhlOVNEa0FtM1J2Ymx6eWVEV05xTjRFQ0FPRVBPRlNnVUV4YXpEdTEKRGlYZkNhWGZLN1liQy90ZGIzNjNvNkpZOGVCVmlUeHhSRmdQdW9DMENFOGxqZzJBRmJMMXc2OEwzbUZ2TzZRTApkVDlpdk5NQ0FPbWJTK1JUNUVzTVBpQXRUMThpV21YM0Jpc1EwRGc5L1lVNHRQZENId1VZRFBUVkd2TmQ0TGhOCm1NdzNTTVJ0Q2g3MDJKU1puNlJHeGN6SnhPQldsRnNDQU1TN2pCQytwQTEreUlwbC9FWjdmWElWNm8rRGZPQ3oKdzBaekg2TE9jMXpnbDRZZVhoTmR6SWVTcE1KaTg2bTArQlM0TW9IR1gwbGFhRnI4ZGVhZmVpNlprclFNZEdWegpkQzFuY0djdGEyVjVpTTRFRXdFS0FEZ1dJUVI0WWdNS2Z0TGMzZ3VVaE1mejR0U3lkOFdzVlFVQ1l4L2xvd0liCkF3VUxDUWdIQWdZVkNna0lDd0lFRmdJREFRSWVBUUlYZ0FBS0NSRHo0dFN5ZDhXc1ZRYWRBLzBmYlFYeE1MTjkKZ1dIeDZTVElRbElNN3prL2diQ2k4WFlVNVd3Zmt5bDR0bHdUWUMrUXVOb0luZ1ZXakQ3L0IzYUFQdEt3VGVOSwppck5tTnNNczNuTXZNdXgzQk9WYWdJREpqLy9YZ0gyOHE4WEt1VTlmTnJ4NnRQUkJVMWIxTjhTRld3OHcwMmplCm9mdE9ZbzhrUUFWSDR1cGZYekZvQldhNHdjVU0weEtPeUowQjJBUmpIK1dqQVFRQXBwMDFDMVAxb3ZFcjdaYTkKeTZTdWU2eFc2UHFpazJiM0dKWFJ4SGxpN1AzWEw5ZGtEWFNtZjVHOEtSdU5GMGRnY0J3ZTVtVEJNRjhta21kSApmZytQY3phUUNzY3FvS0I2b0JVTUlYWTArZWE1eWRYb2NTNytURmt0UWVNUjZEenR4d1RndC9SWHBwY3B5N3B4CmtBZktWYnV3a2RzUUg1bkJFajlORUtXdDZja0FFUUVBQVFBRC9SdFhUK1dRZlE0a21tdE9JYzRoczVwSzRTWXgKUHUyR1o0VUt6Tlg3ZjI3Wmh1N3NYeGhRTEtSaGcybVJnbGt3RnRTKzRKazVMblNrSUozRXdmZ2ZVSkE1S29zVgpNaUppUnpvK1U3L0Y2Mk45SHdHbHVCTGkrODdBV1BRYzc5WjZoQnA0eDBGZ1NCWWVLVWhvUytnZEI3TG5GWm5LCjRZbk5FbWdaQUY2aE1rS3BBZ0RGcmNsQ01Xc2pWZ3I3RnZuaVIvWWJOQmxIa05EckpkaEtwc1AvbUhlVXg3ejAKVzdZMU9jeEVMR0VsTjllZjA0QnJZTzdMcUE4UUk2QWFpcUwyRmVmZEFnRFh4U3htUy85UUk0alhUb0FmNmNxawpNcm4wQnhVdFRHdTR2aWlIc3dNVUlpallqUXlFV0cvVXhZanJVU2hTY3luQWFuZU1BelBvWEtLdW52NDc2OERkCkFnQzFmeDZDU1RDTUxNQXUwZlliSHdDaXNWMTNVZEJrbXhraThLdnEwMG5vVGRhY1lWMG0vU1IzOUhVWmNYcUIKRkNYbTQ4eDlsZVU4ZDNkdjV0SjFsOGp0bk5HSXRnUVlBUW9BSUJZaEJIaGlBd3ArMHR6ZUM1U0V4L1BpMUxKMwp4YXhWQlFKakgrV2pBaHNNQUFvSkVQUGkxTEozeGF4VlEwc0QvUlJJK3U2QkFHOHE0d0E4KzN6OFI5R3JCSlROCmhHTktiNHpDMU1PaklYbkVselNWWm1FTWFIVVlzajRqY3FsT2hBNFBzQ0JZM2dMSUc4cWsrMlpGcytSMFowREYKRTltaGJ5QVBWUEQxU0QyandHSTNINDhLcHVMSzVTZUhOWHZkdWxGaUdWRXlyczE2V3N6bG5sMmxPWjkzb0ovNApFUGtNc0FrWHhjUmRFVkJCCj10c2YxCi0tLS0tRU5EIFBHUCBQUklWQVRFIEtFWSBCTE9DSy0tLS0tCg=="},
                ],
                "apt-proxy": [
                    {"format": "apt"},
                    {"type": "proxy"},
                    {"remote_url": "http://apt-proxy"},
                    {"apt_dist_name": "bionic"}, 
                    {"apt_flat_repo": True},
                    {"negative_cache_enabled": False}
                ],
                "apt-proxy-http-client": [
                    {"format": "apt"},
                    {"type": "proxy"},
                    {"remote_url": "http://apt-proxy"},
                    {"apt_dist_name": "bionic"}, 
                    {"http_timeout": 60},
                    {"http_user_agent": "test-client"}
                ],
            }
        }
    },
    "results": {
        "apt-hosted": {
            "result": True,
            "changes": {
                "name": "apt-hosted",
                "url": "http://nexus3:8081/repository/apt-hosted",
                "online": True,
                "storage": {
                    "blobStoreName": "default",
                    "strictContentTypeValidation": True,
                    "writePolicy": "ALLOW_ONCE"
                },
                "cleanup": None,
                "apt": {
                    "distribution": "bionic"
                },
                "aptSigning": None,
                "component": {
                    "proprietaryComponents": False
                },
                "format": "apt",
                "type": "hosted"
            },
            "comment": "",
        },
        "apt-proxy": {
            "result": True,
            "changes": {
                "name": "apt-proxy",
                "url": "http://nexus3:8081/repository/apt-proxy",
                "online": True,
                "storage": {
                    "blobStoreName": "default",
                    "strictContentTypeValidation": True,
                    "writePolicy": "ALLOW"
                },
                "cleanup": None,
                "apt": {
                    "distribution": "bionic",
                    "flat": True
                },
                "proxy": {
                    "remoteUrl": "http://apt-proxy",
                    "contentMaxAge": 1440,
                    "metadataMaxAge": 1440
                },
                "negativeCache": {
                    "enabled": False,
                    "timeToLive": 1440
                },
                "httpClient": {
                    "blocked": False,
                    "autoBlock": True,
                    "connection": {
                        "retries": None,
                        "userAgentSuffix": None,
                        "timeout": None,
                        "enableCircularRedirects": False,
                        "enableCookies": False,
                        "useTrustStore": False
                    },
                    "authentication": None
                },
                "routingRuleName": None,
                "format": "apt",
                "type": "proxy"
            },
            "comment": "",
        },
        "apt-proxy-http-client": {
            "result": True,
            "changes": {
                "name": "apt-proxy-http-client",
                "url": "http://nexus3:8081/repository/apt-proxy-http-client",
                "online": True,
                "storage": {
                    "blobStoreName": "default",
                    "strictContentTypeValidation": True,
                    "writePolicy": "ALLOW"
                },
                "cleanup": None,
                "apt": {
                    "distribution": "bionic",
                    "flat": False
                },
                "proxy": {
                    "remoteUrl": "http://apt-proxy",
                    "contentMaxAge": 1440,
                    "metadataMaxAge": 1440
                },
                "negativeCache": {
                    "enabled": True,
                    "timeToLive": 1440
                },
                "httpClient": {
                    "blocked": False,
                    "autoBlock": True,
                    "connection": {
                        "retries": None,
                        "userAgentSuffix": "test-client",
                        "timeout": 60,
                        "enableCircularRedirects": False,
                        "enableCookies": False,
                        "useTrustStore": False
                    },
                    "authentication": None
                },
                "routingRuleName": None,
                "format": "apt",
                "type": "proxy"
            },
            "comment": "",
        },
    }
}

def test_apt_repository_state():
    pillar = state_test_apt_data['pillar']
    ret = client.cmd('test.minion', 'state.apply', ['nexus3.repositories', f'pillar={pillar}'])
    # print(ret['test.minion'])
    for key, values in state_test_apt_data['results'].items():
        id = f"nexus3_repositories_|-repositories_{key}_|-{key}_|-present"
        output = ret['test.minion'][id]
        assert values['result'] == output['result'], f"wrong state result! expected: \"{values['result']}\" got: \"{output['result']}\""
        assert values['comment'] == output['comment'], f"wrong state comment! expected: \"{values['comment']}\" got: \"{output['comment']}\""
        assert values['changes'] == output['changes'], f"wrong changes result! expected: \"{values['changes']}\" got: \"{output['changes']}\""


state_test_docker_data = {
    "pillar": {
        "nexus3": {
            "repositories": {
                "docker-hosted": [
                    {"format": "docker"},
                    {"type": "hosted"},
                    {"docker_http_port": 5000},
                ],
                "docker-proxy": [
                    {"format": "docker"},
                    {"type": "proxy"},
                    {"remote_url": "https://registry-1.docker.io"},
                    {"docker_http_port": 5001},
                    {"docker_force_auth": False},
                    {"docker_index_type": "HUB"},
                ]
            }
        }
    },
    "results": {
        "docker-hosted": {
            "result": True,
            "changes": {
                "name": "docker-hosted",
                "url": "http://nexus3:8081/repository/docker-hosted",
                "online": True,
                "storage": {
                    "blobStoreName": "default",
                    "strictContentTypeValidation": True,
                    "writePolicy": "ALLOW_ONCE",
                    "latestPolicy": False
                },
                "cleanup": None,
                "docker": {
                    "v1Enabled": False,
                    "forceBasicAuth": True,
                    "httpPort": 5000,
                    "httpsPort": None,
                    "subdomain": None
                },
                "component": {
                    "proprietaryComponents": False
                },
                "format": "docker",
                "type": "hosted"
            },
            "comment": ""
        },
        "docker-proxy": {
            "result": True,
            "changes": {
                "name": "docker-proxy",
                "url": "http://nexus3:8081/repository/docker-proxy",
                "online": True,
                "storage": {
                    "blobStoreName": "default",
                    "strictContentTypeValidation": True,
                    "writePolicy": "ALLOW"
                },
                "cleanup": None,
                "docker": {
                    "v1Enabled": False,
                    "forceBasicAuth": False,
                    "httpPort": 5001,
                    "httpsPort": None,
                    "subdomain": None
                },
                "dockerProxy": {
                    "indexType": "HUB",
                    "indexUrl": None,
                    "cacheForeignLayers": None,
                    "foreignLayerUrlWhitelist": []
                },
                "proxy": {
                    "remoteUrl": "https://registry-1.docker.io",
                    "contentMaxAge": 1440,
                    "metadataMaxAge": 1440
                },
                "negativeCache": {
                    "enabled": True,
                    "timeToLive": 1440
                },
                "httpClient": {
                    "blocked": False,
                    "autoBlock": True,
                    "connection": {
                        "retries": None,
                        "userAgentSuffix": None,
                        "timeout": None,
                        "enableCircularRedirects": False,
                        "enableCookies": False,
                        "useTrustStore": False
                    },
                    "authentication": None
                },
                "routingRuleName": None,
                "format": "docker",
                "type": "proxy"
            },
            "comment": "",
        },
    }
}

def test_docker_repository_state():
    pillar = state_test_docker_data['pillar']
    ret = client.cmd('test.minion', 'state.apply', ['nexus3.repositories', f'pillar={pillar}'])
    # print(ret['test.minion'])
    for key, values in state_test_docker_data['results'].items():
        id = f"nexus3_repositories_|-repositories_{key}_|-{key}_|-present"
        output = ret['test.minion'][id]
        assert values['result'] == output['result'], f"wrong state result! expected: \"{values['result']}\" got: \"{output['result']}\""
        assert values['comment'] == output['comment'], f"wrong state comment! expected: \"{values['comment']}\" got: \"{output['comment']}\""
        assert values['changes'] == output['changes'], f"wrong type result! expected: \"{values['changes']}\" got: \"{output['changes']}\""


state_test_raw_data = {
    "pillar": {
        "nexus3": {
            "repositories": {
                "raw-hosted": [
                    {"format": "raw"},
                    {"type": "hosted"},
                ],
                "raw-proxy": [
                    {"format": "raw"},
                    {"type": "proxy"},
                    {"remote_url": "https://registry-1.docker.io"},
                ]
            }
        }
    },
    "results": {
        "raw-hosted": {
            "result": True,
            "changes": {
                "name": "raw-hosted",
                "url": "http://nexus3:8081/repository/raw-hosted",
                "online": True,
                "storage": {
                    "blobStoreName": "default",
                    "strictContentTypeValidation": True,
                    "writePolicy": "ALLOW_ONCE"
                },
                "cleanup": None,
                "component": {
                    "proprietaryComponents": False
                },
                "raw": {
                    "contentDisposition": "ATTACHMENT"
                },
                "format": "raw",
                "type": "hosted"
            },
            "comment": ""
        },
        "raw-proxy": {
            "result": True,
            "changes": {
                "name": "raw-proxy",
                "url": "http://nexus3:8081/repository/raw-proxy",
                "online": True,
                "storage": {
                    "blobStoreName": "default",
                    "strictContentTypeValidation": True,
                    "writePolicy": "ALLOW"
                },
                "cleanup": None,
                "proxy": {
                    "remoteUrl": "https://registry-1.docker.io",
                    "contentMaxAge": 1440,
                    "metadataMaxAge": 1440
                },
                "negativeCache": {
                    "enabled": True,
                    "timeToLive": 1440
                },
                "httpClient": {
                    "blocked": False,
                    "autoBlock": True,
                    "connection": {
                        "retries": None,
                        "userAgentSuffix": None,
                        "timeout": None,
                        "enableCircularRedirects": False,
                        "enableCookies": False,
                        "useTrustStore": False
                    },
                    "authentication": None
                },
                "routingRuleName": None,
                "raw": {
                    "contentDisposition": "ATTACHMENT"
                },
                "format": "raw",
                "type": "proxy"
            },
            "comment": "",
        },
    }
}

def test_raw_repository_state():
    pillar = state_test_raw_data['pillar']
    ret = client.cmd('test.minion', 'state.apply', ['nexus3.repositories', f'pillar={pillar}'])
    # print(ret['test.minion'])
    for key, values in state_test_raw_data['results'].items():
        id = f"nexus3_repositories_|-repositories_{key}_|-{key}_|-present"
        output = ret['test.minion'][id]
        assert values['result'] == output['result'], f"wrong state result! expected: \"{values['result']}\" got: \"{output['result']}\""
        assert values['comment'] == output['comment'], f"wrong state comment! expected: \"{values['comment']}\" got: \"{output['comment']}\""
        assert values['changes'] == output['changes'], f"wrong type result! expected: \"{values['changes']}\" got: \"{output['changes']}\""
