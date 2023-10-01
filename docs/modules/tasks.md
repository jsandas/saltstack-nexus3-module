nexus3_tasks.**describe**(*id*):

    id (str):
        task id

    CLI Example::

    .. code-block:: bash

        salt myminion nexus3_tasks.describe id=512be2c3-aa04-448f-b0ce-2047eee34903

nexus3_tasks.**list_all**():

    CLI Example::

    .. code-block:: bash

        salt myminion nexus3_tasks.list_all

nexus3_tasks.**run**(*id*):

    id (str):
        task id

    CLI Example::

    .. code-block:: bash

        salt myminion nexus3_tasks.run id=512be2c3-aa04-448f-b0ce-2047eee34903

nexus3_tasks.**stop**(*id*):
    id (str):
        task id

    CLI Example::

    .. code-block:: bash

        salt myminion nexus3_tasks.stop id=512be2c3-aa04-448f-b0ce-2047eee34903
