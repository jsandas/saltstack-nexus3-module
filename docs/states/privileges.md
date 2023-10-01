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
        Note:
            required for respository-content-selector privilege type
            content selector must exist before assigning privileges

    description (str):
        description of privilege (Default: 'New Nexus privilege')

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

    .. code-block:: yaml

        create_privilege:
          nexus3_privileges.present:
            - name: testing2
            - actions: ['ALL']
            - description: 'Test repo admin'
            - format: maven2
            - repository: '*'
            - type: repository-admin
