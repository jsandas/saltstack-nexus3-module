'''
Common logic used by the nexus3 state and execution module

:version: v0.2.2

This module contains logic to accommodate nexus3/salt CLI usage
'''

import json
import logging

import requests
import salt.config

__opts__ = salt.config.minion_config("/etc/salt/minion")
__salt__ = salt.loader.minion_mods(__opts__)

log = logging.getLogger(__name__)

base_api_path = 'service/rest'


# TODO: revisit the error handling
def _get_config():
    '''
    Gets configuration from minion config/pillars
    '''
    conn_info = {'hostname': 'http://127.0.0.1:8081',
                'username': '',
                'password': ''}

    _opts = __salt__['config.option']('nexus3')
    
    missing_args = []
    for attr in conn_info:
        if attr not in _opts:
            if conn_info[attr]:
                log.warning('Used default value for nexus3 {}: {}'.format(attr, conn_info[attr]))
                continue
            missing_args.append(attr)
            continue
        conn_info[attr] = _opts[attr]

    if missing_args:
        msg = 'The following connection details are missing: {}'.format(missing_args)
        log.error(msg)

    return conn_info


class NexusClient:
    '''
    Class for connecting to Nexus3 APIs
    '''

    def __init__(self):
        config = _get_config()
        self.username = config['username']
        self.password = config['password']
        self.base_url = '{}/{}'.format(config['hostname'], base_api_path)

    def delete(self, path):
        '''
        delete object from nexus server
        '''
        delete_path = '{}/{}'.format(self.base_url, path)

        ret = {
            'status': -1,
            'body': {}
        }

        try:
            resp = requests.delete(delete_path, auth=(self.username, self.password))
            log.debug('NexusClient Request: {} {}'.format(delete_path, resp.status_code))
            ret['status'] = resp.status_code
            ret['body'] = resp.content
        except Exception as e:
            log.error('NexusClient Request failed: {}'.format(e))
            ret['body'] = e

        return ret

    def get(self, path):
        '''
        get data from nexus server
        '''
        get_path = '{}/{}'.format(self.base_url, path)

        ret = {
            'status': -1,
            'body': {}
        }

        try:
            resp = requests.get(get_path, auth=(self.username, self.password))
            log.debug('NexusClient Request: {} {}'.format(get_path, resp.status_code))
            ret['status'] = resp.status_code
            ret['body'] = resp.content
        except Exception as e:
            log.error('NexusClient Request failed: {}'.format(e))
            ret['body'] = e

        return ret

    def post(self, path, data=None):
        '''
        post payload to Nexus server
        '''
        post_path = '{}/{}'.format(self.base_url, path)
        
        ret = {
            'status': -1,
            'body': {}
        }

        if isinstance(data, str):
            payload = data
            headers = {'Content-type': 'text/plain'}
        else:
            payload = json.dumps(data)
            headers = {'Content-type': 'application/json'}

        try:
            resp = requests.post(post_path, auth=(self.username, self.password), 
                headers=headers, data=payload)
            log.debug('NexusClient Request: {} {}'.format(post_path, resp.status_code))
            ret['status'] = resp.status_code
            ret['body'] = resp.content
        except Exception as e:
            log.error('NexusClient Request failed: {}'.format(e))
            ret['body'] = e

        return ret

    def put(self, path, data=None):
        '''
        put payload to Nexus server
        '''
        put_path = '{}/{}'.format(self.base_url, path)

        ret = {
            'status': -1,
            'body': {}
        }

        if isinstance(data, str):
            payload = data
            headers = {'Content-type': 'text/plain'}
        else:
            payload = json.dumps(data)
            headers = {'Content-type': 'application/json'}

        try:
            resp = requests.put(put_path, auth=(self.username, self.password), 
                headers=headers, data=payload)
            log.debug('NexusClient Request: {} {}'.format(put_path, resp.status_code))
            ret['status'] = resp.status_code
            ret['body'] = resp.content
        except Exception as e:
            log.error('NexusClient Request failed: {}'.format(e))
            ret['body'] = e

        return ret