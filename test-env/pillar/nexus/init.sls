nexus:
  blobstores:
    docker: []
    maven:
      - quota_type: spaceRemainingQuota
      - quota_limit: 1000000000
    s3blobstore:
      - store_type: s3
      - s3_bucket: nexus3
      - s3_accessKeyId: AKIAIOSFODNN7EXAMPLE
      - s3_secretAccessKey: wJalrXUtnFEMIK7MDENGbPxRfiCYEXAMPLEKEY
      - s3_endpoint: http://minio:9000
      - s3_forcePathStyle: True
    unwanted-blobstore:
      - quota_type: spaceRemainingQuota
      - quota_limit: 1000000000
    yum: []
  privileges:
    repo-admin:
      - actions: ['ALL']
      - description: 'test repo admin'
      - format: maven2
      - repository: '*'
      - type: repository-admin
    unwanted-privilege:
      - actions: ['ALL']
      - description: 'unwanted privilege'
      - format: maven2
      - repository: '*'
      - type: repository-admin
  repositories:
    yum-proxy:
      - format: yum
      - type: proxy
      - remote_url: https://rpm.somerepo.com/
      - blobstore: yum
      - remote_username: username
      - remote_password: password
    yum-proxy-noauth:
      - format: yum
      - type: proxy
      - remote_url: https://rpm.someotherrepo.com/
      - blobstore: yum
    yum-group:
      - format: yum
      - type: group
      - group_members: ['yum-proxy']
      - strict_content_validation: False
    docker-hosted:
      - format: docker
      - type: hosted
      - blobstore: docker
      - docker_http_port: 5000
    docker-proxy:
      - format: docker
      - type: proxy
      - remote_url: https://registry-1.docker.io
      - blobstore: docker
      - docker_http_port: 5001
      - docker_force_auth: False
      - docker_index_type: HUB
    maven-hosted:
      - format: maven2
      - type: hosted
      - maven_version_policy: release
      - maven_layout_policy: strict
    maven-group:
      - format: maven2
      - type: group
      - group_members:
        - maven-hosted
    unwanted-hosted:
      - format: yum
      - type: hosted
      - blobstore: yum
  roles:
    repo-admin:
      - privileges: ['nx-repository-admin-*-*-*']
      - description: 'role with privileges to administer repositories'
      - roles: ['nx-anonymous']
    repo-user:
      - privileges: ['nx-repository-view-*-*-read']
      - description: 'role with privileges to read repositories'
      - roles: ['nx-anonymous']
    unwanted-role:
      - privileges: ['nx-repository-view-*-*-read']
      - description: 'unwanted rolewith privileges to read repositories'
      - roles: ['nx-anonymous']
  tasks:
    database_backup:
      typeId: 'db.backup'
      taskProperties: 
        location: '/nexus-data/backup'
      cron: '0 0 21 * * ?'
    docker-garbage-collection:
      typeId: repository.docker.gc
      taskProperties:
        repositoryName: '*'
      cron: '0 0 11 * * ?'
    docker-compact-blobstore:
      typeId: blobstore.compact
      taskProperties:
        blobstoreName: 'docker'
      cron: '0 0 13 * * ?'
  users:
    repo-admin:
      - firstName: Repo
      - lastName: Admin
      - emailAddress: repo-admin@nowhere.com
      - roles: ['repo-admin']
      - password: 'S3cr3tP4ssw0rd1'
    repo-user:
      - firstName: Repo
      - lastName: User
      - emailAddress: repo-user@nowhere.com
      - roles: ['repo-user']
      - password: 'S3cr3tP4ssw0rd2'
    unwanted-user:
      - firstName: Unwanted
      - lastName: User
      - emailAddress: unwanted-user@nowhere.com
      - roles: ['nx-anonymous']
      - password: 'S3cr3tP4ssw0rd3'
