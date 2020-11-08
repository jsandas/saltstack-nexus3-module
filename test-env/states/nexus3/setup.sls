include:
  - .blobstores
  - .repositores
  - .privileges
  - .roles
  - .users
  - .scripts

set_anonymous_access_true:
  nexus3_security.anonymous_access:
    - enabled: True

update_realms:
  nexus3_security.realms:
    - realms: 
      - NexusAuthenticatingRealm
      - NexusAuthorizingRealm
      - DockerToken

setup_email:
  nexus3_email.configure:
    - enabled: True
    - host: smtp.example.com
    - port: 587
    - fromAddress: test@example.com
    - startTlsEnabled: True


