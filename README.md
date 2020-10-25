The purpose of this project is to create a (hopefully) easy to use method for managing Nexus 3 using Salt.  This is a major refactor which leverages the REST api rather than the script api.  Sonatype has disabled execution of groovy scripts by default for security reasons (https://help.sonatype.com/repomanager3/rest-and-integration-api/script-api).

Installation:
Download desired release version from https://github.com/jsandas/saltstack-nexus3-module/releases/

Extract archive and copy the _states, _modules, and _utils folder to the files_root of the saltmaster (usually '/srv/salt').

Then run saltutil.sync_all to copy the files to the minion.

    Example:
        salt '*' saltutil.sync_all

The files under the pillar and states folders under test-env can be used as examples for using these modules.

The nexus3 execution modules depend on the python requests library which should already be installed from the installation of the salt minion.

Configuration:
In order to connect to Nexus 3, credentials can be provided through the minion configuration in yaml format:

    Example:
      nexus3:
        hostname: '127.0.0.1:8081'
        username: 'admin'
        password: 'admin123'

If setting up Nexus for the first time, set the admin (or whichever user you choose to use) password and log that user out.

Modules
=======

nexus3_anonymous_access.**describe**():

    CLI Example::

        salt myminion nexus3_anonymous_access.describe
    

nexus3_anonymous_access.**enable**(*enabled*):

    enabled (bool):
        enable or disable anonymous access [True|False]

    CLI Example::

        salt myminion nexus3_anonymous_access.enable True

---
nexus3_blobstores.**create**(*name,quota_type=None,quota_limit=1000000,store_type='file',s3_bucket='',s3_access_key_id='',s3_secret_access_key=''*):

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
        Type of blobstore file|s3] (Default: file)
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
            The blobstore name is used for blobstore path.

    CLI Example::

        salt myminion nexus3_blobstores.create name=myblobstore
        salt myminion nexus3_blobstores.create name=myblobstore quota_type=spaceRemainingQuota spaceRemainingQuota=5000000
    

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
    

nexus3_blobstores.list_all():

    CLI Example::

        salt myminion nexus3_blobstores.list_all
    

nexus3_blobstores.**update**(*name,quota_type=None,quota_limit=1000000*):

    Note:
        Only blobstore quotas can be updated

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

    CLI Example::

        salt myminion nexus3_blobstores.create name=myblobstore quota_type=spaceRemainingQuota quota_limit=5000000

---
nexus3_email.**configure**(*enabled,fromAddress='nexus@example.org',host='localhost',nexusTrustStoreEnabled=False,password=None,port=0,sslOnConnectEnabled=False,sslServerIdentityCheckEnabled=False,startTlsEnabled=False,startTlsRequired=False,subjectPrefix=None,username=''*):

    enabled (bool):
        enable email support [True|False]

    fromAddress (str):
        mail from address (Default: nexus@example.org)

    host (string):
        smtp hostname (Default: localhost)

    nexusTrustStoreEnabled (bool):
        use nexus truststore [True|False] (Default: False)
        Note:
            Ensure CA certificate is add to the Nexus trustore

    password (str):
        smtp password (Default: None)
       
    port (int):
        smtp port (Default: 0)

    sslOnConnectEnabled (bool):
        connect using tls (SMTPS) (Default: False)
        Note:
            tls_connect and starttls should be mutually exclusive

    sslServerIdentityCheckEnabled (bool):
        verify server certificate (Default: False)

    startTlsEnabled (bool):
        enable starttls (Default: False)
        Note:
            tls_connect and starttls should be mutually exclusive

    startTlsRequired (bool):
        require starttls (Default: False)
        Note:
            tls_connect and starttls should be mutually exclusive

    subjectPrefix (str):
        prefix for subject in emails (Default: None)

    username (str):
        smtp username (Default: '')

    CLI Example::

        salt myminion nexus3_email.configure enabled=True host=smtp.example.com

        salt myminion nexus3_email.configure enabled=False
    

nexus3_email.**describe**():

    CLI Example::

        salt myminion nexus3_email.describe
    

