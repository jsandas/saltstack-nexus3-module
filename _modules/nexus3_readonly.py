'''
execution module for Nexus 3 read-only settings

:version: v0.2.2

:configuration: In order to connect to Nexus 3, certain configuration is required
    in /etc/salt/minion on the relevant minions.

    Example:
      nexus3:
        hostname: '127.0.0.1:8081'
        username: 'admin'
        password: 'admin123'

'''

import json
import logging

import nexus3

log = logging.getLogger(__name__)

__outputter__ = {
    'sls': 'highstate',
    'apply_': 'highstate',
    'highstate': 'highstate',
}

read_only_path = 'v1/read-only'


def describe():
    '''
    CLI Example::

    .. code-block:: bash

        salt myminion nexus3_readonly.describe
    '''

    ret = {
        'read-only': {},
    }

    path = read_only_path

    nc = nexus3.NexusClient()

    resp = nc.get(path)

    if resp['status'] == 200:
        ret['read-only'] = json.loads(resp['body'])
    else:
        ret['comment'] = 'could not get read-only state.'
        ret['error'] = {
            'code': resp['status'],
            'msg': resp['body']
        }

    return ret


def enabled(state, force_release=False):
    '''
    state (bool):
        enable or disable read-only [True|False]

    force_release (bool):
        force release of read-only [True|False] (Default: False)

    CLI Example::

    .. code-block:: bash

        salt myminion nexus3_readonly.enabled True
        salt myminion nexus3_readonly.enabled state=False
    '''
    ret = {
        'read-only': False,
    }

    if state:
        path = read_only_path + '/freeze'
    elif force_release:
        path = read_only_path + '/force_release'
    else:
        path = read_only_path + '/release'

    nc = nexus3.NexusClient()

    resp = nc.post(path)

    if resp['status'] == 204:
        ret['read-only'] = state
    else:
        ret['comment'] = 'could not set read-only mode'
        ret['error'] = {
            'code': resp['status'],
            'msg': resp['body']
        }

    return ret
