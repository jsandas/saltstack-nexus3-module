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
