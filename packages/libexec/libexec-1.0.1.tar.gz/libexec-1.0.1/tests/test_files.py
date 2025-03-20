"""Tests for the files class."""

import os
import tarfile
import logging
import shutil

from pathlib import Path

import pytest

from libexec.files import (
    Files,
    parse_files,
    parse_scripts,
    FileConfig,
    ScriptConfig,
    _get_random_free_filename,
    FileMetadata,
    ScriptMetadata,
    FilesError,
)
from libexec.exec import Exec, Environment


test_data = Path(__file__).parent / "data"
password_file = Path(Path.home() / ".elische/sudo_password")


class TestFiles:
    """Tests for the files class."""

    def test_parse_files(self) -> None:
        """Test the parse_files function."""
        files_config: list[str | FileConfig] = [
            "test.txt",
            FileConfig(source=Path("relative"), destination=Path("folder/relative")),
            FileConfig(source=Path("/absolute"), destination=Path("other/relative")),
            FileConfig(source=Path("/absolute"), destination=Path("/other/absolute")),
            "/etc/resolv.conf",
        ]
        file_meta = parse_files(files_config)
        assert len(file_meta) == 5

        assert file_meta[0].source == Path("test.txt")
        assert file_meta[0].destination_file == Path("test.txt")
        assert file_meta[0].destination_folder is None

        assert file_meta[1].source == Path("relative")
        assert file_meta[1].destination_file == Path("folder/relative")
        assert file_meta[0].destination_folder is None

        assert file_meta[2].source == Path("/absolute")
        assert file_meta[2].destination_file == Path("other/relative")
        assert file_meta[0].destination_folder is None

        assert file_meta[3].source == Path("/absolute")
        assert file_meta[3].destination_file == Path("/other/absolute")
        assert file_meta[3].destination_folder is None

        assert file_meta[4].source == Path("/etc/resolv.conf")
        assert file_meta[4].destination_file == Path("etc/resolv.conf")
        assert file_meta[4].destination_folder is None

    def test_parse_scripts(self) -> None:
        """Test the parse_scripts function."""
        scripts_config: list[str | ScriptConfig] = [
            "script.sh",
            ScriptConfig(name=Path("script1.sh"), env=None),
            ScriptConfig(name=Path("/script2.sh"), env=Environment.SHELL),
            ScriptConfig(name=Path("script3.sh"), env=Environment.SUDO),
            ScriptConfig(name=Path("script4.sh"), env=Environment.FAKEROOT),
            ScriptConfig(name=Path("script5.sh"), env=Environment.CHROOT),
        ]
        script_meta = parse_scripts(scripts_config)
        assert len(script_meta) == 6

        assert script_meta[0].script == Path("script.sh")
        assert script_meta[0].environment == Environment.SHELL

        assert script_meta[1].script == Path("script1.sh")
        assert script_meta[1].environment == Environment.SHELL

        assert script_meta[2].script == Path("/script2.sh")
        assert script_meta[2].environment == Environment.SHELL

        assert script_meta[3].script == Path("script3.sh")
        assert script_meta[3].environment == Environment.SUDO

        assert script_meta[4].script == Path("script4.sh")
        assert script_meta[4].environment == Environment.FAKEROOT

        assert script_meta[5].script == Path("script5.sh")
        assert script_meta[5].environment == Environment.CHROOT

    def test_get_random_free_filename(self) -> None:
        """Test the _get_random_free_filename function."""
        name = _get_random_free_filename(test_data)
        assert not os.path.isfile(name)

    def test_copy_file(self, tmp_path) -> None:
        """Test copying a file."""
        tmp_path = Path(tmp_path)

        file_meta = FileMetadata(source=test_data / "some_file.txt", destination_file=tmp_path / "some_file.txt")

        files = Files(sysroot=tmp_path, exec=Exec())

        result = files.copy_file(file_meta)
        assert len(result) == 1
        assert os.path.isfile(tmp_path / "some_file.txt")

        with open(tmp_path / "some_file.txt", "r", encoding="utf-8") as f:
            content = f.read()

        assert content == "some content\n"

    def test_copy_file_multi_match(self, tmp_path) -> None:
        """Test copying multiple files by match."""
        tmp_path = Path(tmp_path)

        file_meta = FileMetadata(source=test_data / "*_file.txt", destination_folder=tmp_path)

        files = Files(sysroot=tmp_path)

        result = files.copy_file(file_meta)
        assert len(result) == 2
        assert os.path.isfile(tmp_path / "some_file.txt")
        assert os.path.isfile(tmp_path / "other_file.txt")

        with open(tmp_path / "some_file.txt", "r", encoding="utf-8") as f:
            content = f.read()

        assert content == "some content\n"

        with open(tmp_path / "other_file.txt", "r", encoding="utf-8") as f:
            content = f.read()

        assert content == "other content"

    def test_copy_files(self, tmp_path) -> None:
        """Test copying multiple files by match."""
        tmp_path = Path(tmp_path)

        file_metas = [
            FileMetadata(source=test_data / "*file.txt", destination_folder=tmp_path),
            FileMetadata(source=test_data / "different*", destination_folder=tmp_path),
        ]

        files = Files(sysroot=tmp_path)

        result = files.copy_files(file_metas)
        assert len(result) == 3
        assert os.path.isfile(tmp_path / "some_file.txt")
        assert os.path.isfile(tmp_path / "other_file.txt")
        assert os.path.isfile(tmp_path / "different.txt")

    def test_run_script(self, tmp_path) -> None:
        """Test running a script."""
        tmp_path = Path(tmp_path)

        script_meta = ScriptMetadata(script=test_data / "script.sh", workdir=tmp_path)

        files = Files(sysroot=tmp_path)

        result = files.run_script(script_meta)
        assert len(result) == 1
        assert os.path.isfile(tmp_path / "hello.txt")

        with open(tmp_path / "hello.txt", "r", encoding="utf-8") as f:
            content = f.read()

        assert content == "hello\n"

    def test_run_scripts(self, tmp_path) -> None:
        """Test running multiple scripts."""
        tmp_path = Path(tmp_path)

        script_metas = [
            ScriptMetadata(script=test_data / "script.sh", workdir=tmp_path),
            ScriptMetadata(script=test_data / "other_script.sh", workdir=tmp_path),
        ]

        files = Files(sysroot=tmp_path)

        result = files.run_scripts(script_metas)
        assert len(result) == 2
        assert os.path.isfile(tmp_path / "hello.txt")
        assert os.path.isfile(tmp_path / "other.txt")

    def test_pack_sysroot_as_tarball(self, tmp_path) -> None:
        """Test pack_sysroot_as_tarball function."""
        file_metas = [
            FileMetadata(source=test_data / "*file.txt", destination_folder=tmp_path),
            FileMetadata(source=test_data / "different*", destination_folder=tmp_path),
        ]

        files = Files(sysroot=tmp_path)

        result = files.copy_files(file_metas)
        assert len(result) == 3

        tarball = files.pack_sysroot_as_tarball()

        assert os.path.isfile(tarball)

        with tarfile.open(tarball, "r") as tar:
            members = [str(member.name) for member in tar.getmembers()]
            assert "different.txt" in members
            assert "some_file.txt" in members
            assert "other_file.txt" in members

    def test_extract_tarball_as_sysroot(self, tmp_path) -> None:
        """Test extract_tarball_as_sysroot function."""
        files = Files(sysroot=tmp_path)

        files.extract_tarball_as_sysroot(test_data / "sysroot.tar")

        assert os.path.isfile(tmp_path / "other_file.txt")
        assert os.path.isfile(tmp_path / "some_file.txt")
        assert os.path.isfile(tmp_path / "different.txt")

    def test_extract_tarball_as_sysroot_sudo(self, tmp_path) -> None:
        """Test extract_tarball_as_sysroot function."""
        files = Files(sysroot=tmp_path)

        files.extract_tarball_as_sysroot(test_data / "sysroot.tar", sudo=True)

        assert os.path.isfile(tmp_path / "other_file.txt")
        assert os.path.isfile(tmp_path / "some_file.txt")
        assert os.path.isfile(tmp_path / "different.txt")

    def test_pack_sysroot_as_tarball_xz(self, tmp_path) -> None:
        """Test pack_sysroot_as_tarball function."""
        file_meta = FileMetadata(source=test_data / "*file.txt", destination_folder=tmp_path)

        files = Files(sysroot=tmp_path)

        result = files.copy_file(file_meta)
        assert len(result) == 2

        tarball = files.pack_sysroot_as_tarball(compression="xz")

        assert os.path.isfile(tarball)
        assert str(tarball).endswith(".xz")

        with tarfile.open(tarball, "r") as tar:
            members = [str(member.name) for member in tar.getmembers()]
            assert "some_file.txt" in members
            assert "other_file.txt" in members

    def test_pack_sysroot_as_tarball_sudo_xz(self, tmp_path) -> None:
        """Test pack_sysroot_as_tarball function."""
        file_meta = FileMetadata(source=test_data / "*file.txt", destination_folder=tmp_path)

        files = Files(sysroot=tmp_path, exec=Exec(sudo_password_file=password_file))

        result = files.copy_file(file_meta)
        assert len(result) == 2

        tarball = files.pack_sysroot_as_tarball(compression="xz", environment=Environment.SUDO)

        assert os.path.isfile(tarball)
        assert str(tarball).endswith(".xz")

        with tarfile.open(tarball, "r") as tar:
            members = [str(member.name) for member in tar.getmembers()]
            assert "some_file.txt" in members
            assert "other_file.txt" in members

    def test_pack_sysroot_as_tarball_sudo_gz(self, tmp_path) -> None:
        """Test pack_sysroot_as_tarball function."""
        file_meta = FileMetadata(source=test_data / "*file.txt", destination_folder=tmp_path)

        files = Files(sysroot=tmp_path, exec=Exec(sudo_password_file=password_file))

        result = files.copy_file(file_meta)
        assert len(result) == 2

        tarball = files.pack_sysroot_as_tarball(compression="gz", environment=Environment.FAKEROOT)

        assert os.path.isfile(tarball)
        assert str(tarball).endswith(".gz")

        with tarfile.open(tarball, "r") as tar:
            members = [str(member.name) for member in tar.getmembers()]
            assert "some_file.txt" in members
            assert "other_file.txt" in members

    def test_pack_sysroot_as_tarball_fakeroot_bz2(self, tmp_path) -> None:
        """Test pack_sysroot_as_tarball function."""
        file_meta = FileMetadata(source=test_data / "*file.txt", destination_folder=tmp_path)

        files = Files(sysroot=tmp_path, exec=Exec(sudo_password_file=password_file))

        result = files.copy_file(file_meta)
        assert len(result) == 2

        tarball = files.pack_sysroot_as_tarball(compression="bz2", environment=Environment.FAKEROOT)

        assert os.path.isfile(tarball)
        assert str(tarball).endswith(".bz2")

        with tarfile.open(tarball, "r") as tar:
            members = [str(member.name) for member in tar.getmembers()]
            assert "some_file.txt" in members
            assert "other_file.txt" in members

    def test_pack_sysroot_as_tarball_sudo_unknown_compression(self, tmp_path, caplog) -> None:
        """Test pack_sysroot_as_tarball function."""
        file_meta = FileMetadata(source=test_data / "*file.txt", destination_folder=tmp_path)

        files = Files(sysroot=tmp_path, exec=Exec(sudo_password_file=password_file))

        result = files.copy_file(file_meta)
        assert len(result) == 2

        with caplog.at_level(logging.ERROR):
            tarball = files.pack_sysroot_as_tarball(compression="zst", environment=Environment.SUDO)
            assert "Unknown compression: zst" in caplog.text

        assert os.path.isfile(tarball)
        assert str(tarball).endswith(".tar")

        with tarfile.open(tarball, "r") as tar:
            members = [str(member.name) for member in tar.getmembers()]
            assert "some_file.txt" in members
            assert "other_file.txt" in members

    def test_pack_sysroot_as_tarball_sudo(self, tmp_path) -> None:
        """Test pack_sysroot_as_tarball function."""
        file_meta = FileMetadata(source=test_data / "*file.txt", destination_folder=tmp_path)

        files = Files(sysroot=tmp_path, exec=Exec(sudo_password_file=password_file))

        result = files.copy_file(file_meta)
        assert len(result) == 2

        tarball = files.pack_sysroot_as_tarball(environment=Environment.SUDO)

        assert os.path.isfile(tarball)
        assert str(tarball).endswith(".tar")

        with tarfile.open(tarball, "r") as tar:
            members = [str(member.name) for member in tar.getmembers()]
            assert "some_file.txt" in members
            assert "other_file.txt" in members

    def test_pack_sysroot_as_tarball_chroot(self, tmp_path) -> None:
        """Test pack_sysroot_as_tarball function."""
        file_meta = FileMetadata(source=test_data / "*file.txt", destination_folder=tmp_path)

        files = Files(sysroot=tmp_path, exec=Exec(sudo_password_file=password_file))

        result = files.copy_file(file_meta)
        assert len(result) == 2

        with pytest.raises(FilesError):
            files.pack_sysroot_as_tarball(environment=Environment.CHROOT)

    def test_pack_sysroot_as_tarball_sudo_xz_file(self, tmp_path) -> None:
        """Test pack_sysroot_as_tarball function."""
        file_meta = FileMetadata(source=test_data / "*file.txt", destination_folder=tmp_path)

        files = Files(sysroot=tmp_path, exec=Exec(sudo_password_file=password_file))

        result = files.copy_file(file_meta)
        assert len(result) == 2

        tarball = tmp_path / "sysroot.tar"

        result_tarball = files.pack_sysroot_as_tarball(compression="xz", environment=Environment.SUDO, tarball=tarball)

        assert result_tarball == tarball
        assert os.path.isfile(tarball)
        assert str(tarball).endswith(".tar")

        with tarfile.open(tarball, "r") as tar:
            members = [str(member.name) for member in tar.getmembers()]
            assert "some_file.txt" in members
            assert "other_file.txt" in members

    def test_pack_sysroot_as_tarball_sudo_gz_file(self, tmp_path) -> None:
        """Test pack_sysroot_as_tarball function."""
        file_meta = FileMetadata(source=test_data / "*file.txt", destination_folder=tmp_path)

        files = Files(sysroot=tmp_path, exec=Exec(sudo_password_file=password_file))

        result = files.copy_file(file_meta)
        assert len(result) == 2

        tarball = tmp_path / "sysroot.tar"

        result_tarball = files.pack_sysroot_as_tarball(compression="gz", environment=Environment.SUDO, tarball=tarball)

        assert result_tarball == tarball
        assert os.path.isfile(tarball)
        assert str(tarball).endswith(".tar")

        with tarfile.open(tarball, "r") as tar:
            members = [str(member.name) for member in tar.getmembers()]
            assert "some_file.txt" in members
            assert "other_file.txt" in members

    def test_pack_sysroot_as_tarball_sudo_bz2_file(self, tmp_path) -> None:
        """Test pack_sysroot_as_tarball function."""
        file_meta = FileMetadata(source=test_data / "*file.txt", destination_folder=tmp_path)

        files = Files(sysroot=tmp_path, exec=Exec(sudo_password_file=password_file))

        result = files.copy_file(file_meta)
        assert len(result) == 2

        tarball = tmp_path / "sysroot.tar"

        result_tarball = files.pack_sysroot_as_tarball(compression="bz2", environment=Environment.SUDO, tarball=tarball)

        assert result_tarball == tarball
        assert os.path.isfile(tarball)
        assert str(tarball).endswith(".tar")

        with tarfile.open(tarball, "r") as tar:
            members = [str(member.name) for member in tar.getmembers()]
            assert "some_file.txt" in members
            assert "other_file.txt" in members

    def test_copy_file_chroot(self, tmp_path) -> None:
        """Test copy a file in the chroot environment."""
        tmp_path = Path(tmp_path)

        origin_chroot = test_data / "chroot"
        shutil.copytree(origin_chroot, tmp_path, dirs_exist_ok=True)

        file_meta = FileMetadata(
            source=Path("some_file.txt"), destination_file=Path("copy.txt"), environment=Environment.CHROOT
        )

        files = Files(sysroot=tmp_path, exec=Exec(sudo_password_file=password_file))

        files.copy_file(file_meta)

        assert os.path.isfile(tmp_path / "copy.txt")

    def test_copy_file_not_unique(self, tmp_path) -> None:
        """Test copy a not unique file shall raise a FilesError."""
        tmp_path = Path(tmp_path)

        file_meta = FileMetadata(source=test_data / "*.txt", destination_file=tmp_path / "copy.txt")

        files = Files(sysroot=tmp_path, exec=Exec(sudo_password_file=password_file))

        with pytest.raises(FilesError):
            files.copy_file(file_meta)

    def test_copy_file_chroot_from_ext(self, tmp_path) -> None:
        """Test copy a file in the chroot environment."""
        tmp_path = Path(tmp_path)

        origin_chroot = test_data / "chroot"
        shutil.copytree(origin_chroot, tmp_path, dirs_exist_ok=True)

        file_meta = FileMetadata(
            source=(test_data / "other_file.txt").absolute(),
            destination_file=Path("copy.txt"),
            environment=Environment.CHROOT,
            chroot=tmp_path,
        )

        files = Files(sysroot=tmp_path, exec=Exec(sudo_password_file=password_file))

        files.copy_file(file_meta)

        assert os.path.isfile(tmp_path / "copy.txt")

    def test_copy_file_delete_dst(self, tmp_path) -> None:
        """Test copying a file and delete destination before."""
        tmp_path = Path(tmp_path)

        file_metas = [
            FileMetadata(source=test_data / "some_file.txt", destination_file=tmp_path / "some_file.txt"),
            FileMetadata(
                source=test_data / "some_file.txt", destination_file=tmp_path / "some_file.txt", delete_if_exists=True
            ),
        ]

        files = Files(sysroot=tmp_path, exec=Exec())

        result = files.copy_files(file_metas)
        assert len(result) == 2
        assert os.path.isfile(tmp_path / "some_file.txt")

    def test_copy_file_delete_dst_sudo(self, tmp_path) -> None:
        """Test copying a file and delete destination before."""
        tmp_path = Path(tmp_path)

        file_meta = FileMetadata(source=test_data / "some_file.txt", destination_file=tmp_path / "some_file.txt")

        files = Files(sysroot=tmp_path, exec=Exec())

        result = files.copy_file(file_meta)
        assert len(result) == 1
        assert os.path.isfile(tmp_path / "some_file.txt")

        file_meta = FileMetadata(
            source=test_data / "some_file.txt",
            destination_file=tmp_path / "some_file.txt",
            delete_if_exists=True,
            environment=Environment.SUDO,
        )
        result = files.copy_file(file_meta)
        assert len(result) == 1
        assert os.path.isfile(tmp_path / "some_file.txt")

        file_meta = FileMetadata(
            source=test_data / "some_file.txt",
            destination_file=tmp_path / "some_file.txt",
            delete_if_exists=True,
            environment=Environment.SHELL,
        )
        result = files.copy_file(file_meta)
        assert len(result) == 1
        assert os.path.isfile(tmp_path / "some_file.txt")

    def test_copy_file_chroot_invalid_dst(self, tmp_path) -> None:
        """Test copying a file in chroot with dst outside chroot."""
        tmp_path = Path(tmp_path)

        origin_chroot = test_data / "chroot"
        shutil.copytree(origin_chroot, tmp_path, dirs_exist_ok=True)

        file_meta = FileMetadata(
            source=Path("some_file.txt"), destination_file=Path("/tmp/copy.txt"), environment=Environment.CHROOT
        )

        files = Files(sysroot=tmp_path, exec=Exec(sudo_password_file=password_file))

        with pytest.raises(FilesError):
            files.copy_file(file_meta)

    def test_copy_file_uid_gid(self, tmp_path) -> None:
        """Test copying a file and set uid and gid."""
        tmp_path = Path(tmp_path)

        file_meta = FileMetadata(
            source=test_data / "some_file.txt", destination_file=tmp_path / "some_file.txt", user_id=0, group_id=0
        )

        files = Files(sysroot=tmp_path, exec=Exec())

        result = files.copy_file(file_meta)
        assert len(result) == 1
        assert os.path.isfile(tmp_path / "some_file.txt")

        stat = os.stat(tmp_path / "some_file.txt")
        assert stat.st_uid == 0
        assert stat.st_gid == 0

    def test_copy_file_exec(self, tmp_path) -> None:
        """Test copying a file and set exec bit."""
        tmp_path = Path(tmp_path)

        file_meta = FileMetadata(
            source=test_data / "some_file.txt", destination_file=tmp_path / "some_file.txt", executable=True
        )

        files = Files(sysroot=tmp_path, exec=Exec())

        result = files.copy_file(file_meta)
        assert len(result) == 1
        assert os.path.isfile(tmp_path / "some_file.txt")

        assert os.access(tmp_path / "some_file.txt", os.X_OK)

    def test_copy_file_no_exec(self, tmp_path) -> None:
        """Test copying a file and not set exec bit."""
        tmp_path = Path(tmp_path)

        file_meta = FileMetadata(
            source=test_data / "some_file.txt", destination_file=tmp_path / "some_file.txt", executable=False
        )

        files = Files(sysroot=tmp_path, exec=Exec())

        result = files.copy_file(file_meta)
        assert len(result) == 1
        assert os.path.isfile(tmp_path / "some_file.txt")

        assert not os.access(tmp_path / "some_file.txt", os.X_OK)

    def test_run_script_from_chroot(self, tmp_path) -> None:
        """Test running a script contained in the sysroot folder."""
        tmp_path = Path(tmp_path)

        origin_chroot = test_data / "chroot"
        shutil.copytree(origin_chroot, tmp_path, dirs_exist_ok=True)

        files = Files(sysroot=tmp_path, exec=Exec(sudo_password_file=password_file))

        file_meta = FileMetadata(
            source=test_data / "chroot_script.sh", destination_file=tmp_path / "script.sh", executable=False
        )
        files.copy_file(file_meta)

        script_meta = ScriptMetadata(script=Path("script.sh"), workdir=tmp_path, environment=Environment.CHROOT)

        result = files.run_script(script_meta)
        assert len(result) == 1
        assert os.path.isfile(tmp_path / "hello.txt")

        with open(tmp_path / "hello.txt", "r", encoding="utf-8") as f:
            content = f.read()

        assert content == "chroot\n"

    def test_run_script_too_many_matches(self, tmp_path) -> None:
        """Test a FilesError is raised if the script is not unique."""
        tmp_path = Path(tmp_path)

        script_meta = ScriptMetadata(script=test_data / "*.sh", target=tmp_path / "script.sh")

        files = Files(sysroot=tmp_path, exec=Exec(sudo_password_file=password_file))

        with pytest.raises(FilesError):
            files.run_script(script_meta)

    def test_run_script_target(self, tmp_path) -> None:
        """Test running a script."""
        tmp_path = Path(tmp_path)

        script_meta = ScriptMetadata(script=test_data / "script.sh", workdir=tmp_path, target=tmp_path / "script.sh")

        files = Files(sysroot=tmp_path)

        result = files.run_script(script_meta)
        assert len(result) == 1
        assert os.path.isfile(tmp_path / "hello.txt")

        with open(tmp_path / "hello.txt", "r", encoding="utf-8") as f:
            content = f.read()

        assert content == "hello\n"

    def test_run_out_script_in_chroot(self, tmp_path) -> None:
        """Test running a script from the host in the chroot."""
        tmp_path = Path(tmp_path)

        origin_chroot = test_data / "chroot"
        shutil.copytree(origin_chroot, tmp_path, dirs_exist_ok=True)

        files = Files(sysroot=tmp_path, exec=Exec(sudo_password_file=password_file))

        script_meta = ScriptMetadata(script=test_data / "chroot_script.sh", environment=Environment.CHROOT)

        result = files.run_script(script_meta)
        assert len(result) == 1
        assert os.path.isfile(tmp_path / "hello.txt")

        with open(tmp_path / "hello.txt", "r", encoding="utf-8") as f:
            content = f.read()

        assert content == "chroot\n"
