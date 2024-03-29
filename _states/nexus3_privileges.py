'''
state module for Nexus 3 privileges

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

log = logging.getLogger(__name__)


def absent(name):
    '''
    name (str):
        name of privilege

    .. code-block:: yaml

        testing1:
          nexus3_privileges.absent
    '''

    ret = {
        'name': name, 
        'changes': {}, 
        'result': True, 
        'comment': ''
    }

    exists = True

    meta = __salt__['nexus3_privileges.describe'](name)
    
    if not meta['privilege']:
        exists = False

    if exists:
        if __opts__['test']:
            ret['result'] = None
            ret['comment'] = 'privilege {} will be deleted.'.format(name)
            return ret

        resp = __salt__['nexus3_privileges.delete'](name)
        if 'error' in resp.keys():
            ret['result'] = False
            ret['comment'] = meta['error']
        else:
            ret['changes'] = resp
    else:
        ret['comment'] = 'privilege {} does not exist'.format(name)

    return ret


def present(name,
            type,
            actions=[],
            contentSelector=None,
            description='New Nexus privilege',
            domain=None,
            format=None,
            pattern=None,
            repository=None,
            scriptName=None):
    '''
    name (str):
        privilege name

    type (str):
        privilege type [application|repository-admin|respository-content-selector|repository-view|script|wildcard]

    actions (list):
        list of actions [ADD|ALL|CREATE|DELETE|EDIT|READ|UPDATE] (Default: [])

    contentSelector (str):
        name of content selector (Default: None)
        .. note::
            required for respository-content-selector privilege type
            content selector must exist before assigning privileges

    description (str):
        description of privilege (Default: 'New Nexus privilege')

    domain (str):
        domain of privilege [roles|scripts|search|selectors|settings|ssl-truststore|tasks|users|userschangepw] (Default: None)
        .. note::
            required for application privilege type

    format (str):
        respository format [bower|cocoapads|conan|docker|etc.] (Default: None)
        .. note::
            required for repository-admin, respository-content-selector, and repository-view privilege types

    pattern (regex):
        regex pattern to group other privileges (Default: None)
        .. note::
            required for wildcard privilege type

    repository (str):
        repository name (Default: None)
        .. note::
            required for repository-admin, respository-content-selector, and repository-view privilege types

    scriptName (str):
        script name (Default: None)

    .. code-block:: yaml

        create_privilege:
          nexus3_privileges.present:
            - name: testing2
            - actions: ['ALL']
            - description: 'Test repo admin'
            - format: maven2
            - repository: '*'
            - type: repository-admin
    '''

    ret = {
        'name': name, 
        'changes': {}, 
        'result': True, 
        'comment': ''
    }

    exists = True
    # get value of realms
    meta = __salt__['nexus3_privileges.describe'](name)

    if meta['privilege'] == {}:
        exists = False

    if not exists:

        if __opts__['test']:
            ret['result'] = None
            ret['comment'] = 'privilege {} will be created.'.format(name)
            return ret

        create_results = __salt__['nexus3_privileges.create'](name, type, actions,
                    contentSelector, description, domain, format, pattern, repository, scriptName)

        if 'error' in create_results.keys():
            ret['result'] = False
            ret['comment'] = create_results['error']
            return ret        

        ret['changes'] = create_results

    if exists:
        is_update = False
        updates = {}

        if meta['privilege']['description'] != description:
            updates['description'] = description
            is_update = True
        if meta['privilege']['actions'] != actions:
            updates['actions'] = actions
            is_update = True

        if type == 'application':
            if domain is None:
                ret['comment'] = 'domain cannot be None for type {}'.format(type)
                return ret
            if meta['privilege']['domain'] != domain:
                updates['domain'] = domain
                is_update = True

        if type in ['repository-admin','repository-view']:
            if format is None or repository is None:
                ret['comment'] = 'format and repository cannot be None for type {}'.format(type)
                return ret
            if meta['privilege']['format'] != format:
                updates['format'] = format
                is_update = True
            if meta['privilege']['repository'] != repository:
                updates['repository'] = repository
                is_update = True

        if type == 'repository-content-selector':
            if format is None or repository is None or contentSelector is None:
                ret['comment'] = 'format, contentSelector, and repository cannot be None for type {}'.format(type)
                return ret
            if meta['privilege']['format'] != format:
                updates['format'] = format
                is_update = True
            if meta['privilege']['repository'] != repository:
                updates['repository'] = repository
                is_update = True
            if meta['privilege']['contentSelector'] != contentSelector:
                updates['contentSelector'] = contentSelector
                is_update = True

        if type == 'scripts':
            if script is None:
                ret['comment'] = 'scriptName cannot be None for type {}'.format(type)
                return ret
            if meta['privilege']['scriptName'] != scriptName:
                updates['scriptName'] = scriptName
                is_update = True

        if type == 'wildcard':
            if pattern is None:
                ret['comment'] = 'pattern cannot be None for type {}'.format(type)
                return ret
            if meta['privilege']['pattern'] != pattern:
                updates['pattern'] = pattern
                is_update = True

        if __opts__['test']:
            if is_update:
                ret['result'] = None
                ret['comment'] = 'privilege {} will be updated with: {}'.format(name, updates)
            else:
                ret['comment'] = 'privilege {} is in desired state.'.format(name)
            return ret
        
        if is_update:
            update_results = __salt__['nexus3_privileges.update'](name, actions,
                        contentSelector, description, domain, format, pattern, repository, scriptName)

            if 'error' in update_results.keys():
                ret['result'] = False
                ret['comment'] = update_results['error']
                return ret        

            ret['changes'] = updates
        else:
            ret['comment'] = 'privilege {} is in desired state.'.format(name)
    return ret
