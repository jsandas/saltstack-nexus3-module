The purpose of this project is to provide an easy method for managing Nexus 3 with Salt using the REST API. Sonatype has disabled execution of groovy scripts by default for security reasons (https://help.sonatype.com/repomanager3/rest-and-integration-api/script-api).

Installation:

Extension package installation (supported path):

Install from source for development:

  pip install -e .

The legacy file_root sync layout (`_modules`, `_states`, `_utils`) has been removed from this branch.

  Development commands:

    make test
    make test-integration
    make lint
    make docs-sphinx
    make changelog-draft

  Docs:

  - [Installation](docs/topics/installation.md)
  - [Migration](docs/topics/migration.md)
  - [Deprecation Policy](docs/topics/deprecation-policy.md)
  - [API Modules Reference](docs/ref/modules.rst)
  - [API States Reference](docs/ref/states.rst)

The files under the `nexus3` and `salt/pillar` folders can be used as examples for using these modules.

The nexus3 execution modules depend on the python requests library which should already be installed from the installation of the salt minion.

Configuration:
In order to connect to Nexus 3, credentials can be provided through the minion configuration in yaml format:

    Example:
      nexus3:
        hostname: '127.0.0.1:8081'
        username: 'admin'
        password: 'admin123'

If setting up Nexus for the first time, set the admin (or whichever user you choose to use) password and log then log out.

**Reference docs:**
[Modules](docs/ref/modules.rst)
[States](docs/ref/states.rst)
