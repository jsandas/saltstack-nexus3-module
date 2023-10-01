'''
execution module for the Nexus 3 repositories

:version: v0.2.2

:configuration: In order to connect to Nexus 3, certain configuration is required
    in /etc/salt/minion on the relevant minions.

    Example:
      nexus3:
        hostname: '127.0.0.1:8081'
        username: 'admin'
        password: 'admin123'

'''

import base64
import json
import logging

import nexus3

log = logging.getLogger(__name__)

__outputter__ = {
    'sls': 'highstate',
    'apply_': 'highstate',
    'highstate': 'highstate',
}

repo_base_path = 'v1/repositories'


def _format_url_string(format):
    '''
    Helper function to handle inconsistency in format name and api url paths
    '''
    ret = format
    if format == 'maven2':
        ret = 'maven'
    return ret


def group(name,
        format,
        blobstore='default',
        docker_force_auth=True,
        docker_http_port=None,
        docker_https_port=None,
        docker_v1_enabled=False,
        group_members=[],
        strict_content_validation=True):

    '''
    Nexus 3 supports many different formats.  The bower, docker, maven2, and nuget formats have built-in arguments.

    name (str):
        Name of repository
    
    format (str):
        Format of repository [bower|cocoapads|conan|docker|etc.]
        .. note::
            This can be any officaly supported repository format for Nexus

    blobstore (str):
        Name of blobstore to use (Default: default)

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

    docker_v1_enabled (bool):
        Enable v1 api support [True|False] (Default: False)

    group_members (list):
        List of repositories in group (Default: [])
        .. note::
            The list cannot be empty.  An error will be returned

    strict_content_validation (bool):
        Enable strict content type validation [True|False] (Default: True)
  }

    CLI Example::

    .. code-block:: bash

        salt myminion nexus3_repositories.group name=test-yum-group format=yum group_members=['test-yum']
    '''

    ret = {
        'repository': {},
    }

    format_url_string = _format_url_string(format)

    payload = {
        'name': name,
        'online': True,
        'storage': {
            'blobStoreName': blobstore,
            'strictContentTypeValidation': strict_content_validation,
        },
        'group': {
            'memberNames': group_members
        }
    }

    docker = {
        'docker': {
            'v1Enabled': docker_v1_enabled,
            'forceBasicAuth': docker_force_auth,
        }
    }

    if format == 'docker':
        if docker_http_port is not None:
            docker['docker']['httpPort'] = docker_http_port
        if docker_https_port is not None:
            docker['docker']['httpsPort'] = docker_https_port
        payload.update(docker)

    metadata = describe(name)

    update = False
    if metadata['repository']:
        update = True

    if not group_members:
        if update:
            ret['comment'] = 'could not update repository {}.'.format(name)
        else:
            ret['comment'] = 'could not create repository {}.'.format(name)

        ret['error'] = 'group_members cannot be empty'
        return ret

    nc = nexus3.NexusClient()

    if update:
        update_path = repo_base_path + '/' + format_url_string + '/group/' + name
        resp = nc.put(update_path, payload)
        ret['comment'] = 'updated repository {}.'.format(name)
    else:
        create_path = repo_base_path + '/' + format_url_string + '/group'
        resp = nc.post(create_path, payload)
        ret['comment'] = 'created repository {}.'.format(name)

    if resp['status'] == 201 or resp['status'] == 204:
        ret['repository'] = describe(name)['repository']
    else:
        if update:
            ret['comment'] = 'could not update repository {}.'.format(name)
        else:
            ret['comment'] = 'could not create repository {}.'.format(name)

        ret['error'] = {
            'code': resp['status'],
            'msg': resp['body']
        }

    return ret


