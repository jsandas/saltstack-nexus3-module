''''
execution module for Nexus 3 blobstores

:version: v0.2

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
    "sls": "highstate",
    "apply_": "highstate",
    "highstate": "highstate",
}

blobstore_path = 'v1/blobstores'


def create(name,
        quota_type=None,
        quota_limit=1000000,
        store_type='file',
        s3_accessKeyId='',
        s3_bucket='nexus3',
        s3_endpoint='',
        s3_expiration='3',
        s3_forcePathStyle=False,
        s3_prefix='',
        s3_region='Default',
        s3_secretAccessKey=''):
    '''
    name (str):
        Name of blobstore
        .. note::
            The blobstore name is used for blobstore path.  

    quota_type (str):
        Quota type [None|spaceRemainingQuota|spaceUsedQuota] (Default: None)

    quota_limit (int):
        Quota limit in bytes (Default: 1000000)
        .. note::
            The limit should be no less than 1000000 bytes (1 MB) otherwise
            it does not display properly in the UI.

    store_type (str):
        Type of blobstore [file|s3] (Default: file)

    s3_accessKeyId (str):
        AWS Access Key for S3 bucket (Default: '')

    s3_bucket (str):
        Name of S3 bucket (Default: 'nexus3')

    s3_endpoint (str):
        custom URL for s3 api [http://localhost:9000] (Default: '')
        .. note::
            only required if using a s3 compatible service

    s3_expiration (int):
        days until deleted blobs are purged from bucket (Default: 3)
        .. note::
            set to -1 to disable

    s3_forcePathStyle (bool):
        force path style url format (Default: False)
        .. note:
            if using s3 compatible service like min.io, set this to True

    s3_region (str):
        Region of S3 bucket [us-east-1,us-east-2,us-west-1,us-west-2,etc] (Default: 'Default')

    s3_secretAccessKey (str):
        AWS Secret Access Key for S3 bucket (Default: '')

    CLI Example::

    .. code-block:: bash

        salt myminion nexus3_blobstores.create name=myblobstore
        salt myminion nexus3_blobstores.create name=myblobstore quota_type=spaceRemainingQuota spaceRemainingQuota=5000000
        salt myminion nexus3_blobstores.create name=mys3blobstore store_type=s3 s3_bucket=nexus3 s3_accessKeyId=AKIAIOSFODNN7EXAMPLE s3_secretAccessKey=wJalrXUtnFEMIK7MDENGbPxRfiCYEXAMPLEKEY s3_endpoint=http://minio:9000 s3_forcePathStyle=True
    '''

    ret = {
        'blobstore': {},
    }

    path = '{}/{}'.format(blobstore_path, store_type)

    payload = {
        'name': name,
    }

    if store_type == 'file':
        payload['path'] = '/nexus-data/blobs/' + name
    
    if store_type == 's3':

        s3_config = {}

        s3_config['bucket'] = {
            'region': s3_region,
            'name': s3_bucket,
            'prefix': s3_prefix,
            'expiration': s3_expiration
        }   

        if s3_accessKeyId != '' or s3_secretAccessKey != '':
            s3_config['bucketSecurity'] ={
                'accessKeyId': s3_accessKeyId,
                'secretAccessKey': s3_secretAccessKey,
                # 'role': 'string',
                # 'sessionToken': 'string'
            }

        # "encryption": {
        #     'encryptionType': 's3ManagedEncryption',
        #     'encryptionKey': 'string'
        # }

        if s3_endpoint != '':
            s3_config['advancedBucketConnection'] = {
                'endpoint': s3_endpoint,
                'signerType': 'DEFAULT',
                'forcePathStyle': s3_forcePathStyle
            }

        payload['bucketConfiguration'] = s3_config

    if quota_type is not None:
        payload['softQuota'] = {
            'type': quota_type,
            'limit': quota_limit
        }

    nc = nexus3.NexusClient()

    resp = nc.get(path + '/' + name)

    if resp['status'] == 200:
        ret['comment'] = 'blobstore {} already exists.'.format(name)
        return ret

    resp = nc.post(path, payload)

    if resp['status'] in [201, 204]:
        ret['blobstore'] = describe(name)['blobstore']
    else:
        ret['comment'] = 'could not create blobstore {}.'.format(name)
        ret['error'] = {
            'code': resp['status'],
            'msg': resp['body']
        }


    return ret


def delete(name):
    '''
    name (str):
        Name of blobstore

    CLI Example::

    .. code-block:: bash

        salt myminion nexus3_blobstores.delete name=myblobstore
    '''

    ret = {
        'comment': 'Deleted blobstore "{}"'.format(name)
    }

    path = '{}/{}'.format(blobstore_path, name)

    nc = nexus3.NexusClient()
    resp = nc.delete(path)

    if resp['status'] == 404:
        ret['comment'] = 'blobstore {} does not exist.'.format(name)
    elif resp['status'] != 204:
        ret['comment'] = 'could not delete blobstore {}.'.format(name)
        ret['error'] = {
            'code': resp['status'],
            'msg': resp['body']
        }

    return ret


def describe(name):
    '''
    name (str):
        Name of blobstore

    CLI Example::

    .. code-block:: bash

        salt myminion nexus3_blobstores.describe name=myblobstore
    '''

    ret = {
        'blobstore': {},
    }

    resp = list_all()

    if 'error' in resp.keys():
        ret['result'] = False
        ret['comment'] = 'could not retrieve blobstore {}.'.format(name)
        ret['error'] = resp['error']
        return ret        

    for bstore in resp['blobstores']:
        if bstore['name'] == name:
            ret['blobstore'] = bstore
            break

    if ret['blobstore']:
        path = '{}/{}/{}'.format(blobstore_path, ret['blobstore']['type'].lower(), name)

        nc = nexus3.NexusClient()
        resp = nc.get(path)

        if resp['status'] == 200:
            ret['blobstore'].update(json.loads(resp['body']))
        else:
            ret['comment'] = 'could not retrieve blobstore {}'.format(name)
            ret['error'] = {
                'code': resp['status'],
                'msg': resp['body']
            }

    return ret


def list_all():
    '''
    CLI Example::

    .. code-block:: bash

        salt myminion nexus3_blobstores.list_all
    '''

    ret = {
        'blobstores': {}
    }

    nc = nexus3.NexusClient()
    resp = nc.get(blobstore_path)

    if resp['status'] == 200:
        ret['blobstores'] = json.loads(resp['body'])
    else:
        ret['comment'] = 'could not retrieve blobstores.'
        ret['error'] = {
            'code': resp['status'],
            'msg': resp['body']
        }

    return ret


def update(name,
        quota_type=None,
        quota_limit=1000000,
        s3_accessKeyId='',
        s3_bucket='nexus3',
        s3_endpoint='',
        s3_expiration='3',
        s3_forcePathStyle=False,
        s3_prefix='',
        s3_region='Default',
        s3_secretAccessKey=''):
    '''
    name (str):
        Name of blobstore
        .. note::
            The blobstore name is used for blobstore path.  

    quota_type (str):
        Quota type [None|spaceRemainingQuota|spaceUsedQuota] (Default: None)

    quota_limit (int):
        Quota limit in bytes (Default: 1000000)
        .. note::
            The limit should be no less than 1000000 bytes (1 MB) otherwise
            it does not display properly in the UI.

    s3_accessKeyId (str):
        AWS Access Key for S3 bucket (Default: '')

    s3_bucket (str):
        Name of S3 bucket (Default: 'nexus3')

    s3_endpoint (str):
        custom URL for s3 api [http://localhost:9000] (Default: '')
        .. note::
            only required if using a s3 compatible service

    s3_expiration (int):
        days until deleted blobs are purged from bucket (Default: 3)
        .. note::
            set to -1 to disable

    s3_forcePathStyle (bool):
        force path style url format (Default: False)
        .. note:
            if using s3 compatible service like min.io, set this to True

    s3_region (str):
        Region of S3 bucket [us-east-1,us-east-2,us-west-1,us-west-2,etc] (Default: 'Default')

    s3_secretAccessKey (str):
        AWS Secret Access Key for S3 bucket (Default: '')

    CLI Example::

    .. code-block:: bash

        salt myminion nexus3_blobstores.create name=myblobstore quota_type=spaceRemainingQuota quota_limit=5000000
        salt myminion nexus3_blobstores.update name=mys3blobstore s3_bucket=nexus3 s3_accessKeyId=AKIAIOSFODNN7EXAMPLE s3_secretAccessKey=wJalrXUtnFEMIK7MDENGbPxRfiCYEXAMPLEKEY s3_endpoint=http://minio:9000 s3_forcePathStyle=True
    '''

    ret = {
        'blobstore': {}
    }

    metadata = describe(name)

    if not metadata['blobstore']:
        return metadata

    payload = {
        'name': name,
    }

    if metadata['blobstore']['type'].lower() == 'file':
        payload['path'] = '/nexus-data/blobs/' + name
        
    if metadata['blobstore']['type'].lower() == 's3':

        s3_config = {}

        s3_config['bucket'] = {
            'region': s3_region,
            'name': s3_bucket,
            'prefix': s3_prefix,
            'expiration': s3_expiration
        }   

        if s3_accessKeyId != '' or s3_secretAccessKey != '':
            s3_config['bucketSecurity'] ={
                'accessKeyId': s3_accessKeyId,
                'secretAccessKey': s3_secretAccessKey,
                # 'role': 'string',
                # 'sessionToken': 'string'
            }

        # "encryption": {
        #     'encryptionType': 's3ManagedEncryption',
        #     'encryptionKey': 'string'
        # }

        if s3_endpoint != '':
            s3_config['advancedBucketConnection'] = {
                'endpoint': s3_endpoint,
                'signerType': 'DEFAULT',
                'forcePathStyle': s3_forcePathStyle
            }

        payload['bucketConfiguration'] = s3_config

    if quota_type is not None:
        payload['softQuota'] = {
            'type': quota_type,
            'limit': quota_limit
        }

    path = '{}/{}/{}'.format(blobstore_path, metadata['blobstore']['type'].lower(), name)

    nc = nexus3.NexusClient()

    resp = nc.put(path, payload)

    if resp['status'] == 204:
        ret['blobstore'] = describe(name)['blobstore']
    else:
        ret['comment'] = 'could not update blobstore {}.'.format(name)
        ret['error'] = {
            'code': resp['status'],
            'msg': resp['body']
        }

    return ret
