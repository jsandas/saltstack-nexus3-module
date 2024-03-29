'''
execution module for Nexus 3 security realms

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

realms_path = 'v1/security/realms'


def list_active():
    '''
    CLI Example::

    .. code-block:: bash

        salt myminion nexus3_realms.list_active
    '''

    ret = {
        'realms': {},
    }

    path = realms_path + '/active'
    nc = nexus3.NexusClient()

    resp = nc.get(path)

    if resp['status'] == 200:
        ret['realms'] = json.loads(resp['body'])
    else:
        ret['comment'] = 'could not retrieve active realms.'
        ret['error'] = {
            'code': resp['status'],
            'msg': resp['body']
        }

    return ret


def list_all():
    '''
    CLI Example::

    .. code-block:: bash

        salt myminion nexus3_realms.list_all
    '''

    ret = {
        'realms': {},
    }

    path = realms_path + '/available'
    nc = nexus3.NexusClient()

    resp = nc.get(path)

    if resp['status'] == 200:
        ret['realms'] = json.loads(resp['body'])
    else:
        ret['comment'] = 'could not retrieve available realms.'
        ret['error'] = {
            'code': resp['status'],
            'msg': resp['body']
        }

    return ret


def reset():
    '''
    Resets realms to default

    CLI Example::

    .. code-block:: bash

        salt myminion nexus3_realms.reset
    '''

    ret = {
        'realms': {},
    }

    path = realms_path + '/active'

    # these are the defaults enabled
    # upon first start of Nexus 3
    payload = [
        'NexusAuthenticatingRealm', 
        'NexusAuthorizingRealm',
        'NpmToken'
    ]

    nc = nexus3.NexusClient()

    resp = nc.put(path, payload)

    if resp['status'] == 204:
        ret['realms'] = list_active()['realms']
        ret['comment'] = 'realms reset to defaults.'
    else:
        ret['comment'] = 'could not reset realms.'
        ret['error'] = {
            'code': resp['status'],
            'msg': resp['body']
        }

    return ret


def update(realms=[]):
    '''
    realms (list):
        list of realms in order they should be used 
        .. note::
            Include all desired realms in list as this will override
            the current list

    CLI Example::

    .. code-block:: bash

        salt myminion nexus3_realms.update realms="['NexusAuthenticatingRealm','NexusAuthorizingRealm','NpmToken','DockerToken']"
    '''

    ret = {
        'realms': {},
    }

    path = realms_path + '/active'

    nc = nexus3.NexusClient()

    resp = nc.put(path, realms)

    if resp['status'] == 204:
        ret['realms'] = list_active()['realms']
        ret['comment'] = 'realms updated.'
    else:
        ret['comment'] = 'could not update realms.'
        ret['error'] = {
            'code': resp['status'],
            'msg': resp['body']
        }

    return ret