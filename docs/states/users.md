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
        Note:
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
