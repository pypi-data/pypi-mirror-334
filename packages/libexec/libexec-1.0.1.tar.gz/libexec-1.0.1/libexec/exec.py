"""Run Linux shell commands in different environments."""

import logging
import os
import subprocess
import tempfile
import glob

from getpass import getpass
from enum import Enum
from io import BufferedWriter
from pathlib import Path
from subprocess import PIPE
from typing import Optional, Any
from dataclasses import dataclass


class CommandFailed(Exception):
    """Raised if a command returns and returncode which is not 0."""


class Environment(Enum):
    """Enumeration for execution environments."""

    SHELL = 0
    SUDO = 1
    FAKEROOT = 2
    CHROOT = 3


@dataclass
class CommandSpec:
    """
    Command specification.
    """

    command: str
    """Command to run."""

    environment: Environment = Environment.SHELL
    """Environment for running the command."""

    workdir: Optional[Path] = None
    """Current working directory for the command."""

    chroot: Optional[Path] = None
    """Chroot folder, if chroot is used."""

    stdout: Optional[BufferedWriter] = None
    """Writer to capture the stdout."""

    check: bool = True
    """Check the return code of the command."""

    capture_output: bool = False
    """Capture th command output. If false, the output will be visible on the terminal."""

    def __str__(self):
        return f"CommandSpec<command={self.command}, env={self.environment}>"

    def __repr__(self):
        return str(self)


@dataclass
class CommandResult:
    command: CommandSpec
    """The executed command."""

    exit_code: int
    """ The exit code for the command."""

    stdout: Optional[str] = None
    """The STDOUT output, if captured and not redirected to a file."""

    stderr: Optional[str] = None
    """The STDERR output, if captured."""

    def __str__(self):
        return f"CommandResult<command={self.command}, exit_code={self.exit_code}>"

    def __repr__(self):
        return str(self)


