nexus3_readonly.**describe**():

    CLI Example::

    .. code-block:: bash

        salt myminion nexus3_readonly.describe


nexus3_readonly.**enabled**(*state, force_release=True*):

    state (bool):
        enable or disable read-only [True|False]

    force_release (bool):
        force release of read-only [True|False] (Default: False)

    CLI Example::

    .. code-block:: bash

        salt myminion nexus3_readonly.enabled True
        salt myminion nexus3_readonly.enabled state=False
