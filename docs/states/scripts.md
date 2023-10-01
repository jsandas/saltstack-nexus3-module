nexus3_scripts.base_url(*name*):

    Set base url for Nexus

    name (str):
      URL to set base_url to for Nexus 3

      Note:
        This would usually be the FQDN used
        to access Nexus

    .. code-block:: yaml

      http://localhost:8081:
      nexus3_scripts.base_url


nexus3_scripts.task(*name,typeId,taskProperties,cron,setAlertEmail=None*):

    name (str):
        Name of task

    typeId (str):
        Nexus taskId [db.backup|repository.docker.gc|repository.docker.upload-purge|blobstore.compact|repository.purge-unused]

    taskProperties (dict):
        Dictionary of the task properties
        Note:
            The key/values under task_properties is indented 4 spaces instead
            of two.  This is how salt creates a dictionary from the yaml

    setAlertEmail (str):
        Email to send alerts to

    cron (str):
        Cron-like string to schedule task runs

        .. example::
            '0 0 11 * 5 ?'

        Note:
            Cron schedule notes:
            Field Name	Allowed Values
            Seconds	    0-59
            Minutes	    0-59
            Hours	    0-23
            Dayofmonth	1-31
            Month	    1-12 or JAN-DEC
            Dayofweek	1-7 or SUN-SAT
            Year(optional)	empty, 1970-2099

    .. code-block:: yaml

      database_backup:
        nexus3_scripts.tasks:
          - task_type_id: 'db.backup'
          - task_properties:
              location:'/nexus-data/backup'
          - task_cron: '0 0 21 * * ?'
