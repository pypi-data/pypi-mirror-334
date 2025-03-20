Exec Module
===========

.. automodule:: libexec.exec


The core of libexec is the `Exec` class.

.. autoclass:: libexec.exec.Exec
    :members:

It takes `CommandSpec` objects, executes the commands, and returns the result as `CommandResult` objects.

.. autoclass:: libexec.exec.CommandSpec
    :members:

.. autoclass:: libexec.exec.CommandResult
    :members:

If commands are executed in a _chroot_ environment, also sudo is required.
If the `sudo` command needs a password, the password can be either provided
as path to a file given to `Exec.__ini__`, or is asked interactive once.
The module is implemented in a way, that `sudo` is avoided where possible safely.
If a command is executed in a `chroot` environment, the Linux special filesystems
are made available in the `chroot` environment, and also necessary files like `/etc/resolv.conf`
are made available. To allow the modification of existing files in the `chroot`
environment, the `chroot` folder is created as overlay mount of, 
the real chroot folder, a middle layer where the special filesystems and special
host files are provided, and a writeable upper layer.
When closing the `chroot`, the modified files are merged back to the chroot folder.