nexus3_email.**reset**():

    CLI Example::

        salt myminion nexus3_email.reset
    

nexus3_email.**verify**():

    CLI Example::
    
    to (str):
        address to send test email to
    
        salt myminion nexus3_email.verify


---
nexus3_privileges.**create**(*name,type,actions=[],contentSelector=None,description='New Nexus privilege',domain=None,format=None,pattern=None,repository=None,scriptName=None*):

    name (str):
        privilege name

    type (str):
        privilege type [application|repository-admin|respository-content-selector|repository-view|script|wildcard]

    actions (list):
        list of actions [ADD|ALL|BROWSE|CREATE|DELETE|EDIT|READ|UPDATE] (Default: [])

    contentSelector (str):
        name of content selector (Default: None
        Note:
            required for respository-content-selector privilege type
            content selector must exist before assigning privileges

    description (str):
        description of privilge (Default: 'New Nexus privilege')

    domain (str):
        domain of privilege [roles|scripts|search|selectors|settings|ssl-truststore|tasks|users|userschangepw] (Default: None)
        Note:
            required for application privilege type

    format (str):
        respository format [bower|cocoapads|conan|docker|etc.] (Default: None)
        Note:
            required for repository-admin, respository-content-selector, and repository-view privilege types

    pattern (regex):
        regex pattern to group other privileges (Default: None)
        Note:
            required for wildcard privilege type

    repository (str):
        repository name (Default: None)
        Note:
            required for repository-admin, respository-content-selector, and repository-view privilege types

    scriptName (str):
        script name (Default: None)

    CLI Example::

        salt myminion nexus3_privileges.create name=nx-userschangepw actions="['ADD','READ']" description='Change password permission' domain=userschangepw type=application

        salt myminion nexus3_privileges.create name=nx-repository-view-nuget-nuget-hosted-browse actions=['BROWSE'] description='Browse privilege for nuget-hosted repository views' format=nuget repository=nuget-hosted type=repository-view
    

nexus3_privileges.**delete**(*name*):

    name (str):
        privilege name

    CLI Example::

        salt myminion nexus3_privileges.delete nx-analytics-all
    

nexus3_privileges.**describe**(*name*):

    name (str):
        privilege name

    CLI Example::

        salt myminion nexus3_privileges.describe nx-analytics-all
    

nexus3_privileges.**list_all**():

    CLI Example::

        salt myminion nexus3_privileges.list_all
    

nexus3_privileges.**update**(*name,actions=None,contentSelector=None,description=None,domain=None,format=None,pattern=None,repository=None,scriptName=None*):

    name (str):
        privilege name

    actions (list):
        list of actions [ADD|ALL|CREATE|DELETE|EDIT|READ|UPDATE] (Default: None)

    contentSelector (str):
        name of content selector (Default: None)
        Note:
            content selector must exist before assigning privileges

    description (str):
        description of privilege (Default: None)

    domain (str):
        domain of privilege [roles|scripts|search|selectors|settings|ssl-truststore|tasks|users|userschangepw] (Default: None)
        Note:
            required for application privilege type

    format (str):
        respository format [bower|cocoapads|conan|docker|etc.] (Default: None)
        Note:
            required for repository-admin, respository-content-selector, and repository-view privilege types

    pattern (regex):
        regex pattern to group other privileges (Default: None)
        Note:
            required for wildcard privilege type

    repository (str):
        repository name (Default: None)
        Note:
            required for repository-admin, respository-content-selector, and repository-view privilege types

    scriptName (str):
        script name (Default: None)

    CLI Example::

        salt myminion nexus3_privileges.update name=testing actions="['ADD','READ']" description='Change password permission' domain=userschangepw type=application


---
nexus3_realms.**list_active**():

    CLI Example::

        salt myminion nexus3_realms.list_active
    

nexus3_realms.**list_all**():

    CLI Example::

        salt myminion nexus3_realms.list_all
    

nexus3_realms.**reset**():

    Resets realms to default

    CLI Example::

        salt myminion nexus3_realms.reset
    

nexus3_realms.**update**(*realms*):

    realms (list):
        list of realms in order they should be used 
        Note:
            Include all desired realms in list as this will override
            the current list

    CLI Example::

        salt myminion nexus3_realms.update realms="['NexusAuthenticatingRealm','NexusAuthorizingRealm','NpmToken','DockerToken']"


---
nexus3_repositories.**delete**(*name*):

    name (str):
        name of repository
    
    CLI Example::

        salt myminion nexus3_repository.delete name=maven-central
    

nexus3_repositories.**describe**(*name*):

    name (str):
        name of repository
    
    CLI Example::

        salt myminion nexus3_repository.describe name=maven-central
    

nexus3_repositories.**group**(*name,format,blobstore='default',docker_force_auth=True,docker_http_port=None,docker_https_port=None,docker_v1_enabled=False,group_members=[],strict_content_validation=True*):

    Nexus 3 supports many different formats.  The bower, docker, maven, and nuget formats have built-in arguments.

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
  }

    CLI Example::

        salt myminion nexus3_repositories.group name=test-yum-group format=yum group_members=['test-yum']
    

