nexus3_email.clear(*name*):

    name (str):
        state id name
        Note:
            do not provide this argument, this is only here
            because salt passes this arg always

    .. code-block:: yaml

        clear_email:
          nexus3_email.clear


nexus3_email.configure(*name,enabled,fromAddress='nexus@example.org',host='localhost',nexusTrustStoreEnabled=False,password=None,port=0,sslOnConnectEnabled=False,sslServerIdentityCheckEnabled=False,startTlsEnabled=False,startTlsRequired=False,subjectPrefix=None,username=''*):

    name (str):
        state id name
        Note:
            do not provide this argument, this is only here
            because salt passes this arg always

    enabled (bool):
        enable email support [True|False]

    fromAddress (str):
        mail from address (Default: nexus@example.org)

    host (string):
        smtp hostname (Default: localhost)

    nexusTrustStoreEnabled (bool):
        use nexus truststore [True|False] (Default: False)
        Note:
            Ensure CA certificate is add to the Nexus trustore

    password (str):
        smtp password (Default: None)
       
    port (int):
        smtp port (Default: 0)

    sslOnConnectEnabled (bool):
        connect using tls (SMTPS) (Default: False)
        Note:
            sslOnConnectEnabled and startTlsEnabled/startTlsRequired should be mutually exclusive

    sslServerIdentityCheckEnabled (bool):
        verify server certificate (Default: False)

    startTlsEnabled (bool):
        enable starttls (Default: False)
        Note:
            sslOnConnectEnabled and startTlsEnabled/startTlsRequired should be mutually exclusive

    startTlsRequired (bool):
        require starttls (Default: False)
        Note:
            sslOnConnectEnabled and startTlsEnabled/startTlsRequired should be mutually exclusive


    subjectPrefix (str):
        prefix for subject in emails (Default: None)

    username (str):
        smtp username (Default: '')

    .. code-block:: yaml

        setup_email:
          nexus3_email.configure:
            - enabled: True
            - host: smtp@example.com
            - port: 587
            - fromAddress: test@example.com
            - startTlsEnabled: True
