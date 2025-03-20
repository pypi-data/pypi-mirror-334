Files Module
============

.. automodule:: libexec.files

The `Files` class handles file copy operations and script execution operations.

File copy operations are defined using `FileMetadata`:

.. autoclass:: libexec.files.FileMetadata
    :members:

Script executions are defined using `ScriptMetadata`:

.. autoclass:: libexec.files.ScriptMetadata
    :members:

And then processed by `Files`:

.. autoclass:: libexec.files.Files
    :members:

If a critical problem is detected when processing a file or script operation,
a `FilesError` is raised.

.. autoclass:: libexec.files.FilesError

Handling sysroots is supported with `Files.extract_tarball_as_sysroot` and
`Files.pack_sysroot_as_tarball`.

Scripts and files from config files
-----------------------------------

Defining scripts and file copy operations using config files is supported with the
`libyamlconf` compatible classes `ScriptConfig` and `FileConfig`:

.. autoclass:: libexec.files.ScriptConfig
    :members:

.. autoclass:: libexec.files.FileConfig
    :members:

Parsing such config entries is supported by the following functions:

.. autofunction:: libexec.files.parse_file

.. autofunction:: libexec.files.parse_files

.. autofunction:: libexec.files.parse_script

.. autofunction:: libexec.files.parse_scripts

Internal support functions
--------------------------

.. autofunction:: libexec.files._get_random_free_filename
