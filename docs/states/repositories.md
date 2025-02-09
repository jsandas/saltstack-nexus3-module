nexus3_repositories.**absent**(*name*):

    name (str):
        name (str):
            name of respository

    .. code-block:: yaml

        delete_repository:
          nexus3_repositories.absent:
            - name: test-yum


nexus3_repositories.**present**(*name,format,type,apt_dist_name='bionic',apt_flat_repo=False,apt_gpg_passphrase='',apt_gpg_priv_key='',auto_block=True,blobstore='default',blocked=False,bower_rewrite_urls=True,cleanup_policies=[],content_max_age=1440,docker_force_auth=True,docker_http_port=None,docker_https_port=None,docker_index_type='HUB',docker_index_url=None,docker_v1_enabled=False,group_members=[],http_retries=None,http_timeout=None,http_user_agent=None,maven_layout_policy='STRICT',maven_version_policy='MIXED',metadata_max_age=1440,negative_cache_enabled=True,negative_cache_max_age=1440,ntlm_domain=None,ntlm_host=None,nuget_cache_max_age=3600,remote_auth_type='username',remote_bearer_token=None,remote_password=None,remote_url='',remote_username=None,strict_content_validation=True,write_policy='ALLOW_ONCE',yum_deploy_policy='STRICT',yum_repodata_depth=0*):

    name (str):
        name (str):
            name of respository

    format (str):
        Format of repository [apt|bower|cocoapads|conan|docker|maven2|etc.]
        .. note::
            This can be any officaly supported repository format for Nexus

    type (str):
        Repository type [hosted|group|proxy]

    apt_dist_name (str):
        Apt distribution name (Default: bionic)

    apt_flat_repo (bool):
        Repo is flat ie: no folders (Default: False)

    apt_gpg_passphrase (str):
        GPG signing private key passphrase (Default: '')

    apt_gpg_priv_key (str):
        GPG signing private key (Default: '')
        .. note::
            This is require for hosted apt repositories

    auto_block (bool):
        Auto-block upstream if too many errors (Default: True)

    blobstore (str):
        Name of blobstore to use (Default: default)

    blocked (boo):
        Block repository (Default: False)

    bower_rewrite_urls (bool):
        Bower rewrite urls (Default: True)
    
    cleanup_policies (list):
        List of cleanup policies to apply to repository (Default: [])

    content_max_age (int):
        Max age of content cache in seconds (Default: 1440)

    docker_force_auth (bool):
        Force basic authentication [True|False] (Default: True)

    docker_http_port (int):
        HTTP port for docker api (Default: None)
        .. note::
            Used if the server is behind a secure proxy

    docker_https_port (int):
        HTTPS port for docker api (Default: None)
        .. note::
            Used if the server is configured for https

    docker_index_type (str):
        Type of index for docker registry [REGISTRY|HUB|CUSTOM] (Default: HUB)
        .. note::
            If using CUSTOM then docker_index_url must be specified

    docker_index_url (str):
        Url for docker index (Default: None)
        .. note::
            If using CUSTOM then docker_index_url must be specified

    http_retries: (int):
        Retries for proxy repositories to upstream (Default: None)

    http_timeout: (int):
        Timeout for proxy repositories to upstream in seconds (Default: None)

    http_user_agent (str):
        User agent suffix for proxy repositories (Default: None)

    docker_v1_enabled (bool):
        Enable v1 api support [True|False] (Default: False)

    maven_layout_policy (str):
        Validate all paths are maven artifacts or metadata paths [STRICT|PERMISSIVE] (default: STRICT)

    maven_version_policy (str):
        Type of marven artificats this repository stores [RELEASE|SNAPSHOT|MIXED] (default: MIXED)

    metadata_max_age (int):
        Max age of metadata cache in seconds (Default: 1440)

    ntlm_domain (str):
        NTLM domain (Default: None)

    ntlm_host (str):
        NTLM Host (Default: None)

    nuget_cache_max_age (int):
        Nuget cache max age in seconds (Default: 3600)

    negative_cache_enabled (bool):
        Enable negative caching (ie 404, etc.) (Default: True)

    negative_cache_max_age (int):
        Negative cache max age in seconds (Default: 1440)

    remote_auth_type (str):
        Authentication type for remote url [username|ntlm|bearerToken] (Default: username)
        .. note::
            Setting the bearerToken value currently does work with the REST API.  This will have to be set in the UI for now.
            https://github.com/sonatype/nexus-public/issues/247

    remote_bearer_token (str):
        Bearer Token for remote url (Default: None)
        .. note::
            Setting the bearerToken value currently does work with the REST API.  This will have to be set in the UI for now.
            https://github.com/sonatype/nexus-public/issues/247

    remote_password (str):
        Password for remote url (Default: None)

    remote_url (str):
        Remote url to proxy

    remote_username (str):
        Username for remote url (Default: None)

    strict_content_validation (bool):
        Enable strict content type validation [True|False] (Default: True)

    write_policy (str):
        Controls if deployments of and updates to artifacts are allowed [ALLOW|ALLOW_ONCE|DENY] (Default: ALLOW_ONCE)

    yum_deploy_policy (str):
        Validate that all paths are RPMs or yum metadata [STRICT|PERMISSIVE] (Default: STRICT)

    yum_repodata_depth (int):
        Specifies the repository depth where repodata folder(s) are created (Default: 0)

    .. code-block:: yaml

        create_repository:
          nexus3_repositories.present:
            - name: test-yum
            - type: proxy
            - blobstore: yum-blobstore
            - remote_url: https://yum.example.com
