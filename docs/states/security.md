nexus3_security.anonymous_access(*name,enabled*):

    name (str):
        state id name
        Note:
            do not provide this argument, this is only here
            because salt passes this arg always
    
    enabled (bool):
        enable or disable anonymous access [True|False]

    .. code-block:: yaml

        set_anonymous_access:
          nexus3_security.anonymous_access:
            - enabled: True


nexus3_security.realms(*name,realms*):

    name (str):
        state id name
        Note:
            do not provide this argument, this is only here
            because salt passes this arg always
    
    realms (list):
        list of realms in order they should be used 
        Note:
            Include all desired realms in list as this will override
            the current list

    .. code-block:: yaml

        update_realms:
          nexus3_security.realms:
            - realms: ['NexusAuthenticatingRealm','NexusAuthorizingRealm','NpmToken','DockerToken']

        update_realms:
          nexus3_security.realms:
            - realms: 
              - NexusAuthenticatingRealm
              - NexusAuthorizingRealm
              - NpmToken
              - DockerToken
