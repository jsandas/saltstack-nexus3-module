'''
execution module for Nexus 3 security roles

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

roles_path = 'v1/security/roles'


def create(name,
        description='',
        privileges=[],
        roles=[]):
    '''
    name (str):
        name of role
    
    description (str):
        description of role

    privileges (list):
        list of privileges (Default: [])

    roles (list):
        roles to inherit from (Default: [])

    CLI Example::

    .. code-block:: bash

        salt myminion nexus3_roles.create name=test_role description='test role' roles="['nx-admin']"
    '''

    ret = {
        'role': {},
    }

    path = roles_path

    payload = {
        'id': name,
        'name': name,
        'description': description,
        'privileges': privileges,
        'roles': roles
    }

    nc = nexus3.NexusClient()

    resp = nc.post(path, payload)

    if resp['status'] == 200:
        ret['role'] = json.loads(resp['body'])
    else:
        ret['comment'] = 'could not create role {}.'.format(name)
        ret['error'] = {
            'code': resp['status'],
            'msg': resp['body']
        }

    return ret


def delete(name):
    '''
    name (str):
        name of role

    CLI Example::

    .. code-block:: bash

        salt myminion nexus3_roles.delete nx-admin
    '''
    ret = {}

    path = roles_path + '/' + name
    nc = nexus3.NexusClient()

    resp = nc.delete(path)

    if resp['status'] == 204:
        ret['comment'] = 'role {} deleted'.format(name)
    else:
        ret['comment'] = 'could not delete role {}.'.format(name)
        ret['error'] = {
            'code': resp['status'],
            'msg': resp['body']
        }

    return ret


def describe(name):
    '''
    name (str):
        name of role

    CLI Example::

    .. code-block:: bash

        salt myminion nexus3_roles.describe nx-admin
    '''

    ret = {
        'role': {},
    }

    path = roles_path + '/' + name
    nc = nexus3.NexusClient()

    resp = nc.get(path)

    if resp['status'] == 200:
        ret['role'] = json.loads(resp['body'])
    else:
        ret['comment'] = 'could not retrieve role {}.'.format(name)
        ret['error'] = {
            'code': resp['status'],
            'msg': resp['body']
        }

    return ret


def list_all():
    '''
    CLI Example::

    .. code-block:: bash

        salt myminion nexus3_roles.list_all
    '''

    ret = {
        'roles': {},
    }

    path = roles_path
    nc = nexus3.NexusClient()

    resp = nc.get(path)

    if resp['status'] == 200:
        ret['roles'] = json.loads(resp['body'])
    else:
        ret['comment'] = 'could not retrieve roles.'
        ret['error'] = {
            'code': resp['status'],
            'msg': resp['body']
        }

    return ret


def update(name,
        description=None,
        privileges=None,
        roles=None):
    '''
    name (str):
        name of role
    
    description (str):
        description of role (Default: None)

    privileges (list):
        list of privileges (Default: None)

    roles (list):
        roles to inherit from (Default: None)

    CLI Example::

    .. code-block:: bash

        salt myminion nexus3_roles.update name=test_role roles="['nx-admin']"
    '''

    ret = {
        'role': {},
    }

    meta = describe(name)['role']

    path = roles_path + '/' + name

    if description is not None:
        meta['description'] = description
    
    if privileges is not None:
        meta['privileges'] = privileges
    
    if roles is not None:
        meta['roles'] = roles

    nc = nexus3.NexusClient()
    resp = nc.put(path, meta)

    if resp['status'] == 204:
        ret['role'] = describe(name)['role']
    else:
        ret['comment'] = 'could not update role {}.'.format(name)
        ret['error'] = {
            'code': resp['status'],
            'msg': resp['body'],
        }

    return ret