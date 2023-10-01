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
        Note:
            requires at least an empty list

    roles (list):
        roles to inherit from
        Note:
            requires at least an empty list

    .. code-block:: yaml

        create_role:
          nexus3_roles.present:
            - name: test_role 
            - description: 'test role'
            - roles: ['nx-admin']
