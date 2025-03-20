"""Process files and scripts."""

import copy
import uuid
import glob
import logging
import os
import tempfile
import tarfile

from pathlib import Path
from typing import Optional
from dataclasses import dataclass

from pydantic import BaseModel

from libexec.exec import Environment, Exec, CommandResult, CommandSpec


@dataclass
class ScriptMetadata:
    """Metadata for script processing"""

    script: Path
    """Path to the script."""

    target: Optional[Path] = None
    """Copy script file to the given target."""

    workdir: Optional[Path] = None
    """Work directory when running the script."""

    chroot: Optional[Path] = None
    """Chroot root environment when running the script."""

    environment: Environment = Environment.SHELL
    """Environment for running the script."""

    check: bool = True
    """Check the result of the script execution."""


@dataclass
class FileMetadata:
    """Metadata for file processing"""

    source: Path
    """Source file."""
    destination_folder: Optional[Path] = None
    """Destination folder for copying the file."""
    destination_file: Optional[Path] = None
    """Destination file for copying the file."""
    user_id: Optional[int] = None
    """User ID of the new file. Default is keep the current UID."""
    group_id: Optional[int] = None
    """Group ID of the new file. Default is keep the current GID."""
    move: Optional[bool] = False
    """Move instead of copy."""
    delete_if_exists: Optional[bool] = False
    """Delete the destination before copying, if destination exists."""
    environment: Environment = Environment.SUDO
    """Environment for copying the file. Default is sudo."""
    chroot: Optional[Path] = None
    """Root folder of the chroot."""
    executable: Optional[bool] = None
    """Mark as executable."""


class FilesError(Exception):
    """Raised if file processing action failed."""


def _get_random_free_filename(parent: Path) -> Path:
    """
    Generate a radom not existing file name in the given parent folder.

    :param parent: Parent folder.
    :returns: Non-existing file path.
    """
    while True:
        name = str(uuid.uuid4())
        file = parent / name
        if not os.path.isfile(file):  # pragma: no branch
            return file