class Exec:
    """Run commands in environments."""

    def __init__(self, sudo_password_file: Optional[Path] = None) -> None:
        """
        Create a new Exec instance.

        :param sudo_password_file: Path to a file containing the sudo password.
        """

        self._use_sudo_password: bool = False
        self._sudo_password: Optional[str] = None

        self._chroot_host_config_layer: Optional[Path] = None
        self._chroot_modifications_layer: Optional[Path] = None
        self._chroot_workdir_layer: Optional[Path] = None
        self._chroot_merged_folder: Optional[Path] = None

        self.state: Path = Path(tempfile.mktemp())
        self.state.touch()

        if sudo_password_file and Path(sudo_password_file).is_file():
            logging.info("Loading sudo password from %s.", sudo_password_file)
            with open(sudo_password_file, "r", encoding="utf-8") as f:
                password = f.read()
            self._sudo_password = password.replace("\n", "")

        self._use_sudo_password = self._check_sudo_requires_password()
        logging.info("Use sudo password? %s", self._use_sudo_password)

    def __del__(self) -> None:
        """Cleanup the state file."""
        os.remove(self.state)

    def _check_sudo_requires_password(self) -> bool:
        """
        Test if sudo command requires a password.

        :returns: True if sudo requires a password.
        """
        result = self._run_cmd(CommandSpec(command="sudo -n mount", check=False, capture_output=True))
        return result.exit_code != 0

    def _run_cmd(self, command: CommandSpec) -> CommandResult:
        """
        Run a command using subprocess.

        :param command: Command to execute.
        :returns: CommandResult.
        :raises CommandFailed: If a command provides a return code != 0 and check is True.
        """
        logging.debug("Running command: %s", command)

        # Decide how to handle command output
        out: Any = None
        if command.capture_output:
            out = PIPE
        if command.stdout:
            out = command.stdout

        # Decide how to handle command error output
        err: Any = None
        if command.capture_output:
            err = PIPE

        logging.debug("Command output handling: out=%s err=%s", out, err)

        # Take care of sudo password.
        cmd = command.command

        if (
            command.environment == Environment.SUDO or command.environment == Environment.CHROOT
        ) and self._use_sudo_password:  # pragma: no cover
            # Host and timing / environment specific behavior
            logging.debug("Using sudo password for command %s.", command)
            if self._sudo_password is None:
                logging.debug("No sudo password. Using interactive password query.")
                self._sudo_password = getpass(prompt="Please enter the sudo password:")
            cmd = f'echo "{self._sudo_password}" | {cmd}'

        # Run the command - check is handled later, to get the stdout and stderr output.
        p = subprocess.run(cmd, check=False, shell=True, stdout=out, stderr=err, cwd=command.workdir)

        # Process the command output
        p_out: Optional[str] = None
        p_err: Optional[str] = None
        if command.capture_output and command.stdout is None:
            p_out = p.stdout.decode("utf8", errors="ignore")
            assert p_out is not None
            if p_out.strip():
                log_out = p_out.strip()
                if len(log_out) > 100:
                    log_out = f"{log_out[:100]}..."
                logging.debug("STDOUT: %s", log_out)

        if command.capture_output:
            p_err = p.stderr.decode("utf8", errors="ignore")
            assert p_err is not None
            if p_err.strip():
                log_err = p_err.strip()
                # no test needed
                if len(log_err) > 100:  # pragma: no cover
                    log_err = f"{log_err[:100]}..."
                logging.debug("Command %s had error output: : %s", command, log_err)

        # Handle the return code
        if p.returncode != 0:
            logging.debug("Returncode of command %s was not zero: %s", command, p.returncode)
            if command.check:
                logging.error("Execution of command %s failed with returncode %s!", command, p.returncode)
                raise CommandFailed(
                    f"Execution of command {command} failed with returncode {p.returncode}!\n"
                    f"returncode: {p.returncode}\n"
                    f"STDOUT:\n{p_out}"
                    f"STDERR:\n{p_err}"
                )

        return CommandResult(command=command, exit_code=p.returncode, stdout=p_out, stderr=p_err)

    def _special_folders(self, chroot: Path, mount: bool) -> None:
        """
        Mount special file systems to chroot folder.

        :param chroot: Base folder for mounting the special filesystems.
        :param mount: True for mounting, False for un-mounting.
        """
        if mount:
            logging.debug("Mounting special special filesystems to %s.", chroot)

            # Prepare overlay-mount middle folder
            self._chroot_host_config_layer = Path(tempfile.mkdtemp())
            os.makedirs(self._chroot_host_config_layer, exist_ok=True)
            # Prepare overlay-mount modifications folder
            self._chroot_modifications_layer = Path(tempfile.mkdtemp())
            os.makedirs(self._chroot_modifications_layer, exist_ok=True)
            # Prepare overlay-mount workdir folder
            self._chroot_workdir_layer = Path(tempfile.mkdtemp())
            os.makedirs(self._chroot_workdir_layer, exist_ok=True)
            # Prepare overlay-mount merged folder
            self._chroot_merged_folder = Path(tempfile.mkdtemp())
            os.makedirs(self._chroot_merged_folder, exist_ok=True)
        else:
            logging.debug("Un-mounting special special filesystems from %s.", chroot)

        # Special files from host
        files = [
            ("/etc/resolv.conf", "etc/resolv.conf"),
            ("/etc/gai.conf", "etc/gai.conf"),
            ("/proc/mounts", "etc/mtab"),
        ]

        if mount:
            assert self._chroot_host_config_layer
            # Copy special files form host.
            for file, target_name in files:
                target_file = self._chroot_host_config_layer / target_name
                self._sudo(
                    CommandSpec(
                        command=f"mkdir -p {target_file.parent}", capture_output=True, environment=Environment.SUDO
                    )
                )
                self._sudo(
                    CommandSpec(
                        command=f"cp -L {file} {target_file}", capture_output=True, environment=Environment.SUDO
                    )
                )

        # Special filesystems
        mounts = [
            ("dev", "-o bind"),
            ("dev/pts", "-o bind"),
            ("sys", "-t sysfs"),
            ("proc", "-t proc"),
        ]
        # Reverse order on unmounting
        if not mount:
            mounts.reverse()

        # Mount or umount the special folders
        for chroot_folder, mount_options in mounts:
            assert self._chroot_host_config_layer
            target_folder = self._chroot_host_config_layer / chroot_folder
            if mount:
                self._sudo(
                    CommandSpec(command=f"mkdir -p {target_folder}", capture_output=True, environment=Environment.SUDO)
                )
                self._sudo(
                    CommandSpec(
                        command=f"mount {mount_options} /{chroot_folder} {target_folder}",
                        capture_output=True,
                        environment=Environment.SUDO,
                    )
                )
            else:
                self._sudo(
                    CommandSpec(command=f"umount {target_folder}", capture_output=True, environment=Environment.SUDO)
                )

        if mount:
            # Create the overlay mount
            command = (
                f"mount -t overlay overlay -o lowerdir={chroot.absolute()}:{self._chroot_host_config_layer},"
                f"upperdir={self._chroot_modifications_layer},workdir={self._chroot_workdir_layer} {self._chroot_merged_folder}"
            )
            self._sudo(CommandSpec(command=command, capture_output=True, environment=Environment.SUDO))
        else:
            # Unmount the overlay mount
            assert self._chroot_merged_folder
            self._sudo(
                CommandSpec(
                    command=f"umount {self._chroot_merged_folder}", capture_output=True, environment=Environment.SUDO
                )
            )

            # Merge the modifications to the chroot folder
            assert self._chroot_modifications_layer
            for match in glob.glob("**/*", root_dir=self._chroot_modifications_layer, recursive=True):
                modified_file = self._chroot_modifications_layer / match
                target = chroot / match
                logging.debug("Copying modified file %s back to chroot %s.", match, chroot)
                # Remove target if it exists
                self._sudo(CommandSpec(command=f"rm -rf {target}", capture_output=True, environment=Environment.SUDO))
                # Create parent dir.
                self._sudo(
                    CommandSpec(command=f"mkdir -p {target.parent}", capture_output=True, environment=Environment.SUDO)
                )
                # Copy file. May fail is type is not copy-able.
                result = self._sudo(
                    CommandSpec(
                        command=f"cp -rf {modified_file} {target}",
                        capture_output=True,
                        environment=Environment.SUDO,
                        check=False,
                    )
                )
                if result.exit_code != 0:  # pragma: no cover
                    logging.error("Copying back modified file %s to chroot failed!", modified_file)

            # Cleanup the temporary folders
            self._sudo(
                CommandSpec(
                    command=f"rm -rf {self._chroot_modifications_layer}",
                    capture_output=True,
                    environment=Environment.SUDO,
                )
            )
            self._chroot_modifications_layer = None
            self._sudo(
                CommandSpec(
                    command=f"rm -rf {self._chroot_merged_folder}", capture_output=True, environment=Environment.SUDO
                )
            )
            self._chroot_merged_folder = None
            self._sudo(
                CommandSpec(
                    command=f"rm -rf {self._chroot_workdir_layer}", capture_output=True, environment=Environment.SUDO
                )
            )
            self._chroot_workdir_layer = None
            # Ensure special folders are unmounted
            result = self._sudo(
                CommandSpec(
                    command=f"mount | grep {self._chroot_host_config_layer}",
                    check=False,
                    capture_output=True,
                    environment=Environment.SUDO,
                )
            )
            if result.exit_code == 0:  # pragma: no cover
                # Should never happen, just to be on the save side and not endanger the host.
                logging.critical(
                    "Unmounting special folders failed! Will not cleanup host layer folder %s.",
                    self._chroot_host_config_layer,
                )
            else:
                self._sudo(
                    CommandSpec(
                        command=f"rm -rf {self._chroot_host_config_layer}",
                        capture_output=True,
                        environment=Environment.SUDO,
                    )
                )
            self._chroot_host_config_layer = None

    def _fakeroot(self, command: CommandSpec | str) -> CommandResult:
        """
        Run a command using fakeroot.

        :param command: Command specification or string.
        :returns: CommandResult of the command.
        """
        if isinstance(command, str):
            command = CommandSpec(command=command, environment=Environment.FAKEROOT)

        command.command = f"fakeroot -i {self.state} -s {self.state} -- {command.command}"

        return self._run_cmd(command)

    def _chroot(self, command: CommandSpec) -> CommandResult:
        """
        Run a command using sudo and chroot.

        :param command: Command specification.
        :returns: CommandResult of the command.
        :raises CommandFailed: Raises an CommandFailed if the chroot folder is not given.
        """

        if not command.chroot:
            raise CommandFailed("Mounting of the special folders requires to provide the chroot!")

        self._special_folders(Path(command.chroot), True)

        assert self._chroot_merged_folder
        command.command = f"chroot {self._chroot_merged_folder} {command.command}"

        try:
            result = self._sudo(command)

        finally:
            self._special_folders(Path(command.chroot), False)

        return result

    def _sudo(self, command: CommandSpec | str) -> CommandResult:
        """
        Run a command using sudo.

        :param command: Command specification.
        :returns: CommandResult of the command.
        """
        if isinstance(command, str):
            command = CommandSpec(command=command, environment=Environment.SUDO)

        command.command = command.command.replace('"', r"\"")

        if self._use_sudo_password:
            # Host and timing / environment specific behavior
            command.command = f'sudo -S bash -c "{command.command}"'  # pragma: no cover
        else:
            # Host and timing / environment specific behavior
            command.command = f'sudo -n bash -c "{command.command}"'  # pragma: no cover

        return self._run_cmd(command)

    def exec(self, command: CommandSpec | str) -> CommandResult:
        """
        Execute the given command.

        :param command: Command to run as CommandSpec or string.
        :returns: Output as CommandResult.
        :raises CommandFailed: If an unknown command environment is provided.
        """
        if isinstance(command, str):
            command = CommandSpec(command=command)

        if command.environment == Environment.SHELL:
            return self._run_cmd(command)
        elif command.environment == Environment.SUDO:
            return self._sudo(command)
        elif command.environment == Environment.CHROOT:
            return self._chroot(command)
        elif command.environment == Environment.FAKEROOT:
            return self._fakeroot(command)
        else:  # pragma: no cover
            # Only happens if a invalid type is provided as environment.
            raise CommandFailed("Environment %s of command %s not implemented!", command.environment, command)