nexus3_repositories.**hosted**(*name,format,apt_dist_name='bionic',apt_gpg_passphrase='',apt_gpg_priv_key='',blobstore='default',cleanup_policies=[],docker_force_auth=True,docker_http_port=None,docker_https_port=None,docker_v1_enabled=False,maven_layout_policy='STRICT',maven_version_policy='MIXED',strict_content_validation=True,yum_deploy_policy='STRICT',yum_repodata_depth=0,write_policy='ALLOW_ONCE'*):

    Nexus 3 supports many different formats.  The apt, bower, docker, maven, and nuget formats have built-in arguments.

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
        GPG signing private key (Default: '')
        Note:
            This is require for hosted apt repositories

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
  }

    CLI Example::

        salt myminion nexus3.repositories.create_hosted name=test-raw format=raw blobstore=raw_blobstore

        salt myminion nexus3_repositories.create_hosted name=test-yum format=yum yum_repodata_depth=3 yum_deploy_policy=permissive
    

nexus3_repositories.**list_all**():

    CLI Example::

        salt myminion nexus3_repositories.list_all


nexus3_repositories.**proxy**(*name,format,remote_url,apt_dist_name='bionic',apt_flat_repo=False,blobstore='default',bower_rewrite_urls=True,cleanup_policies=[],content_max_age=1440,docker_force_auth=True,docker_http_port=None,docker_https_port=None,docker_index_type='HUB',docker_index_url=None,docker_index_type='HUB',docker_index_url=None,docker_v1_enabled=False,maven_layout_policy='STRICT',maven_version_policy='MIXED',metadata_max_age=1440,nuget_cache_max_age=3600,remote_password=None,remote_username=None,strict_content_validation=True*):

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
        .. note::
            Used if the server is behind a secure proxy

    docker_https_port (int):
        HTTPS port for docker api (Default: None)
        .. note::
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

    nuget_cache_max_age (int):
        Nuget cache max age in seconds (Default: 3600)

    remote_password (str):
        Password for remote url (Default: None)

    remote_username (str):
        Username for remote url (Default: None)

    strict_content_validation (bool):
        Enable strict content type validation [True|False] (Default: True)

    CLI Example::

        salt myminion nexus3.repositories.proxy name=test_raw format=raw blobstore=raw_blobstore

        salt myminion nexus3_repositories.proxy name=test_apt format=apt remote_url=http://test.example.com remote_username=bob remote_password=testing apt_dist_name=bionic apt_flat_repo=False


---
nexus3_roles.**create**(*name,description='',privileges=[],roles=[]*):

    name (str):
        name of role
    
    description (str):
        description of role

    privileges (list):
        list of privileges (Default: [])

    roles (list):
        roles to inherit from (Default: [])

    CLI Example::

        salt myminion nexus3_roles.create name=test_role description='test role' roles="['nx-admin']"
    

