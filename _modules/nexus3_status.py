''''
execution module for Nexus 3 status check

:version: v0.2.1

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

status_path = 'v1/status'


def check():
    '''
    Health check endpoint that returns the results of the system status checks

    CLI Example::

    .. code-block:: bash

        salt myminion nexus3_status.check
    '''

    ret = {
        'status': {},
    }

    path = status_path + '/check'

    nc = nexus3.NexusClient()

    resp = nc.get(path)

    if resp['status'] == 200:
        ret['status'] = json.loads(resp['body'])
    else:
        ret['comment'] = 'could not get status checks'
        ret['error'] = {
            'code': resp['status'],
            'msg': resp['body']
        }

    return ret