class Files:
    """Process files and scripts."""

    def __init__(self, sysroot: Path, exec: Optional[Exec] = None) -> None:
        """
        Create a new Files instance.

        :param sysroot: Sysroot folder.
        :param exec: Exec instance for running commands.
        """
        if exec:
            self._exec: Exec = exec
        else:
            self._exec = Exec()

        self._sysroot = sysroot
        os.makedirs(self._sysroot, exist_ok=True)

    def copy_files(self, files: list[FileMetadata]) -> list[CommandResult]:
        """
        Copy files.

        :param files: Metadata for the files to copy.
        :returns: The CommandResults of the copy commands.
        """
        results: list[CommandResult] = []

        for file in files:
            results.extend(self.copy_file(file))

        return results

    def copy_file(self, file: FileMetadata) -> list[CommandResult]:
        """
        Copy file.

        :param file: Metadata for the file to copy.
        :returns: The CommandResult of the copy commands.
        :raises FilesError: FilesError is raised in case of severe processing errors.
        """
        results: list[CommandResult] = []

        file = copy.copy(file)

        if file.environment == Environment.CHROOT and not file.chroot:
            file.chroot = self._sysroot

        matches = list(glob.glob(str(file.source)))

        if file.environment == Environment.CHROOT and not file.source.is_absolute() and len(matches) == 0:
            assert file.chroot
            chroot_based_source = file.chroot / file.source
            logging.info(
                "No matches for %s on host. Trying to match in chroot %s (%s).",
                file.source,
                file.chroot,
                chroot_based_source,
            )
            matches = list(glob.glob(str(chroot_based_source)))

        if file.destination_file and len(matches) > 1:
            raise FilesError(
                f"The file {file.source} matches multiple files ({matches}), but only one target {file.destination_file} is given!"
            )

        for match in matches:
            if file.environment == Environment.CHROOT and file.source.is_absolute():
                src = Path(match).absolute()
            else:
                src = Path(match).absolute()

            if file.destination_file:
                dst = file.destination_file
            else:
                dst = Path(src.name)

            # If the dst is already absolute, Path / dst will be dst.
            if file.destination_folder:
                dst = file.destination_folder / dst

            if file.environment == Environment.CHROOT:
                assert file.chroot
                dst = file.chroot / dst
            else:
                dst = self._sysroot / dst

            dst = dst.absolute()

            if file.delete_if_exists:
                if file.environment == Environment.CHROOT or file.environment == Environment.SUDO:
                    env = Environment.SUDO
                else:
                    env = Environment.SHELL
                self._exec.exec(CommandSpec(command=f"rm -f {dst}", environment=env))

            move = file.move

            if file.environment == Environment.CHROOT and file.chroot and not str(src).startswith(str(file.chroot)):
                # Copy src to chroot.
                chroot_src = _get_random_free_filename(file.chroot)
                results.append(
                    self._exec.exec(
                        CommandSpec(command=f"cp {src} {chroot_src}", environment=Environment.SUDO, capture_output=True)
                    )
                )
                src = chroot_src
                move = True

            if file.environment == Environment.CHROOT:
                # Convert paths to chroot.
                if not str(dst).startswith(str(file.chroot)):
                    raise FilesError(f"Destination {dst} is not in chroot {file.chroot}! File: {file}")

                assert file.chroot
                src = Path(f"/{src.relative_to(file.chroot)}")
                dst = Path(f"/{dst.relative_to(file.chroot)}")

            if move:
                results.append(
                    self._exec.exec(
                        CommandSpec(
                            command=f"mv {src} {dst}",
                            environment=file.environment,
                            chroot=file.chroot,
                            capture_output=True,
                        )
                    )
                )
            else:
                results.append(
                    self._exec.exec(
                        CommandSpec(
                            command=f"cp {src} {dst}",
                            environment=file.environment,
                            chroot=file.chroot,
                            capture_output=True,
                        )
                    )
                )

            # Process UID and GID.
            if file.user_id is not None:
                self._exec.exec(
                    CommandSpec(
                        command=f"chown {file.user_id} {dst}", environment=Environment.SUDO, capture_output=True
                    )
                )
            if file.group_id is not None:
                self._exec.exec(
                    CommandSpec(
                        command=f"chown :{file.group_id} {dst}", environment=Environment.SUDO, capture_output=True
                    )
                )

            # Handle executable flag.
            if file.executable is not None:
                if file.executable is True:
                    self._exec.exec(
                        CommandSpec(command=f"chmod +x {dst}", environment=Environment.SUDO, capture_output=True)
                    )
                else:
                    self._exec.exec(
                        CommandSpec(command=f"chmod -x {dst}", environment=Environment.SUDO, capture_output=True)
                    )

        return results

    def run_scripts(self, scripts: list[ScriptMetadata]) -> list[CommandResult]:
        """
        Run scripts.

        :param scripts: ScriptMetadata for the scripts execution.
        :returns: CommandResults of the script execution.
        """
        results: list[CommandResult] = []

        for script in scripts:
            results.extend(self.run_script(script))

        return results

    def run_script(self, script: ScriptMetadata) -> list[CommandResult]:
        """
        Run the given script in the sysroot.

        :param script: ScriptMetadata for the script execution.
        :returns: CommandResult.
        :raises FilesError: FilesError is raised in case of severe processing errors.
        """
        results: list[CommandResult] = []

        script = copy.copy(script)

        if script.environment == Environment.CHROOT and not script.chroot:
            script.chroot = self._sysroot

        matches = list(glob.glob(str(script.script)))

        if script.environment == Environment.CHROOT and not script.script.is_absolute() and len(matches) == 0:
            assert script.chroot
            chroot_based_source = script.chroot / script.script
            logging.info(
                "No matches for script %s on host. Trying to match in chroot %s (%s).",
                script.script,
                script.chroot,
                chroot_based_source,
            )
            matches = list(glob.glob(str(chroot_based_source)))

        if script.target and len(matches) > 1:
            raise FilesError(
                f"The file {script.target} matches multiple files ({matches}), but only one target {script.target} is given!"
            )

        for match in matches:
            script_file = Path(match).absolute()

            if script.target:
                file_meta = FileMetadata(source=script_file, destination_file=script.target, executable=True)
                self.copy_file(file_meta)
                script_file = script.target

            if script.environment == Environment.CHROOT and not str(script_file).startswith(str(script.chroot)):
                # Copy script to chroot
                assert script.chroot
                destination = _get_random_free_filename(script.chroot)
                file_meta = FileMetadata(source=script_file, destination_file=destination, executable=True)
                self.copy_file(file_meta)
                script_file = destination

            # Ensure script is executable
            if script.environment == Environment.CHROOT or script.environment == Environment.SUDO:
                environment = Environment.SUDO
            else:
                environment = Environment.SHELL
            self._exec.exec(CommandSpec(command=f"chmod +x {script_file}", environment=environment, check=False))

            if script.environment == Environment.CHROOT:
                # Convert path to chroot.
                assert script.chroot
                script_file = Path(f"/{script_file.relative_to(script.chroot)}")
                if script.workdir is None:
                    script.workdir = script.chroot
                else:
                    script.workdir = Path(f"/{script.workdir.absolute().relative_to(script.chroot)}")

            results.append(
                self._exec.exec(
                    CommandSpec(
                        command=str(script_file),
                        environment=script.environment,
                        workdir=script.workdir,
                        chroot=script.chroot,
                        check=script.check,
                    )
                )
            )

        return results

    def extract_tarball_as_sysroot(self, tarball: Path, sudo: bool = False) -> None:
        """
        Extract tar archive to the sysroot directory.

        :param tarball: Path to the tarball.
        :param sudo: Use sudo for extraction.
        """
        if not sudo:
            with tarfile.open(tarball) as tar:
                tar.extractall(self._sysroot)
        else:
            self._exec.exec(CommandSpec(command=f"tar -xf {tarball} -C {self._sysroot}", environment=Environment.SUDO))

    def pack_sysroot_as_tarball(
        self,
        tarball: Optional[Path] = None,
        compression: Optional[str] = None,
        environment: Environment = Environment.SHELL,
    ) -> Path:
        """
        Create tar archive of sysroot folder.


        :param tarball: Path of the tarball to create.
        :param compression: Compression string, e.g. gz or xz.
        :param environment: Environment to use for compression, not CHROOT.
        :returns: Path to the created tarball.
        :raises FilesError: If environment is CHROOT.
        """
        if environment == Environment.CHROOT:
            raise FilesError("CHROOT environment is not supported for pack_sysroot_as_tarball!")

        if not tarball:
            tarball = Path(tempfile.mktemp(prefix="sysroot", suffix=".tar"))

            if compression:
                compressed_tarball = Path(str(tarball) + "." + compression)
            else:
                compressed_tarball = tarball
        else:
            compressed_tarball = tarball

        if environment == Environment.SHELL:
            # Use python functions.
            mode: str = "w"
            if compression:
                mode = f"w:{compression}"
                tarball = compressed_tarball

            with tarfile.open(name=tarball, mode=mode) as tar:  # type: ignore
                tar.add(self._sysroot, arcname=os.path.sep)
        else:
            self._exec.exec(
                CommandSpec(
                    command=f"tar -cf {tarball.absolute()} *",
                    environment=environment,
                    capture_output=True,
                    workdir=self._sysroot,
                )
            )
            if compression:
                if compression == "xz":
                    self._exec.exec(
                        CommandSpec(command=f"xz {tarball.absolute()}", environment=environment, capture_output=True)
                    )
                    tarball = Path(str(tarball) + ".xz")
                    if tarball != compressed_tarball:
                        self._exec.exec(
                            CommandSpec(
                                command=f"mv {tarball.absolute()} {compressed_tarball.absolute()}",
                                environment=environment,
                                capture_output=True,
                            )
                        )
                    tarball = compressed_tarball
                elif compression == "gz":
                    self._exec.exec(
                        CommandSpec(command=f"gzip {tarball.absolute()}", environment=environment, capture_output=True)
                    )
                    tarball = Path(str(tarball) + ".gz")
                    if tarball != compressed_tarball:
                        self._exec.exec(
                            CommandSpec(
                                command=f"mv {tarball.absolute()} {compressed_tarball.absolute()}",
                                environment=environment,
                                capture_output=True,
                            )
                        )
                    tarball = compressed_tarball
                elif compression == "bz2":
                    self._exec.exec(
                        CommandSpec(command=f"bzip2 {tarball.absolute()}", environment=environment, capture_output=True)
                    )
                    tarball = Path(str(tarball) + ".bz2")
                    if tarball != compressed_tarball:
                        self._exec.exec(
                            CommandSpec(
                                command=f"mv {tarball.absolute()} {compressed_tarball.absolute()}",
                                environment=environment,
                                capture_output=True,
                            )
                        )
                    tarball = compressed_tarball
                else:
                    logging.error("Unknown compression: %s", compression)

        return tarball


