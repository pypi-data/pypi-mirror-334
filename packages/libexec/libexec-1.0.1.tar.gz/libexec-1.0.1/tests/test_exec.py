"""Tests for the exec class."""

import shutil

from pathlib import Path

import pytest

from libexec.exec import Exec, CommandSpec, Environment, CommandFailed, CommandResult


test_data = Path(__file__).parent / "data"
password_file = Path(Path.home() / ".elische/sudo_password")


class TestExec:
    """Tests for the exec class."""

    def test_exec_shell(self) -> None:
        """Test executing something on the default shell."""
        exec = Exec()
        result = exec.exec(CommandSpec(command="ls -lah .", workdir=Path("/"), environment=Environment.SHELL))
        assert result.exit_code == 0
        assert result.stdout is None
        assert result.stderr is None

    def test_exec_str(self) -> None:
        """Test executing something on the default shell."""
        exec = Exec()
        result = exec.exec("ls -lah .")
        assert result.exit_code == 0
        assert result.stdout is None
        assert result.stderr is None

    def test_exec_shell_capture_output(self) -> None:
        """Test executing something on the default shell and capturing the output."""
        exec = Exec()
        result = exec.exec(
            CommandSpec(command="ls -lah .", workdir=Path("/"), environment=Environment.SHELL, capture_output=True)
        )
        assert result.exit_code == 0
        assert result.stdout is not None
        assert "etc" in result.stdout
        assert result.stderr == ""

    def test_exec_shell_write_output(self, tmp_path) -> None:
        """Test executing something on the default shell and write the output."""
        exec = Exec()

        out_file = tmp_path / "stdout"
        result = None

        with open(out_file, "wb") as f:
            result = exec.exec(
                CommandSpec(command="ls -lah .", workdir=Path("/"), environment=Environment.SHELL, stdout=f)
            )

        assert result
        assert result.exit_code == 0
        assert result.stdout is None
        assert result.stderr is None

        with open(out_file, "r", encoding="utf-8") as f:
            content = f.read()
            assert "etc" in content

    def test_failing_command(self) -> None:
        """Test for a failing command."""
        exec = Exec()
        with pytest.raises(CommandFailed):
            exec.exec(
                CommandSpec(
                    command="ls -lah /not-existing-dir",
                    workdir=Path("/"),
                    environment=Environment.SHELL,
                    capture_output=True,
                )
            )

    def test_exec_sudo_password_file(self) -> None:
        """Test executing something as sudo."""
        exec = Exec(sudo_password_file=password_file)
        result = exec.exec(
            CommandSpec(command="ls -lah .", workdir=Path("/"), environment=Environment.SUDO, capture_output=True)
        )
        assert result.exit_code == 0
        assert result.stdout is not None
        assert result.stderr is not None

    def test_exec_sudo_str(self) -> None:
        """Test executing something as sudo."""
        exec = Exec(sudo_password_file=password_file)
        result = exec._sudo("ls -lah .")
        assert result.exit_code == 0
        assert result.stdout is None
        assert result.stderr is None

    @pytest.mark.skipif(not password_file.is_file(), reason="Requires password_file to exist.")
    def test_exec_sudo_password_interactive(self) -> None:
        """Test executing something as sudo."""
        exec = Exec()

        # Fill the sudo password field
        with open(password_file, "r", encoding="utf-8") as f:
            exec._sudo_password = f.read().replace("\n", "")

        result = exec.exec(
            CommandSpec(command="ls -lah .", workdir=Path("/"), environment=Environment.SUDO, capture_output=True)
        )
        assert result.exit_code == 0
        assert result.stdout is not None
        assert result.stderr is not None

    def test_exec_fakeroot(self) -> None:
        """Test executing something using fakeroot."""
        exec = Exec()
        result = exec.exec(
            CommandSpec(command="id", workdir=Path("/"), environment=Environment.FAKEROOT, capture_output=True)
        )
        assert result.exit_code == 0
        assert result.stdout is not None
        assert "uid=0(root) gid=0(root)" in result.stdout
        assert result.stderr == ""

    def test_exec_fakeroot_str(self) -> None:
        """Test executing something using fakeroot."""
        exec = Exec()
        result = exec._fakeroot("id")
        assert result.exit_code == 0
        assert result.stdout is None
        assert result.stderr is None

    def test_exec_chroot(self) -> None:
        """Test executing something using chroot."""
        chroot = test_data / "chroot"

        exec = Exec(sudo_password_file=password_file)
        result = exec.exec(
            CommandSpec(command='/bin/sh -c "id"', chroot=chroot, environment=Environment.CHROOT, capture_output=True)
        )
        assert result.exit_code == 0
        assert result.stdout is not None
        assert "uid=0 gid=0" in result.stdout
        assert result.stderr == ""

    def test_command_spec_repr(self) -> None:
        """Test CommandSpec representation."""
        cmd = CommandSpec(command="echo 'hello'", environment=Environment.SHELL)
        assert str(cmd) == "CommandSpec<command=echo 'hello', env=Environment.SHELL>"

    def test_command_result_repr(self) -> None:
        """Test CommandResult representation."""
        cmd = CommandSpec(command="echo 'hello'", environment=Environment.SHELL)
        result = CommandResult(command=cmd, exit_code=0)
        assert (
            str(result)
            == "CommandResult<command=CommandSpec<command=echo 'hello', env=Environment.SHELL>, exit_code=0>"
        )

    def test_exec_chroot_no_chroot(self) -> None:
        """Test executing something using chroot without providing a chroot."""
        exec = Exec(sudo_password_file=password_file)
        with pytest.raises(CommandFailed):
            exec.exec(
                CommandSpec(command='/bin/sh -c "id"', chroot=None, environment=Environment.CHROOT, capture_output=True)
            )

    def test_exec_chroot_change_content(self, tmp_path) -> None:
        """Test changing the chroot."""
        origin_chroot = test_data / "chroot"

        shutil.copytree(origin_chroot, tmp_path, dirs_exist_ok=True)

        exec = Exec(sudo_password_file=password_file)
        result = exec.exec(
            CommandSpec(
                command='/bin/sh -c "busybox mkdir -p /my/folder"',
                chroot=tmp_path,
                environment=Environment.CHROOT,
                capture_output=True,
            )
        )
        assert result.exit_code == 0

        my_folder = Path(tmp_path) / "my/folder"
        assert my_folder.is_dir()

        result = exec.exec(
            CommandSpec(
                command='/bin/sh -c "busybox date > /now"',
                chroot=tmp_path,
                environment=Environment.CHROOT,
                capture_output=True,
            )
        )
        assert result.exit_code == 0

        date_file = Path(tmp_path) / "now"
        assert date_file.is_file()

    def test_exec_chroot_resolv(self, tmp_path) -> None:
        """Test resolv.conf and modifying it."""
        origin_chroot = test_data / "chroot"

        shutil.copytree(origin_chroot, tmp_path, dirs_exist_ok=True)

        exec = Exec(sudo_password_file=password_file)
        result = exec.exec(
            CommandSpec(
                command='/bin/sh -c "busybox cat /etc/resolv.conf"',
                chroot=tmp_path,
                environment=Environment.CHROOT,
                capture_output=True,
            )
        )
        assert result.exit_code == 0

        with open("/etc/resolv.conf", "r", encoding="utf-8") as f:
            resolv_content = f.read()

        assert resolv_content == result.stdout

        result = exec.exec(
            CommandSpec(
                command='/bin/sh -c "busybox id > /etc/resolv.conf"',
                chroot=tmp_path,
                environment=Environment.CHROOT,
                capture_output=True,
            )
        )
        assert result.exit_code == 0

        resolv = tmp_path / "etc/resolv.conf"

        with open(resolv, "r", encoding="utf-8") as f:
            modified_resolv_content = f.read()

        assert "uid=0 gid=0" in modified_resolv_content
