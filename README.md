The purpose of this project is to create a (hopefully) easy to use method for managing Nexus 3 using Salt.  This is a major refactor which leverages the REST api rather than the script api.  Sonatype has disabled execution of groovy scripts by default for security reasons (https://help.sonatype.com/repomanager3/rest-and-integration-api/script-api).

Installation:
Download desired release version from https://github.com/jsandas/saltstack-nexus3-module/releases/

Extract archive and copy the _states, _modules, and _utils folder to the files_root of the saltmaster (usually '/srv/salt').

Then run saltutil.sync_all to copy the files to the minion.

    Example:
        salt '*' saltutil.sync_all

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

**Modules:**
[anonymous_access](docs/modules/anonymous_access.md)
[blobstores](docs/modules/blobstores.md)
[email](docs/modules/email.md)
[privileges](docs/modules/privileges.md)
[readonly](docs/modules/readonly.md)
[realms](docs/modules/realms.md)
[repositories](docs/modules/repositories.md)
[roles](docs/modules/roles.md)
[status](docs/modules/status.md)
[tasks](docs/modules/tasks.md)
[users](docs/modules/users.md)

**States:**
[blobstores](docs/states/users.md)
[email](docs/states/email.md)
[privileges](docs/states/privileges.md)
[repositories](docs/states/repositories.md)
[roles](docs/states/roles.md)
[scripts](docs/states/scripts.md)
[security](docs/states/security.md)
[users](docs/states/users.md)