nexus3_roles.**delete**(*name*):

    name (str):
        name of role

    CLI Example::

        salt myminion nexus3_roles.delete nx-admin
    

nexus3_roles.**describe**(*name*):

    name (str):
        name of role

    CLI Example::

        salt myminion nexus3_roles.describe nx-admin
    

nexus3_roles.**list_all**():

    CLI Example::

        salt myminion nexus3_roles.list_all
    

nexus3_roles.**update**(*name,description=None,privileges=None,roles=None*):

    name (str):
        name of role
    
    description (str):
        description of role (Default: None)

    privileges (list):
        list of privileges (Default: None)

    roles (list):
        roles to inherit from (Default: None)

    CLI Example::

        salt myminion nexus3_roles.update name=test_role roles="['nx-admin']"


---
nexus3_users.**create**(*name,password,emailAddress,firstName,lastName,roles=['nx-anonymous'],status='active'*):

    name (str):
        name of user
    
    password (str):
        password of user

    emailAddress (str):
        email address

    firstName (str):
        first name

    lastName (str):
        last name
    
    roles (list):
        list of roles (Default: ['nx-anonymous'])

    status (str):
        user status [active|disabled] (Default: active)

    CLI Example::

        salt myminion nexus3_users.create name=test_user emailAddress="fake@email.com" password=testpassword firstName=Test lastName=User roles="['nx-admin']"
        
        Note:
            running this command via the command-line could result in the password being saved
            is the user shell history
    

nexus3_users.**delete**(*name*):

    name (str):
        name of user

    CLI Example::

        salt myminion nexus3_users.delete test_user
    

nexus3_users.**describe**(*name*):

    name (str):
        name of user

    CLI Example::

        salt myminion nexus3_users.describe test_user
    

nexus3_users.**list_all**():

    CLI Example::

        salt myminion nexus3_users.list_all
    

nexus3_users.**update**(*name,emailAddress=None,firstName=None,lastName=None,roles=None,status=None*):

    name (str):
        name of user

    emailAddress (str):
        email address (Default: None)

    firstName (str):
        first name (Default: None)

    lastName (str):
        last name (Default: None)
    
    roles (list):
        list of roles (Default: None)

    status (str):
        user status [active|disabled] (Default: None)

    CLI Example::

        salt myminion nexus3_users.update name=test_user firstName=Testing roles="['nx-anonymous']"
    

nexus3_users.**update_password**(*name,password*):

    name (str):
        name of user

    password (str):
        password

    CLI Example::

        salt myminion nexus3_users.update_password name=test_user password=testing123

        Note:
            running this command via the command-line could result in the password being saved
            is the user shell history


States
======

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
        .. note::
            The limit should be no less than 1000000 bytes (1 MB) otherwise
            it does not display properly in the UI.

    store_type (str):
        Type of blobstore [file|s3] (Default: file)
        .. note::
            S3 blobstores are currently not implemented.

    s3_bucket (str):
        Name of S3 bucket (Default: '')
        .. note::
            S3 blobstores are currently not implemented.

    s3_access_key_id (str):
        AWS Access Key for S3 bucket (Default: '')
        .. note::
            S3 blobstores are currently not implemented.

    s3_secret_access_key (str):
        AWS Secret Access Key for S3 bucket (Default: '')
        .. note::
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


---
nexus3_email.clear(*name*):

    name (str):
        state id name
        .. note::
            do not provide this argument, this is only here
            because salt passes this arg always

    .. code-block:: yaml

        clear_email:
          nexus3_email.clear


