#!/usr/bin/env python

import salt.client

client = salt.client.LocalClient()

def test_list_all():
    ret = client.cmd('test.minion', 'nexus3_repositories.list_all')
    print(ret)
    assert len(ret['test.minion']['repositories']) >= 7,'not enough repositories found'


def test_hosted():
    ret = client.cmd('test.minion', 'nexus3_repositories.hosted', ['name=test-yum-hosted','format=yum','yum_repodata_depth=3','yum_deploy_policy=permissive'])
    print(ret)
    data = ret['test.minion']['repository']
    assert data['name'] == 'test-yum-hosted','repo name is incorrect'
    assert data['yum']['deployPolicy'] == 'PERMISSIVE','deployPolicy is incorrect'
    assert data['yum']['repodataDepth'] == 3,'repodataDepth is incorrect'


def test_group():
    ret = client.cmd('test.minion', 'nexus3_repositories.group', ['name=test-yum-group','format=yum','group_members=["test-yum-hosted"]'])
    print(ret)
    data = ret['test.minion']['repository']
    assert data['name'] == 'test-yum-group','repo name is incorrect'
    assert data['group']['memberNames'] == ['test-yum-hosted'],'memberNames is incorrect'


def test_proxy():
    ret = client.cmd('test.minion', 'nexus3_repositories.proxy', ['name=test-yum-proxy','format=yum','remote_url=https://randomurl.com'])
    print(ret)
    data = ret['test.minion']['repository']
    assert data['name'] == 'test-yum-proxy','repo name is incorrect'
    assert data['proxy']['remoteUrl'] == 'https://randomurl.com','remoteUrl is incorrect'
    assert data['httpClient']['authentication'] is None,'authentication is incorrect'

def test_proxy_with_auth():
    ret = client.cmd('test.minion', 'nexus3_repositories.proxy', ['name=test-yum-proxy_auth','format=yum','remote_url=https://randomurlauth.com','remote_username=test_user','remote_password=test_password'])
    print(ret)
    data = ret['test.minion']['repository']
    assert data['name'] == 'test-yum-proxy_auth','repo name is incorrect'
    assert data['proxy']['remoteUrl'] == 'https://randomurlauth.com','remoteUrl is incorrect'
    assert data['httpClient']['authentication']['type'] == 'username','authentication type is incorrect'
    assert data['httpClient']['authentication']['username'] == 'test_user','authentication username is incorrect'

def test_describe():
    ret = client.cmd('test.minion', 'nexus3_repositories.describe', ['name=test-yum-hosted'])
    print(ret)
    assert ret['test.minion']['repository'] != {},'data is empty'
    assert ret['test.minion']['repository']['name'] == 'test-yum-hosted','repository test-yum not found'
    assert ret['test.minion']['repository']['format'] == 'yum','format found'
    assert ret['test.minion']['repository']['type'] == 'hosted','type found'


# clean the slate
client.cmd('test.minion', 'nexus3_repositories.delete', ['name=test-yum-hosted'])
client.cmd('test.minion', 'nexus3_repositories.delete', ['name=test-yum-group'])
client.cmd('test.minion', 'nexus3_repositories.delete', ['name=test-yum-proxy'])
client.cmd('test.minion', 'nexus3_repositories.delete', ['name=test-yum-proxy_auth'])

test_list_all()

test_hosted()

test_group()

test_proxy() 

test_proxy_with_auth()

test_describe()