nexus3_email.**configure**(*enabled,fromAddress='nexus@example.org',host='localhost',nexusTrustStoreEnabled=False,password=None,port=0,sslOnConnectEnabled=False,sslServerIdentityCheckEnabled=False,startTlsEnabled=False,startTlsRequired=False,subjectPrefix=None,username=''*):

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
            tls_connect and starttls should be mutually exclusive

    sslServerIdentityCheckEnabled (bool):
        verify server certificate (Default: False)

    startTlsEnabled (bool):
        enable starttls (Default: False)
        Note:
            tls_connect and starttls should be mutually exclusive

    startTlsRequired (bool):
        require starttls (Default: False)
        Note:
            tls_connect and starttls should be mutually exclusive

    subjectPrefix (str):
        prefix for subject in emails (Default: None)

    username (str):
        smtp username (Default: '')

    CLI Example::

        salt myminion nexus3_email.configure enabled=True host=smtp.example.com

        salt myminion nexus3_email.configure enabled=False
    

nexus3_email.**describe**():

    CLI Example::

        salt myminion nexus3_email.describe
    

nexus3_email.**reset**():

    CLI Example::

        salt myminion nexus3_email.reset
    

nexus3_email.**verify**(*to*):

    CLI Example::
    
    to (str):
        address to send test email to
    
        salt myminion nexus3_email.verify to=test@domain.com
