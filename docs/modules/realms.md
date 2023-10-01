nexus3_realms.**list_active**():

    CLI Example::

        salt myminion nexus3_realms.list_active
    

nexus3_realms.**list_all**():

    CLI Example::

        salt myminion nexus3_realms.list_all
    

nexus3_realms.**reset**():

    Resets realms to default

    CLI Example::

        salt myminion nexus3_realms.reset
    

nexus3_realms.**update**(*realms*):

    realms (list):
        list of realms in order they should be used 
        Note:
            Include all desired realms in list as this will override
            the current list

    CLI Example::

        salt myminion nexus3_realms.update realms="['NexusAuthenticatingRealm','NexusAuthorizingRealm','NpmToken','DockerToken']"