nexus3_email.configure(*name,enabled,fromAddress='nexus@example.org',host='localhost',nexusTrustStoreEnabled=False,password=None,port=0,sslOnConnectEnabled=False,sslServerIdentityCheckEnabled=False,startTlsEnabled=False,startTlsRequired=False,subjectPrefix=None,username=''*):

    name (str):
        state id name
        .. note::
            do not provide this argument, this is only here
            because salt passes this arg always

    enabled (bool):
        enable email support [True|False]

    fromAddress (str):
        mail from address (Default: nexus@example.org)

    host (string):
        smtp hostname (Default: localhost)

    nexusTrustStoreEnabled (bool):
        use nexus truststore [True|False] (Default: False)
        .. note::
            Ensure CA certificate is add to the Nexus trustore

    password (str):
        smtp password (Default: None)
       
    port (int):
        smtp port (Default: 0)

    sslOnConnectEnabled (bool):
        connect using tls (SMTPS) (Default: False)
        .. note::
            sslOnConnectEnabled and startTlsEnabled/startTlsRequired should be mutually exclusive

    sslServerIdentityCheckEnabled (bool):
        verify server certificate (Default: False)

    startTlsEnabled (bool):
        enable starttls (Default: False)
        .. note::
            sslOnConnectEnabled and startTlsEnabled/startTlsRequired should be mutually exclusive

    startTlsRequired (bool):
        require starttls (Default: False)
        .. note::
            sslOnConnectEnabled and startTlsEnabled/startTlsRequired should be mutually exclusive


    subjectPrefix (str):
        prefix for subject in emails (Default: None)

    username (str):
        smtp username (Default: '')

    .. code-block:: yaml

        setup_email:
          nexus3_email.configure:
            - enabled: True
            - host: smtp@example.com
            - port: 587
            - fromAddress: test@example.com
            - startTlsEnabled: True


---
nexus3_privileges.**absent**(*name*):

    name (str):
        name of privilege

    .. code-block:: yaml

        testing1:
          nexus3_privileges.absent


nexus3_privileges.**present**(*name,type,actions=[],contentSelector=None,description='New Nexus privilege',domain=None,format=None,pattern=None,repository=None,scriptName=None*):

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


---
nexus3_repositories.**absent**(*name*):

    name (str):
        name (str):
            name of respository

    .. code-block:: yaml

        delete_repository:
          nexus3_repositories.absent:
            - name: test-yum


nexus3_repositories.**present**(*name,format,type,apt_dist_name='bionic',apt_flat_repo=False,apt_gpg_passphrase='',apt_gpg_priv_key='',blobstore='default',bower_rewrite_urls=True,cleanup_policies=[],content_max_age=1440,docker_force_auth=True,docker_http_port=None,docker_https_port=None,docker_index_type='HUB',docker_index_url=None,docker_v1_enabled=False,group_members=[],maven_layout_policy='STRICT',maven_version_policy='MIXED',metadata_max_age=1440,nuget_cache_max_age=3600,remote_password=None,remote_url='',remote_username=None,strict_content_validation=True,write_policy='ALLOW_ONCE',yum_deploy_policy='STRICT',yum_repodata_depth=0*):

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
        .. note::
            Used if the server is behind a secure proxy

    docker_https_port (int):
        HTTPS port for docker api (Default: None)
        .. note::
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

    nuget_cache_max_age (int):
        Nuget cache max age in seconds (Default: 3600)

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


---
nexus3_roles.**absent**(*name*):

    name (str):
        name of role

    .. code-block:: yaml

        testing1:
          nexus3_roles.absent


nexus3_roles.**present**(*name,description,privileges,roles*):

    name (str):
        name of role
    
    description (str):
        description of role

    privileges (list):
        list of privileges
        .. note::
            requires at least an empty list

    roles (list):
        roles to inherit from
        .. note::
            requires at least an empty list

    .. code-block:: yaml

        create_role:
          nexus3_roles.present:
            - name: test_role 
            - description: 'test role'
            - roles: ['nx-admin']


---
nexus3_scripts.base_url(*name*):

    Set base url for Nexus

    name (str):
      URL to set base_url to for Nexus 3

      .. note::
        This would usually be the FQDN used
        to access Nexus

    .. code-block:: yaml

      http://localhost:8081:
      nexus3_scripts.base_url


