'''
execution module for Nexus 3 security annonymous access

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

anon_access_path = 'v1/security/anonymous'


def describe():
    '''
    CLI Example::

    .. code-block:: bash

        salt myminion nexus3_anonymous_access.describe
    '''

    ret = {
        'anonymous_access': {},
    }

    nc = nexus3.NexusClient()

    resp = nc.get(anon_access_path)

    if resp['status'] == 200:
        ret['anonymous_access'] = json.loads(resp['body'])
    else:
        ret['comment'] = 'Failed to retrieve anonymous access settings.'
        ret['error'] = {
            'code': resp['status'],
            'msg': resp['body']
        }

    return ret


def enable(enabled):
    '''
    enabled (bool):
        enable or disable anonymous access [True|False]

    CLI Example::

    .. code-block:: bash

        salt myminion nexus3_anonymous_access.enable True
    '''

    ret = {
        'anonymous_access': {},
        'error': None
    }

    payload = {
        'enabled': enabled,
        'userId': 'anonymous',
        'realmName': 'NexusAuthorizingRealm'
    }

    if not isinstance(enabled, bool):
        ret['error'] = f'\"{enabled}\" is not a boolean value'     
        return ret 

    nc = nexus3.NexusClient()

    resp = nc.put(anon_access_path, payload)

    if resp['status'] == 200:
        ret['anonymous_access'] = json.loads(resp['body'])
    else:
        ret['error'] = {
            'http_code': resp['status'],
            'msg': json.loads(resp['body'])
        }

    return ret