class ScriptConfig(BaseModel):
    """Config entry for a script."""

    name: Path
    env: Optional[Environment] = None


def parse_script(script: ScriptConfig | str) -> ScriptMetadata:
    """
    Convert ScriptConfig object or string to ScriptMetadata object.

    :param script: ScriptConfig or string representing path.
    :returns: ScriptMetadata.
    """
    if isinstance(script, ScriptConfig):
        if script.env:
            return ScriptMetadata(script=script.name, environment=script.env)
        else:
            return ScriptMetadata(script=script.name)
    else:
        return ScriptMetadata(script=Path(script))


def parse_scripts(scripts: list[ScriptConfig | str]) -> list[ScriptMetadata]:
    """
    Convert ScriptConfig objects or strings to ScriptMetadata objects.

    :param scripts: List of ScriptConfig or strings representing paths.
    :returns: List of ScriptMetadata.
    """
    parsed_scripts: list[ScriptMetadata] = []

    for entry in scripts:
        parsed_scripts.append(parse_script(entry))

    return parsed_scripts


class FileConfig(BaseModel):
    """Config entry for a file."""

    source: Path
    """Path of the file."""
    destination: Path
    """Destination path of the file. Can be absolute or relative to the sysroot."""


def parse_file(file: FileConfig | str) -> FileMetadata:
    """
    Convert FileConfig object or string to FileMetadata object.

    :param file: FileConfig or string representing path.
    :returns: FileMetadata.
    """
    if isinstance(file, FileConfig):
        return FileMetadata(source=file.source, destination_file=file.destination)
    else:
        f: Path = Path(file)
        if f.is_absolute():
            # Copy e.g. /etc/resolv.conf to sysroot/etc/resolv.conf by stripping the leading /
            return FileMetadata(source=f, destination_file=Path(str(f)[1:]))
        else:
            # Copy e.g. folder/some.txt to sysroot/folder/some.txt
            return FileMetadata(source=f, destination_file=f)


def parse_files(files: list[FileConfig | str]) -> list[FileMetadata]:
    """
    Convert FileConfig objects or strings to FileMetadata objects.

    :param files: List of FileConfig or strings representing paths.
    :returns: List of FileMetadata.
    """
    parsed_files: list[FileMetadata] = []

    for entry in files:
        parsed_files.append(parse_file(entry))

    return parsed_files
