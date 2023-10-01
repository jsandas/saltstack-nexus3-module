nexus3_blobstores.**absent**(*name*):

    name (str):
        Name of blobstore

    .. code-block:: yaml

        myblobstore:
          nexus3_blobstores.absent


        delete_myblobstore:
          nexus3_blobstores.absent:
            - name: myblobstore


nexus3_blobstores.**present**(*name,quota_type=None,quota_limit=1000000,store_type='file',s3_bucket='',s3_access_key_id='',s3_secret_access_key=''*):

    name (str):
        Name of blobstore

    quota_type (str):
        Quota type [None|spaceRemainingQuota|spaceUsedQuota] (Default: None)

    quota_limit (int):
        Quota size in bytes (Default: 1000000)
        Note:
            The limit should be no less than 1000000 bytes (1 MB) otherwise
            it does not display properly in the UI.

    store_type (str):
        Type of blobstore [file|s3] (Default: file)
        Note:
            S3 blobstores are currently not implemented.

    s3_bucket (str):
        Name of S3 bucket (Default: '')
        Note:
            S3 blobstores are currently not implemented.

    s3_access_key_id (str):
        AWS Access Key for S3 bucket (Default: '')
        Note:
            S3 blobstores are currently not implemented.

    s3_secret_access_key (str):
        AWS Secret Access Key for S3 bucket (Default: '')
        Note:
            S3 blobstores are currently not implemented.


    .. code-block:: yaml

        myblobstore:
          nexus3_blobstores.present:
            - store_type: file


        myblobstore:
          nexus3_blobstores.present:
            - store_type: file
            - quota_type: spaceUsedQuota
            - quota_limit: 5000000
