

    CLI Example::

        salt myminion nexus3.repositories.create_hosted name=test-raw format=raw blobstore=raw_blobstore

        salt myminion nexus3_repositories.create_hosted name=test-yum format=yum yum_repodata_depth=3 yum_deploy_policy=permissive
    

nexus3_repositories.**list_all**():

    CLI Example::

        salt myminion nexus3_repositories.list_all


nexus3_repositories.**proxy**(*name,format,remote_url,apt_dist_name='bionic',apt_flat_repo=False,blobstore='default',bower_rewrite_urls=True,cleanup_policies=[],content_max_age=1440,docker_force_auth=True,docker_http_port=None,docker_https_port=None,docker_index_type='HUB',docker_index_url=None,docker_index_type='HUB',docker_index_url=None,docker_v1_enabled=False,maven_layout_policy='STRICT',maven_version_policy='MIXED',metadata_max_age=1440,ntlm_domain=None,ntlm_host=None,nuget_cache_max_age=3600,remote_auth_type='username',remote_bearer_token=None,remote_password=None,remote_username=None,strict_content_validation=True*):

    Nexus 3 supports many different formats.  The apt, bower, docker, maven, and nuget formats have built-in arguments.

    name (str):
        Name of repository
    
    format (str):
        Format of repository [apt|bower|cocoapads|conan|docker|maven2|etc.]
        Note:
            This can be any officaly supported repository format for Nexus

    remote_url (str):
        Remote url to proxy

    apt_dist_name (str):
        Apt distribution name (Default: bionic)

    apt_flat_repo (bool):
        Repo is flat ie: no folders (Default: False)

    blobstore (str):
        Name of blobstore to use (Default: default)

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
        Note:
            Used if the server is behind a secure proxy

    docker_https_port (int):
        HTTPS port for docker api (Default: None)
        Note:
            Used if the server is configured for https

    docker_index_type (str):
        Type of index for docker registry [REGISTRY|HUB|CUSTOM] (Default: HUB)
        Note:
            If using CUSTOM then docker_index_url must be specified

    docker_index_url (str):
        Url for docker index (Default: None)
        Note:
            If using CUSTOM then docker_index_url must be specified

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

    remote_username (str):
        Username for remote url (Default: None)

    strict_content_validation (bool):
        Enable strict content type validation [True|False] (Default: True)

    CLI Example::

        salt myminion nexus3.repositories.proxy name=test_raw format=raw blobstore=raw_blobstore

        salt myminion nexus3_repositories.proxy name=test_apt format=apt remote_url=http://test.example.com remote_username=bob remote_password=testing apt_dist_name=bionic apt_flat_repo=False
