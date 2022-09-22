''''
execution module for Nexus 3 tasks

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

tasks_path = 'v1/tasks'


def describe(id):
    '''
    id (str):
        task id

    CLI Example::

    .. code-block:: bash

        salt myminion nexus3_tasks.describe id=512be2c3-aa04-448f-b0ce-2047eee34903
    '''

    ret = {
        'task': {},
    }

    path = tasks_path + '/' + id

    nc = nexus3.NexusClient()

    resp = nc.get(path)

    if resp['status'] == 200:
        ret['task'] = json.loads(resp['body'])
    else:
        ret['comment'] = 'could not get task: {}'.format(id)
        ret['error'] = {
            'code': resp['status'],
            'msg': resp['body']
        }

    return ret


def list_all():
    '''
    CLI Example::

    .. code-block:: bash

        salt myminion nexus3_tasks.list_all
    
    TODO: 
        add support for the continuationToken for larger lists
    '''

    ret = {
        'tasks': {},
    }

    path = tasks_path

    nc = nexus3.NexusClient()

    resp = nc.get(path)

    if resp['status'] == 200:
        ret['tasks'] = json.loads(resp['body'])
    else:
        ret['comment'] = 'could not get tasks'
        ret['error'] = {
            'code': resp['status'],
            'msg': resp['body']
        }

    return ret


def run(id):
    '''
    id (str):
        task id

    CLI Example::

    .. code-block:: bash

        salt myminion nexus3_tasks.run id=512be2c3-aa04-448f-b0ce-2047eee34903
    '''

    ret = {
        'task': {},
    }

    path = tasks_path + '/' + id + '/run'

    nc = nexus3.NexusClient()

    resp = nc.post(path, None)

    if resp['status'] == 204:
        ret['task'] = 'ran task: {}'.format(id)
    else:
        ret['comment'] = 'could not run task: {}'.format(id)
        if resp['status'] == 404:
            msg = 'task not found'
        elif resp['status'] == 405:
            msg = 'task is disabled'
        else:
            msg = resp['body']

        ret['error'] = {
            'code': resp['status'],
            'msg': msg
        }

    return ret


def stop(id):
    '''
    id (str):
        task id

    CLI Example::

    .. code-block:: bash

        salt myminion nexus3_tasks.stop id=512be2c3-aa04-448f-b0ce-2047eee34903
    '''

    ret = {
        'task': {},
    }

    path = tasks_path + '/' + id + '/run'

    nc = nexus3.NexusClient()

    resp = nc.post(path, None)

    if resp['status'] == 204:
        ret['task'] = 'stopped task: {}'.format(id)
    else:
        ret['comment'] = 'could not stop task: {}'.format(id)
        if resp['status'] == 404:
            msg = 'task not found'
        elif resp['status'] == 405:
            msg = 'task is disabled'
        else:
            msg = resp['body']

        ret['error'] = {
            'code': resp['status'],
            'msg': msg
        }

    return ret