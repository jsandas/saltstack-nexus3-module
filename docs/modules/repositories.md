nexus3_repositories.**_format_url_string**(*format*):

    Helper function to handle inconsistency in format name and api url paths


nexus3_repositories.**group**(*name,format,blobstore='default',docker_force_auth=True,docker_http_port=None,docker_https_port=None,docker_v1_enabled=False,group_members=[],strict_content_validation=True*):

    Nexus 3 supports many different formats.  The bower, docker, maven2, and nuget formats have built-in arguments.

    name (str):
        Name of repository

    format (str):
        Format of repository [bower|cocoapads|conan|docker|etc.]
        Note:
            This can be any officaly supported repository format for Nexus

    blobstore (str):
        Name of blobstore to use (Default: default)

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

    docker_v1_enabled (bool):
        Enable v1 api support [True|False] (Default: False)

    group_members (list):
        List of repositories in group (Default: [])
        Note:
            The list cannot be empty.  An error will be returned

    strict_content_validation (bool):
        Enable strict content type validation [True|False] (Default: True)

    CLI Example::

    .. code-block:: bash

        salt myminion nexus3_repositories.group name=test-yum-group format=yum group_members=['test-yum']


nexus3_repositories.**hosted**(*name,format,apt_dist_name='bionic',apt_gpg_passphrase='',apt_gpg_priv_key='',blobstore='default',cleanup_policies=[],docker_force_auth=True,docker_http_port=None,docker_https_port=None,docker_v1_enabled=False,maven_layout_policy='STRICT',maven_version_policy='MIXED',strict_content_validation=True,yum_deploy_policy='STRICT',yum_repodata_depth=0,write_policy='ALLOW_ONCE'*):

    Nexus 3 supports many different formats.  The apt, bower, docker, maven2, and nuget formats have built-in arguments.

    name (str):
        Name of repository

    format (str):
        Format of repository [apt|bower|cocoapads|conan|docker|maven2|etc.]
        Note:
            This can be any officaly supported repository format for Nexus

    apt_dist_name (str):
        Apt distribution name (Default: bionic)

    apt_gpg_passphrase (str):
        GPG signing private key passphrase (Default: '')

    apt_gpg_priv_key (str):
        Base64 string of GPG signing private key (Default: '')
        Note:
            create base64 string to preserve newline characters:
              ?> base64 private-key.gpg

    blobstore (str):
        Name of blobstore to use (Default: default)

    cleanup_policies (list):
        List of cleanup policies to apply to repository (Default: [])

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

    docker_v1_enabled (bool):
        Enable v1 api support [True|False] (Default: False)

    maven_layout_policy (str):
        Validate all paths are maven artifacts or metadata paths [STRICT|PERMISSIVE] (default: STRICT)

    maven_version_policy (str):
        Type of marven artificats this repository stores [RELEASE|SNAPSHOT|MIXED] (default: MIXED)

    strict_content_validation (bool):
        Enable strict content type validation [True|False] (Default: True)

    yum_deploy_policy (str):
        Validate that all paths are RPMs or yum metadata [STRICT|PERMISSIVE] (Default: STRICT)

    yum_repodata_depth (int):
        Specifies the repository depth where repodata folder(s) are created (Default: 0)

    write_policy (str):
        Controls if deployments of and updates to artifacts are allowed [ALLOW|ALLOW_ONCE|DENY] (Default: ALLOW_ONCE)

    CLI Example::

    .. code-block:: bash

        salt myminion nexus3_repositories.hosted name=test-raw format=raw blobstore=raw_blobstore

        salt myminion nexus3_repositories.hosted name=test-yum format=yum yum_repodata_depth=3 yum_deploy_policy=permissive


nexus3_repositories.**proxy**(*name,format,remote_url,apt_dist_name='bionic',apt_flat_repo=False,auto_block=True,blobstore='default',blocked=False,bower_rewrite_urls=True,cleanup_policies=[],content_max_age=1440,docker_force_auth=True,docker_http_port=None,docker_https_port=None,docker_index_type='HUB',docker_index_url=None,docker_path_enabled=False,docker_subdomain=None,docker_v1_enabled=False,http_retries=None,http_timeout=None,http_user_agent=None,maven_layout_policy='STRICT',maven_version_policy='MIXED',metadata_max_age=1440,negative_cache_enabled=True,negative_cache_max_age=1440,ntlm_domain=None,ntlm_host=None,nuget_cache_max_age=3600,remote_auth_type='username',remote_bearer_token=None,remote_password=None,remote_username=None,strict_content_validation=True*):

    Nexus 3 supports many different formats.  The apt, bower, docker, maven2, and nuget formats have built-in arguments.

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

    docker_path_enabled (bool):
        Enable path based docker repositories [True|False] (Default: False)
        Note:
            If true then subdomain will be set to None because path and subdomain are mutually exclusive in nexus

    docker_subdomain (str):
        Enable subdomain based docker repositories (Default: None)
        Note:
            If true then path will be set to false because path and subdomain are mutually exclusive in nexus

    docker_v1_enabled (bool):
        Enable v1 api support [True|False] (Default: False)

    http_retries: (int):
        Retries for proxy repositories to upstream (Default: None)

    http_timeout: (int):
        Timeout for proxy repositories to upstream in seconds (Default: None)

    http_user_agent (str):
        User agent suffix for proxy repositories (Default: None)

    maven_layout_policy (str):
        Validate all paths are maven artifacts or metadata paths [STRICT|PERMISSIVE] (default: STRICT)

    maven_version_policy (str):
        Type of marven artificats this repository stores [RELEASE|SNAPSHOT|MIXED] (default: MIXED)

    metadata_max_age (int):
        Max age of metadata cache in seconds (Default: 1440)

    negative_cache_enabled (bool):
        Enable negative caching (ie 404, etc.) (Default: True)

    negative_cache_max_age (int):
        Negative cache max age in seconds (Default: 1440)

    nuget_cache_max_age (int):
        Nuget cache max age in seconds (Default: 3600)

    ntlm_domain (str):
        NTLM domain (Default: None)

    ntlm_host (str):
        NTLM Host (Default: None)

    remote_auth_type (str):
        Authentication type for remote url [username|ntlm|bearerToken] (Default: username)
        Note:
            Setting the bearerToken value currently does work with the REST API.  This will have to be set in the UI for now.
            https://github.com/sonatype/nexus-public/issues/247

    remote_bearer_token (str):
        Note:
            Setting the bearerToken value currently does work with the REST API.  This will have to be set in the UI for now.
            https://github.com/sonatype/nexus-public/issues/247

    remote_password (str):
        Password for remote url (Default: None)

    remote_username (str):
        Username for remote url (Default: None)

    strict_content_validation (bool):
        Enable strict content type validation [True|False] (Default: True)

    CLI Example::

    .. code-block:: bash

        salt myminion nexus3_repositories.proxy name=test_raw format=raw remote_url=http://test.example.com blobstore=raw_blobstore

        salt myminion nexus3_repositories.proxy name=test_apt format=apt remote_url=http://test.example.com remote_username=bob remote_password=testing apt_dist_name=bionic apt_flat_repo=False


nexus3_repositories.**delete**(*name*):

    name (str):
        name of repository

    CLI Example::

    .. code-block:: bash

        salt myminion nexus3_repositories.delete name=maven-central


nexus3_repositories.**describe**(*name*):

    name (str):
        name of repository

    CLI Example::

    .. code-block:: bash

        salt myminion nexus3_repositories.describe name=maven-central


nexus3_repositories.**list_all**(**):

    CLI Example::

    .. code-block:: bash

        salt myminion nexus3_repositories.list_all
