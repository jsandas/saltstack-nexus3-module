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

If setting up Nexus for the first time, set the admin (or whichever user you choose to use) password and log then log out.

**Modules:**
[anonymous_access]('/jsandas/saltstack-nexus3-module/docs/modules/anonymous_access.md')
[blobstores]('/jsandas/saltstack-nexus3-module/docs/modules/blobstores.md')
[email]('/jsandas/saltstack-nexus3-module/docs/modules/email.md')
[privileges]('/jsandas/saltstack-nexus3-module/docs/modules/privileges.md')
[readonly]('/jsandas/saltstack-nexus3-module/docs/modules/readonly.md')
[realms]('/jsandas/saltstack-nexus3-module/docs/modules/realms.md')
[repositories]('/jsandas/saltstack-nexus3-module/docs/modules/repositories.md')
[roles]('/jsandas/saltstack-nexus3-module/docs/modules/roles.md')
[status]('/jsandas/saltstack-nexus3-module/docs/modules/status.md')
[tasks]('/jsandas/saltstack-nexus3-module/docs/modules/tasks.md')
[users]('/jsandas/saltstack-nexus3-module/docs/modules/users.md')

**States:**
[blobstores]('/jsandas/saltstack-nexus3-module/docs/states/users.md')
[email]('/jsandas/saltstack-nexus3-module/docs/states/email.md')
[privileges]('/jsandas/saltstack-nexus3-module/docs/states/privileges.md')
[repositories]('/jsandas/saltstack-nexus3-module/docs/states/repositories.md')
[roles]('/jsandas/saltstack-nexus3-module/docs/states/roles.md')
[scripts]('/jsandas/saltstack-nexus3-module/docs/states/scripts.md')
[security]('/jsandas/saltstack-nexus3-module/docs/states/security.md')
[users]('/jsandas/saltstack-nexus3-module/docs/states/users.md')
