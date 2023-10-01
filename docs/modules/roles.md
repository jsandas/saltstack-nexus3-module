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