def hosted(name,
        format,
        apt_dist_name='bionic',
        apt_gpg_passphrase='',
        apt_gpg_priv_key='',
        blobstore='default',
        cleanup_policies=[],
        docker_force_auth=True,
        docker_http_port=None,
        docker_https_port=None,
        docker_v1_enabled=False,
        maven_layout_policy='STRICT',
        maven_version_policy='MIXED',
        strict_content_validation=True,
        yum_deploy_policy='STRICT',
        yum_repodata_depth=0,
        write_policy='ALLOW_ONCE'):

    '''
    Nexus 3 supports many different formats.  The apt, bower, docker, maven2, and nuget formats have built-in arguments.

    name (str):
        Name of repository
    
    format (str):
        Format of repository [apt|bower|cocoapads|conan|docker|maven2|etc.]
        .. note::
            This can be any officaly supported repository format for Nexus

    apt_dist_name (str):
        Apt distribution name (Default: bionic)

    apt_gpg_passphrase (str):
        GPG signing private key passphrase (Default: '')

    apt_gpg_priv_key (str):
        Base64 string of GPG signing private key (Default: '')
        .. note::
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
        .. note::
            Used if the server is behind a secure proxy

    docker_https_port (int):
        HTTPS port for docker api (Default: None)
        .. note::
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

    .. code-block:: bash

        salt myminion nexus3.repositories.create_hosted name=test-raw format=raw blobstore=raw_blobstore

        salt myminion nexus3_repositories.create_hosted name=test-yum format=yum yum_repodata_depth=3 yum_deploy_policy=permissive
    '''

    ret = {
        'repository': {},
    }

    format_url_string = _format_url_string(format)

    payload = {
        'name': name,
        'online': True,
        'storage': {
            'blobStoreName': blobstore,
            'strictContentTypeValidation': strict_content_validation,
            'writePolicy': write_policy.upper()
        }
    }

    cleanup = {
        'cleanup': {
            'policyNames': cleanup_policies
        }
    }

    base64_bytes = apt_gpg_priv_key.encode('utf-8')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('utf-8')

    apt = {
        'apt': {
            'distribution': apt_dist_name,
        },
        'aptSigning': {
            'keypair': message,
            'passphrase': apt_gpg_passphrase

        }
    }

    docker = {
        'docker': {
            'v1Enabled': docker_v1_enabled,
            'forceBasicAuth': docker_force_auth,
        }
    }

    maven = {
        'maven': {
            'versionPolicy': maven_version_policy.upper(),
            'layoutPolicy': maven_layout_policy.upper()
        }
    }

    yum = {
        'yum': {
            'repodataDepth': yum_repodata_depth,
            'deployPolicy': yum_deploy_policy.upper()
        }
    }

    if cleanup_policies:
        payload.update(cleanup)
        
    if format == 'apt':
        payload.update(apt)

    if format == 'docker':
        if docker_http_port is not None:
            docker['docker']['httpPort'] = docker_http_port
        if docker_https_port is not None:
            docker['docker']['httpsPort'] = docker_https_port
        payload.update(docker)
    
    if format == 'maven2':
        payload.update(maven)

    if format == 'yum':
        payload.update(yum)

    metadata = describe(name)

    update = False
    if metadata['repository']:
        update = True

    nc = nexus3.NexusClient()

    if update:
        update_path = repo_base_path + '/' + format_url_string + '/hosted/' + name
        resp = nc.put(update_path, payload)
        ret['comment'] = 'updated repository {}.'.format(name)
    else:
        create_path = repo_base_path + '/' + format_url_string + '/hosted'
        resp = nc.post(create_path, payload)
        ret['comment'] = 'created repository {}.'.format(name)

    if resp['status'] == 201 or resp['status'] == 204:
        ret['repository'] = describe(name)['repository']
    else:
        if update:
            ret['comment'] = 'could not update repository {}.'.format(name)
        else:
            ret['comment'] = 'could not create repository {}.'.format(name)

        ret['error'] = {
            'code': resp['status'],
            'msg': resp['body']
        }

    return ret


