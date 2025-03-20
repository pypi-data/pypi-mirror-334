"""
Libexec support running and manipulating files and sysroots in different environments.

This library provides an API to copy files and folders and runs script on Linux hosts
in a shell, a fakeroot, a sudo or a chroot environment. When sudo is used, the password
can be provided in an interactive way, or using a protected file e.g. mode 600 and
placed in the users home directory.

The commands are executed by the `Exec` class:

.. autoclass:: libexec.exec.Exec
    :members:
    :noindex:

The commands to execute are represented as `CommandSpec`:

.. autoclass:: libexec.exec.CommandSpec
    :members:
    :noindex:

The execution results are provided as `CommandResult`

.. autoclass:: libexec.exec.CommandResult
    :members:
    :noindex:

The class `Files` provides a comfort layer for using `Exec` for file copying and script execution.

.. autoclass:: libexec.files.Files
    :noindex:

For usage with `Files`, file copy operations are represented as `FileMetadata`:

.. autoclass:: libexec.files.FileMetadata
    :members:
    :noindex:

And scripts are represented as `ScriptMetadata`:

.. autoclass:: libexec.files.FileMetadata
    :members:
    :noindex:

If files or scripts are specified by in configuration files, the following `pydantic` classes can be used:

.. autoclass:: libexec.files.FileConfig
    :members:
    :noindex:

.. autoclass:: libexec.files.ScriptConfig
    :members:
    :noindex:

And parsed using:

.. autofunction:: libexec.files.parse_files
    :noindex:

.. autofunction:: libexec.files.parse_scripts
    :noindex:

"""

__version__ = "1.0.1"
