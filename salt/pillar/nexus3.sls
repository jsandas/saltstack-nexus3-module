nexus3:
  blobstores:
    apt: []
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
    apt-hosted:
      - format: apt
      - type: hosted
      - blobstore: apt
      - apt_gpg_priv_key: LS0tLS1CRUdJTiBQR1AgUFJJVkFURSBLRVkgQkxPQ0stLS0tLQoKbFFIWUJHTWY1YU1CQkFETlgyRTBVZlcvUHdEczB6bGNIRnExeVhaMFppS2ZXRTgyU0lURU51UHcwVzRuc1o2dgpKRnNzMk96MWlrZWpNOEN1SFNmZXVkWkE5TkFsRjJHbDQ3R2xOQzlORlFxWHVLMlh2Z0F3UXFFWkkvaWhXRzlmCmxxdFBDS2tHTHFzSnFjTmU1LzRlVklmUWxSdUl4R0tlbWRLV3htUFlaNkcvcEY5Zng4aENyQ1ViQVFBUkFRQUIKQUFQOUZTaWVleVYyakIyUm10U29ORFUzbzBMK1VUKzBrWFluc3hBRm5iR0tDbVdKVTgyWTY3SnpNa3VuSGlVQQovRzk0aW5lMmc5dmhsdytoNGpCbWZ4RFdYRitpcm83K1AzaE9MSUxQVDhiNWpVN1BQV3lzSi8wc3hieDJ5bXR4CkdkQWdobTFNd1FIUEVYQkx1dkpQQmlZeUhlOVNEa0FtM1J2Ymx6eWVEV05xTjRFQ0FPRVBPRlNnVUV4YXpEdTEKRGlYZkNhWGZLN1liQy90ZGIzNjNvNkpZOGVCVmlUeHhSRmdQdW9DMENFOGxqZzJBRmJMMXc2OEwzbUZ2TzZRTApkVDlpdk5NQ0FPbWJTK1JUNUVzTVBpQXRUMThpV21YM0Jpc1EwRGc5L1lVNHRQZENId1VZRFBUVkd2TmQ0TGhOCm1NdzNTTVJ0Q2g3MDJKU1puNlJHeGN6SnhPQldsRnNDQU1TN2pCQytwQTEreUlwbC9FWjdmWElWNm8rRGZPQ3oKdzBaekg2TE9jMXpnbDRZZVhoTmR6SWVTcE1KaTg2bTArQlM0TW9IR1gwbGFhRnI4ZGVhZmVpNlprclFNZEdWegpkQzFuY0djdGEyVjVpTTRFRXdFS0FEZ1dJUVI0WWdNS2Z0TGMzZ3VVaE1mejR0U3lkOFdzVlFVQ1l4L2xvd0liCkF3VUxDUWdIQWdZVkNna0lDd0lFRmdJREFRSWVBUUlYZ0FBS0NSRHo0dFN5ZDhXc1ZRYWRBLzBmYlFYeE1MTjkKZ1dIeDZTVElRbElNN3prL2diQ2k4WFlVNVd3Zmt5bDR0bHdUWUMrUXVOb0luZ1ZXakQ3L0IzYUFQdEt3VGVOSwppck5tTnNNczNuTXZNdXgzQk9WYWdJREpqLy9YZ0gyOHE4WEt1VTlmTnJ4NnRQUkJVMWIxTjhTRld3OHcwMmplCm9mdE9ZbzhrUUFWSDR1cGZYekZvQldhNHdjVU0weEtPeUowQjJBUmpIK1dqQVFRQXBwMDFDMVAxb3ZFcjdaYTkKeTZTdWU2eFc2UHFpazJiM0dKWFJ4SGxpN1AzWEw5ZGtEWFNtZjVHOEtSdU5GMGRnY0J3ZTVtVEJNRjhta21kSApmZytQY3phUUNzY3FvS0I2b0JVTUlYWTArZWE1eWRYb2NTNytURmt0UWVNUjZEenR4d1RndC9SWHBwY3B5N3B4CmtBZktWYnV3a2RzUUg1bkJFajlORUtXdDZja0FFUUVBQVFBRC9SdFhUK1dRZlE0a21tdE9JYzRoczVwSzRTWXgKUHUyR1o0VUt6Tlg3ZjI3Wmh1N3NYeGhRTEtSaGcybVJnbGt3RnRTKzRKazVMblNrSUozRXdmZ2ZVSkE1S29zVgpNaUppUnpvK1U3L0Y2Mk45SHdHbHVCTGkrODdBV1BRYzc5WjZoQnA0eDBGZ1NCWWVLVWhvUytnZEI3TG5GWm5LCjRZbk5FbWdaQUY2aE1rS3BBZ0RGcmNsQ01Xc2pWZ3I3RnZuaVIvWWJOQmxIa05EckpkaEtwc1AvbUhlVXg3ejAKVzdZMU9jeEVMR0VsTjllZjA0QnJZTzdMcUE4UUk2QWFpcUwyRmVmZEFnRFh4U3htUy85UUk0alhUb0FmNmNxawpNcm4wQnhVdFRHdTR2aWlIc3dNVUlpallqUXlFV0cvVXhZanJVU2hTY3luQWFuZU1BelBvWEtLdW52NDc2OERkCkFnQzFmeDZDU1RDTUxNQXUwZlliSHdDaXNWMTNVZEJrbXhraThLdnEwMG5vVGRhY1lWMG0vU1IzOUhVWmNYcUIKRkNYbTQ4eDlsZVU4ZDNkdjV0SjFsOGp0bk5HSXRnUVlBUW9BSUJZaEJIaGlBd3ArMHR6ZUM1U0V4L1BpMUxKMwp4YXhWQlFKakgrV2pBaHNNQUFvSkVQUGkxTEozeGF4VlEwc0QvUlJJK3U2QkFHOHE0d0E4KzN6OFI5R3JCSlROCmhHTktiNHpDMU1PaklYbkVselNWWm1FTWFIVVlzajRqY3FsT2hBNFBzQ0JZM2dMSUc4cWsrMlpGcytSMFowREYKRTltaGJ5QVBWUEQxU0QyandHSTNINDhLcHVMSzVTZUhOWHZkdWxGaUdWRXlyczE2V3N6bG5sMmxPWjkzb0ovNApFUGtNc0FrWHhjUmRFVkJCCj10c2YxCi0tLS0tRU5EIFBHUCBQUklWQVRFIEtFWSBCTE9DSy0tLS0tCg==
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
    npm-proxy:
      - format: npm
      - type: proxy
      - remote_url: https://npm.somerepo.com/
      # currently setting the bearer token for NPM is not possible
      # with the Nexus REST API at this time.
      # https://github.com/sonatype/nexus-public/issues/247
      # - remote_auth_type: bearerToken
      # - remote_bearer_token: password
    yum-proxy:
      - format: yum
      - type: proxy
      - remote_url: https://rpm.somerepo.com/
      - blobstore: yum
      - remote_username: username
      - remote_password: password
    yum-group:
      - format: yum
      - type: group
      - group_members: ['yum-proxy']
      - strict_content_validation: False
    yum-proxy-noauth:
      - format: yum
      - type: proxy
      - remote_url: https://rpm.someotherrepo.com/
      - blobstore: yum
    maven-group:
      - format: maven2
      - type: group
      - group_members:
        - maven-hosted
    maven-hosted:
      - format: maven2
      - type: hosted
      - maven_version_policy: release
      - maven_layout_policy: strict
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
