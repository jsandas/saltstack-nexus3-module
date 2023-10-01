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