def proxy(name,
        format,
        remote_url,
        apt_dist_name='bionic',
        apt_flat_repo=False,
        blobstore='default',
        bower_rewrite_urls=True,
        cleanup_policies=[],
        content_max_age=1440,
        docker_force_auth=True,
        docker_http_port=None,
        docker_https_port=None,
        docker_index_type='HUB',
        docker_index_url=None,
        docker_v1_enabled=False,
        maven_layout_policy='STRICT',
        maven_version_policy='MIXED',
        metadata_max_age=1440,
        ntlm_domain=None,
        ntlm_host=None,
        nuget_cache_max_age=3600,
        remote_auth_type='username',
        remote_bearer_token=None,
        remote_password=None,
        remote_username=None,
        strict_content_validation=True):

    '''
    Nexus 3 supports many different formats.  The apt, bower, docker, maven2, and nuget formats have built-in arguments.

    name (str):
        Name of repository
    
    format (str):
        Format of repository [apt|bower|cocoapads|conan|docker|maven2|etc.]
        .. note::
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
        .. note::
            If using CUSTOM then docker_index_url must be specified

    docker_index_url (str):
        Url for docker index (Default: None)
        .. note::
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

    ntlm_domain (str):
        NTLM domain (Default: None)

    ntlm_host (str):
        NTLM Host (Default: None)

    remote_auth_type (str):
        Authentication type for remote url [username|ntlm|bearerToken] (Default: username)
        .. note::
            Setting the bearerToken value currently does work with the REST API.  This will have to be set in the UI for now.
            https://github.com/sonatype/nexus-public/issues/247

    remote_bearer_token (str):
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

    .. code-block:: bash

        salt myminion nexus3.repositories.proxy name=test_raw format=raw blobstore=raw_blobstore

        salt myminion nexus3_repositories.proxy name=test_apt format=apt remote_url=http://test.example.com remote_username=bob remote_password=testing apt='{'distribution': 'bionic', 'flat':
 False}'
    '''

    ret = {
        'repository': {},
    }

    format_url_string = _format_url_string(format)

    payload = {
        'name': name,
        'online': True,
        'storage': {
            'blobStoreName': blobstore,
            'strictContentTypeValidation': strict_content_validation
        },
        'proxy': {
            'remoteUrl': remote_url,
            'contentMaxAge': content_max_age,
            'metadataMaxAge': metadata_max_age
        },
        'negativeCache': {
            'enabled': True,
            'timeToLive': 1440
        },
        'httpClient': {
            'authentication': None,
            'blocked': False,
            'autoBlock': True,
            'connection': {
                'retries': 0,
                'userAgentSuffix': 'string',
                'timeout': 60,
                'enableCircularRedirects': False,
                'enableCookies': False
            }
        },
        'routingRule': 'string'
    }

    # auth dictionary that filters on remote_auth_type
    auth =  {
        'username': {
            'authentication': {
                'type': 'username',
                'username': remote_username,
                'password': remote_password
            },
        },
        'bearerToken': {
            'authentication': {
                'type': 'bearerToken',
                'bearerToken': remote_bearer_token
            },
        },
        'ntlm': {
            'authentication': {
                'type': 'ntlm',
                'username': remote_username,
                'password': remote_password,
                'ntlmDomain': ntlm_domain,
                'ntlmHost': ntlm_host,
            },
        },
    }

    cleanup = {
        'cleanup': {
            'policyNames': cleanup_policies
        }
    }

    apt = {
        'apt': {
            'distribution': apt_dist_name,
            'flat': apt_flat_repo
        }
    }

    bower = {
        'bower': {
            'rewritePackageUrls': bower_rewrite_urls
        }
    }

    docker = {
        'docker': {
            'v1Enabled': docker_v1_enabled,
            'forceBasicAuth': docker_force_auth,
        },
        'dockerProxy': {
            'indexType': docker_index_type.upper(),
            'indexUrl': docker_index_url
        }
    }

    maven = {
        'maven': {
            'versionPolicy': maven_version_policy.upper(),
            'layoutPolicy': maven_layout_policy.upper()
        }
    }

    nuget = {
        'nugetProxy': {
            'queryCacheItemMaxAge': nuget_cache_max_age
        }
    }

    if remote_auth_type in ['username', 'bearerToken','ntlm'] and (remote_username is not None or remote_bearer_token is not None):
        payload['httpClient'].update(auth[remote_auth_type])

    if cleanup_policies:
        payload.update(cleanup)

    if format == 'apt':
        payload.update(apt)

    if format == 'bower':
        payload.update(bower)

    if format == 'docker':
        if docker_http_port is not None:
            docker['docker']['httpPort'] = docker_http_port
        if docker_https_port is not None:
            docker['docker']['httpsPort'] = docker_https_port
        payload.update(docker)
    
    if format == 'maven2':
        payload.update(maven)

    if format == 'nuget':
        payload.update(nuget)

    metadata = describe(name)

    update = False
    if metadata['repository']:
        update = True

    nc = nexus3.NexusClient()

    if update:
        update_path = repo_base_path + '/' + format_url_string + '/proxy/' + name
        resp = nc.put(update_path, payload)
        ret['comment'] = 'updated repository {}.'.format(name)
    else:
        create_path = repo_base_path + '/' + format_url_string + '/proxy'
        resp = nc.post(create_path, payload)
        ret['comment'] = 'created repository {}.'.format(name)

    if resp['status'] == 201 or resp['status'] == 204:
        ret['repository'] = describe(name)['repository']
    else:
        if update:
            ret['comment'] = 'could not update repository {}.'.format(name)
        else:
            ret['comment'] = 'could not create repository {}.'.format(name)

        ret['error'] = {
            'code': resp['status'],
            'msg': resp['body']
        }

    return ret


def delete(name):
    '''
    name (str):
        name of repository
    
    CLI Example::

    .. code-block:: bash

        salt myminion nexus3_repository.delete name=maven-central
    '''

    ret = {
        'comment': 'Repository {} deleted'.format(name)
    }

    delete_path = repo_base_path + '/' + name

    nc = nexus3.NexusClient()
    resp = nc.delete(delete_path)

    if resp['status'] == 404:
        ret['comment'] = 'Repository {} not present.'.format(name)
    elif resp['status'] != 204:
        ret['comment'] = 'Error deleting repository {}.'.format(name)
        ret['error'] = {
            'code': resp['status'],
            'msg': resp['body']
        }

    return ret


def describe(name):
    '''
    name (str):
        name of repository
    
    CLI Example::

    .. code-block:: bash

        salt myminion nexus3_repository.describe name=maven-central
    '''

    ret = {
        'repository': {}
    }

    nc = nexus3.NexusClient()
    resp = nc.get('v1/repositorySettings')

    if resp['status'] != 200:
        ret['comment'] = 'Error restrieving repository information for {}.'.format(name)
        ret['error'] = {
            'code': resp['status'],
            'msg': resp['body']
        }
        return ret

    repo_dict = json.loads(resp['body'])
    for repo in repo_dict:
        if repo['name'] == name:
            ret['repository'] = repo

    return ret


def list_all():
    '''
    CLI Example::

    .. code-block:: bash

        salt myminion nexus3_repositories.list_all

    '''

    ret = {
        'repositories': {}
    }

    nc = nexus3.NexusClient()
    resp = nc.get('v1/repositorySettings')

    if resp['status'] != 200:
        ret['comment'] = 'Error retrieving repositories.'
        ret['error'] = {
            'code': resp['status'],
            'msg': resp['body']
        }
        return ret
    
    ret['repositories'] = json.loads(resp['body'])

    return ret