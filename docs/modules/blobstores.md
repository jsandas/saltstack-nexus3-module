nexus3_blobstores.**create**(*name,quota_type=None,quota_limit=1000000,store_type='file',s3_accessKeyId='',s3_bucket='nexus3',s3_endpoint='',s3_expiration=3,s3_forcePathStyle=False,s3_region=Default,s3_secretAccessKey=''*):

    name (str):
        Name of blobstore
        Note:
            The blobstore name is used for blobstore path.  

    quota_type (str):
        Quota type [None|spaceRemainingQuota|spaceUsedQuota] (Default: None)

    quota_limit (int):
        Quota limit in bytes (Default: 1000000)
        Note:
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
        Note:
            only required if using a s3 compatible service

    s3_expiration (int):
        days until deleted blobs are purged from bucket (Default: 3)
        Note:
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

        salt myminion nexus3_blobstores.create name=myblobstore
        salt myminion nexus3_blobstores.create name=myblobstore quota_type=spaceRemainingQuota spaceRemainingQuota=5000000
        salt myminion nexus3_blobstores.create name=mys3blobstore store_type=s3 s3_bucket=nexus3 s3_accessKeyId=AKIAIOSFODNN7EXAMPLE s3_secretAccessKey=wJalrXUtnFEMIK7MDENGbPxRfiCYEXAMPLEKEY s3_endpoint=http://minio:9000 s3_forcePathStyle=True
    

nexus3_blobstores.**delete**(*name*):

    name (str):
        Name of blobstore

    CLI Example::

        salt myminion nexus3_blobstores.delete name=myblobstore
    

nexus3_blobstores.**describe**(*name*):

    name (str):
        Name of blobstore

    CLI Example::

        salt myminion nexus3_blobstores.describe name=myblobstore
    

nexus3_blobstores.**list_all**():

    CLI Example::

        salt myminion nexus3_blobstores.list_all
    

nexus3_blobstores.**update**(*name,quota_type=None,quota_limit=1000000,s3_accessKeyId='',s3_bucket='nexus3',s3_endpoint='',s3_expiration=3,s3_forcePathStyle=False,s3_prefix='',s3_region='Default',s3_secretAccessKey=''*):

    name (str):
        Name of blobstore
        Note:
            The blobstore name is used for blobstore path.  

    quota_type (str):
        Quota type [None|spaceRemainingQuota|spaceUsedQuota] (Default: None)

    quota_limit (int):
        Quota limit in bytes (Default: 1000000)
        Note:
            The limit should be no less than 1000000 bytes (1 MB) otherwise
            it does not display properly in the UI.

    s3_accessKeyId (str):
        AWS Access Key for S3 bucket (Default: '')

    s3_bucket (str):
        Name of S3 bucket (Default: 'nexus3')

    s3_endpoint (str):
        custom URL for s3 api [http://localhost:9000] (Default: '')
        Note:
            only required if using a s3 compatible service

    s3_expiration (int):
        days until deleted blobs are purged from bucket (Default: 3)
        Note:
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

        salt myminion nexus3_blobstores.update name=myblobstore quota_type=spaceRemainingQuota quota_limit=5000000
        salt myminion nexus3_blobstores.update name=mys3blobstore s3_bucket=nexus3 s3_accessKeyId=AKIAIOSFODNN7EXAMPLE s3_secretAccessKey=wJalrXUtnFEMIK7MDENGbPxRfiCYEXAMPLEKEY s3_endpoint=http://minio:9000 s3_forcePathStyle=True