nexus3_scripts.task(*name,typeId,taskProperties,cron,setAlertEmail=None*):

    name (str):
        Name of task

    typeId (str):
        Nexus taskId [db.backup|repository.docker.gc|repository.docker.upload-purge|blobstore.compact|repository.purge-unused]

    taskProperties (dict):
        Dictionary of the task properties
        .. note::
            The key/values under task_properties is indented 4 spaces instead
            of two.  This is how salt creates a dictionary from the yaml

    setAlertEmail (str):
        Email to send alerts to

    cron (str):
        Cron-like string to schedule task runs

        .. example::
            '0 0 11 * 5 ?'

        .. note::
            Cron schedule notes:
            Field Name	Allowed Values
            Seconds	    0-59
            Minutes	    0-59
            Hours	    0-23
            Dayofmonth	1-31
            Month	    1-12 or JAN-DEC
            Dayofweek	1-7 or SUN-SAT
            Year(optional)	empty, 1970-2099

    .. code-block:: yaml

      database_backup:
        nexus3_scripts.tasks:
          - task_type_id: 'db.backup'
          - task_properties:
              location:'/nexus-data/backup'
          - task_cron: '0 0 21 * * ?'


---
nexus3_security.anonymous_access(*name,enabled*):

    name (str):
        state id name
        .. note::
            do not provide this argument, this is only here
            because salt passes this arg always
    
    enabled (bool):
        enable or disable anonymous access [True|False]

    .. code-block:: yaml

        set_anonymous_access:
          nexus3_security.anonymous_access:
            - enabled: True


nexus3_security.realms(*name,realms*):

    name (str):
        state id name
        .. note::
            do not provide this argument, this is only here
            because salt passes this arg always
    
    realms (list):
        list of realms in order they should be used 
        .. note::
            Include all desired realms in list as this will override
            the current list

    .. code-block:: yaml

        update_realms:
          nexus3_security.realms:
            - realms: ['NexusAuthenticatingRealm','NexusAuthorizingRealm','NpmToken','DockerToken']

        update_realms:
          nexus3_security.realms:
            - realms: 
              - NexusAuthenticatingRealm
              - NexusAuthorizingRealm
              - NpmToken
              - DockerToken


---
nexus3_status.**check**():

    Health check endpoint that returns the results of the system status checks

    CLI Example::

    .. code-block:: bash

        salt myminion nexus3_status.check


---
nexus3_tasks.**describe**(*id*):

    id (str):
        task id

    CLI Example::

    .. code-block:: bash

        salt myminion nexus3_tasks.describe id=512be2c3-aa04-448f-b0ce-2047eee34903

nexus3_tasks.**list_all**():

    CLI Example::

    .. code-block:: bash

        salt myminion nexus3_tasks.list_all

nexus3_tasks.**run**(*id*):

    id (str):
        task id

    CLI Example::

    .. code-block:: bash

        salt myminion nexus3_tasks.run id=512be2c3-aa04-448f-b0ce-2047eee34903

nexus3_tasks.**stop**(*id*):
    id (str):
        task id

    CLI Example::

    .. code-block:: bash

        salt myminion nexus3_tasks.stop id=512be2c3-aa04-448f-b0ce-2047eee34903


---
nexus3_users.**absent**(*name*):

    name (str):
        name of role

    .. code-block:: yaml

        testing1:
          nexus3_users.absent


nexus3_users.**present**(*name,password,emailAddress,firstName,lastName,roles=['nx-anonymous'],status='active'*):

    name (str):
        name of user
    
    password (str):
        password of user

    emailAddress (str):
        email address
        .. note::
            password will always be updated as there is not
            a way to determine it's current value

    firstName (str):
        first name

    lastName (str):
        last name
    
    roles (list):
        list of roles (Default: ['nx-anonymous'])

    status (str):
        user status [active|disabled] (Default: active)

    .. code-block:: yaml

        create_user:
          nexus3_users.present:
            - name: test_role 
            - password: abc123
            - emailAddress: test@email.com
            - firstName: Test
            - lastName: User
            - roles: ['nx-admin']

        create_user:
          nexus3_users.present:
            - name: test_role 
            - password: abc123
            - emailAddress: test@email.com
            - firstName: Test
            - lastName: User
            - roles: ['nx-admin']
            - status: disabled