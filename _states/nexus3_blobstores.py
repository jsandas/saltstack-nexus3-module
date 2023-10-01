'''
state module for Nexus 3 blobstores

:version: v0.2.2

:configuration: In order to connect to Nexus 3, certain configuration is required
    in /etc/salt/minion on the relevant minions.

    Example:
      nexus3:
        hostname: '127.0.0.1:8081'
        username: 'admin'
        password: 'admin123'

'''

import logging

log = logging.getLogger(__name__)


def absent(name):
    '''
    name (str):
        Name of blobstore

    .. code-block:: yaml

        myblobstore:
          nexus3_blobstores.absent


        delete_myblobstore:
          nexus3_blobstores.absent:
            - name: myblobstore
    '''

    ret = {
        'name': name, 
        'changes': {}, 
        'result': True, 
        'comment': ''
    }

    # get metadata of blobstore if it exists
    meta = __salt__['nexus3_blobstores.describe'](name)
    exists = True

    if not meta['blobstore']:
        exists = False

    if not exists:       
        ret['comment'] = 'blobstore {} not found'.format(name)

    # if test is true
    if exists:
        if __opts__['test']:
            ret['result'] = None
            ret['comment'] = 'blobstore {} will be deleted'.format(name)
            return ret

        delete_results = __salt__['nexus3_blobstores.delete'](name)
        if 'error' in delete_results.keys():
            ret['result'] = False
            ret['comment'] = delete_results['error']
            return ret        

        ret['changes'] = delete_results

    return ret


def present(name,
        quota_type=None,
        quota_limit=1000000,
        store_type='file',
        s3_accessKeyId='',
        s3_bucket='nexus3',
        s3_endpoint='',
        s3_expiration=3,
        s3_forcePathStyle=False,
        s3_prefix='',
        s3_region='Default',
        s3_secretAccessKey=''):
    '''
    name (str):
        Name of blobstore

    quota_type (str):
        Quota type [None|spaceRemainingQuota|spaceUsedQuota] (Default: None)

    quota_limit (int):
        Quota size in bytes (Default: 1000000)
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

    .. code-block:: yaml

        myblobstore:
          nexus3_blobstores.present:
            - store_type: file


        myblobstore:
          nexus3_blobstores.present:
            - store_type: file
            - quota_type: spaceUsedQuota
            - quota_limit: 5000000

        mys3blobstore:
          nexus3_blobstores.present:
            - store_type: s3
            - s3_bucket: nexus3
            - s3_accessKeyId: AKIAIOSFODNN7EXAMPLE
            - s3_secretAccessKey: wJalrXUtnFEMIK7MDENGbPxRfiCYEXAMPLEKEY
    '''

    ret = {
        'name': name, 
        'changes': {}, 
        'result': True, 
        'comment': ''
    }

    # get metadata of blobstore if it exists
    meta = __salt__['nexus3_blobstores.describe'](name)
    exists = True

    if not meta['blobstore']:
        exists = False

    if not exists:

        if __opts__['test']:
            ret['result'] = None
            ret['comment'] = 'blobstore {} will be created.'.format(name)
            return ret


        create_results = __salt__['nexus3_blobstores.create'](name, quota_type, 
                                                                quota_limit, store_type,
                                                                s3_accessKeyId,s3_bucket,
                                                                s3_endpoint,s3_expiration,
                                                                s3_forcePathStyle,s3_prefix,
                                                                s3_region,s3_secretAccessKey)
        if 'error' in create_results.keys():
            ret['result'] = False
            ret['comment'] = create_results['error']
            return ret

        ret['changes'] = create_results  
  
    if exists:
        is_update = False
        updates = {}

        ret['comment'] = 'blobstore {} is in desired state'.format(name)

        if quota_type is None and meta['blobstore']['softQuota'] is not None:
            updates['quota_type'] = quota_type
            is_update = True

        if quota_type is not None and meta['blobstore']['softQuota'] is not None:
            if quota_type != meta['blobstore']['softQuota']['type']:
                updates['quota_type'] = quota_type
                is_update = True
            if quota_limit != meta['blobstore']['softQuota']['limit']:
                updates['quota_limit'] = quota_limit
                is_update = True

        if quota_type is not None and meta['blobstore']['softQuota'] is None:
            updates['quota_type'] = quota_type
            updates['quota_limit'] = quota_limit
            is_update = True

        if 'bucketConfiguration' in meta['blobstore']:
            s3_config = meta['blobstore']['bucketConfiguration']

            if s3_config['bucket']['region'] != s3_region:
                updates['s3_region'] = s3_region
                is_update = True
            
            if s3_config['bucket']['name'] != s3_bucket:
                updates['s3_bucket'] = s3_bucket
                is_update = True

            if s3_config['bucket']['prefix'] != s3_prefix:
                updates['s3_prefix'] = s3_prefix
                is_update = True

            if s3_config['bucket']['expiration'] != s3_expiration:
                updates['s3_expiration'] = s3_expiration
                is_update = True

            if s3_config['bucketSecurity']['accessKeyId'] != s3_accessKeyId:
                updates['s3_accessKeyId'] = s3_accessKeyId
                is_update = True

            if s3_config['advancedBucketConnection']['endpoint'] != s3_endpoint:
                updates['s3_endpoint'] = s3_endpoint
                is_update = True

            if s3_config['advancedBucketConnection']['forcePathStyle'] != s3_forcePathStyle:
                updates['s3_forcePathStyle'] = s3_forcePathStyle
                is_update = True

        if __opts__['test']:
            if is_update:
                ret['result'] = None
                ret['comment'] = 'blobstore {} will be updated with: {}'.format(name, updates)
            else:
                ret['comment'] = 'blobstore {} is in desired state.'.format(name)
            return ret

        if is_update:
            update_results = __salt__['nexus3_blobstores.update'](name, quota_type,quota_limit,
                                                                s3_accessKeyId,s3_bucket,
                                                                s3_endpoint,s3_expiration,
                                                                s3_forcePathStyle,s3_prefix,
                                                                s3_region,s3_secretAccessKey)
            if 'error' in update_results.keys():
                ret['result'] = False
                ret['comment'] = update_results['error']
                return ret

            ret['changes'] = updates
            ret['comment'] = ''

    return ret