"""Unit tests for the dotbins module."""

import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from _pytest.capture import CaptureFixture
from _pytest.monkeypatch import MonkeyPatch
from pytest_mock import MockFixture

import dotbins
from dotbins.config import Config, build_tool_config
from dotbins.versions import VersionStore


def test_load_config(temp_dir: Path) -> None:
    """Test loading configuration from YAML."""
    # Create a sample config file - updated to new format
    config_content = """
    tools_dir: ~/tools
    platforms:
      linux:
        - amd64
        - arm64
      macos:
        - arm64
    tools:
        sample-tool:
            repo: sample/tool
            extract_binary: true
            binary_name: sample
            binary_path: bin/sample
            asset_patterns: sample-{version}-{platform}_{arch}.tar.gz
    """

    config_path = temp_dir / "dotbins.yaml"
    with open(config_path, "w") as f:
        f.write(config_content)

    # Load config and validate
    config = Config.load_from_file(str(config_path))

    # Verify config was loaded correctly
    assert config.tools_dir == Path(os.path.expanduser("~/tools"))
    assert "linux" in config.platforms
    assert "macos" in config.platforms
    assert "amd64" in config.platforms["linux"]
    assert "arm64" in config.platforms["linux"]
    assert "arm64" in config.platforms["macos"]
    assert "amd64" not in config.platforms["macos"]  # Important: no amd64 for macOS


def test_load_config_fallback() -> None:
    """Test config loading fallback when file not found."""
    # Mock open to raise FileNotFoundError
    with patch("builtins.open", side_effect=FileNotFoundError):
        config = Config.load_from_file("nonexistent.yaml")

    # Verify default config is returned
    assert config.tools_dir == Path(os.path.expanduser("~/.mydotbins/tools"))


def test_current_platform(monkeypatch: MonkeyPatch) -> None:
    """Test platform detection."""
    # Test Linux/amd64
    monkeypatch.setattr(sys, "platform", "linux")
    monkeypatch.setattr(os, "uname", lambda: MagicMock(machine="x86_64"))
    platform, arch = dotbins.utils.current_platform()
    assert platform == "linux"
    assert arch == "amd64"

    # Test macOS/arm64
    monkeypatch.setattr(sys, "platform", "darwin")
    monkeypatch.setattr(os, "uname", lambda: MagicMock(machine="arm64"))
    platform, arch = dotbins.utils.current_platform()
    assert platform == "macos"
    assert arch == "arm64"


def test_get_latest_release(requests_mock: MockFixture) -> None:
    """Test fetching latest release from GitHub."""
    # Mock GitHub API response
    response_data = {"tag_name": "v1.0.0", "assets": [{"name": "test-1.0.0.tar.gz"}]}
    requests_mock.get(
        "https://api.github.com/repos/test/repo/releases/latest",
        json=response_data,
    )

    # Call the function
    result = dotbins.utils.get_latest_release("test/repo")

    # Verify the result
    assert result["tag_name"] == "v1.0.0"
    assert len(result["assets"]) == 1


def test_find_asset() -> None:
    """Test finding an asset matching a pattern."""
    assets = [
        {"name": "tool-1.0.0-linux_amd64.tar.gz"},
        {"name": "tool-1.0.0-linux_arm64.tar.gz"},
        {"name": "tool-1.0.0-darwin_amd64.tar.gz"},
    ]

    # Test finding Linux amd64 asset
    pattern = "tool-{version}-linux_{arch}.tar.gz"
    asset = dotbins.download._find_asset(assets, pattern)
    assert asset is not None
    assert asset["name"] == "tool-1.0.0-linux_amd64.tar.gz"

    # Test finding macOS asset
    pattern = "tool-{version}-darwin_{arch}.tar.gz"
    asset = dotbins.download._find_asset(assets, pattern)
    assert asset is not None
    assert asset["name"] == "tool-1.0.0-darwin_amd64.tar.gz"

    # Test pattern with no match
    pattern = "tool-{version}-windows_{arch}.zip"
    asset = dotbins.download._find_asset(assets, pattern)
    assert asset is None


def test_download_file(requests_mock: MockFixture, temp_dir: Path) -> None:
    """Test downloading a file from URL."""
    # Setup mock response
    test_content = b"test file content"
    url = "https://example.com/test.tar.gz"
    requests_mock.get(url, content=test_content)

    # Call the function
    dest_path = str(temp_dir / "downloaded.tar.gz")
    result = dotbins.download.download_file(url, dest_path)

    # Verify the file was downloaded correctly
    assert result == dest_path
    with open(dest_path, "rb") as f:
        assert f.read() == test_content


def test_extract_from_archive_tar(temp_dir: Path) -> None:
    """Test extracting binary from tar.gz archive."""
    # Create a test tarball
    import tarfile

    archive_path = str(temp_dir / "test.tar.gz")
    bin_content = b"#!/bin/sh\necho test"

    # Create a tarball with a binary inside
    with tempfile.TemporaryDirectory() as tmpdir:
        bin_path = os.path.join(tmpdir, "test-bin")
        with open(bin_path, "wb") as f:
            f.write(bin_content)
        os.chmod(bin_path, 0o755)  # noqa: S103

        with tarfile.open(archive_path, "w:gz") as tar:
            tar.add(bin_path, arcname="test-bin")

    # Setup tool config
    tool_config = build_tool_config(
        tool_name="test-tool",
        raw_data={
            "binary_name": "test-tool",
            "binary_path": "test-bin",
            "repo": "test/repo",
        },
    )

    # Create destination directory
    dest_dir = temp_dir / "bin"
    dest_dir.mkdir()

    # Call the function
    dotbins.download._extract_from_archive(
        archive_path,
        dest_dir,
        tool_config,
        "linux",
        "1.0.0",
        "amd64",
    )
    # Verify the binary was extracted and renamed
    extracted_bin = dest_dir / "test-tool"
    assert extracted_bin.exists()
    assert extracted_bin.stat().st_mode & 0o100  # Check if executable


def test_extract_from_archive_zip(temp_dir: Path) -> None:
    """Test extracting binary from zip archive."""
    # Create a test zip file
    import zipfile

    archive_path = str(temp_dir / "test.zip")
    bin_content = b"#!/bin/sh\necho test"

    # Create a zip with a binary inside
    with tempfile.TemporaryDirectory() as tmpdir:
        bin_path = os.path.join(tmpdir, "test-bin")
        with open(bin_path, "wb") as f:
            f.write(bin_content)
        os.chmod(bin_path, 0o755)  # noqa: S103

        with zipfile.ZipFile(archive_path, "w") as zip_file:
            zip_file.write(bin_path, arcname="test-bin")

    # Setup tool config
    tool_config = build_tool_config(
        tool_name="test-tool",
        raw_data={
            "binary_name": "test-tool",
            "binary_path": "test-bin",
            "repo": "test/repo",
        },
    )

    # Create destination directory
    dest_dir = temp_dir / "bin"
    dest_dir.mkdir()

    # Call the function
    dotbins.download._extract_from_archive(
        archive_path,
        dest_dir,
        tool_config,
        "linux",
        "1.0.0",
        "amd64",
    )

    # Verify the binary was extracted and renamed
    extracted_bin = dest_dir / "test-tool"
    assert extracted_bin.exists()
    assert extracted_bin.stat().st_mode & 0o100  # Check if executable


def test_make_binaries_executable(temp_dir: Path) -> None:
    """Test making binaries executable."""
    # Setup mock environment
    config = Config(
        tools_dir=temp_dir,
        platforms={"linux": ["amd64"]},  # Use new format
    )

    # Create test binary
    bin_dir = temp_dir / "linux" / "amd64" / "bin"
    bin_dir.mkdir(parents=True)
    bin_file = bin_dir / "test-bin"
    with open(bin_file, "w") as f:
        f.write("#!/bin/sh\necho test")

    # Reset permissions
    bin_file.chmod(0o644)

    # Call the function
    dotbins.download.make_binaries_executable(config)

    # Verify the binary is now executable - use platform-independent check
    mode = bin_file.stat().st_mode
    assert mode & 0o100 != 0, f"File should be executable, mode={mode:o}"


def test_print_shell_setup(capsys: CaptureFixture[str]) -> None:
    """Test printing shell setup instructions."""
    config = Config()
    dotbins.utils.print_shell_setup(config)
    assert config.tools_dir == Path(os.path.expanduser("~/.mydotbins/tools"))
    captured = capsys.readouterr()
    assert "Add this to your shell configuration file" in captured.out
    assert 'export PATH="$HOME/.mydotbins/tools/$_os/$_arch/bin:$PATH"' in captured.out


def test_download_tool_already_exists(temp_dir: Path) -> None:
    """Test prepare_download_task when binary already exists."""
    # Setup environment with complete tool config
    test_tool_config = build_tool_config(
        tool_name="test-tool",
        raw_data={
            "repo": "test/tool",
            "extract_binary": True,
            "binary_name": "test-tool",
            "binary_path": "test-tool",
            "asset_patterns": "test-tool-{version}-{platform}_{arch}.tar.gz",
        },
    )

    version_store = VersionStore(temp_dir)
    version_store.update_tool_info(
        "test-tool",
        "linux",
        "amd64",
        "1.0.0",
        "sha256",
    )

    config = Config(
        tools_dir=temp_dir,
        tools={"test-tool": test_tool_config},
    )

    # Create the binary directory and file
    bin_dir = temp_dir / "linux" / "amd64" / "bin"
    bin_dir.mkdir(parents=True)
    bin_file = bin_dir / "test-tool"
    with open(bin_file, "w") as f:
        f.write("#!/bin/sh\necho test")

    # Mock the get_latest_release function to avoid HTTP requests
    with patch("dotbins.utils.get_latest_release") as mock_release:
        mock_release.return_value = {"tag_name": "v1.0.0", "assets": []}

        # With prepare_download_task, it should return None if file exists
        result = dotbins.download._prepare_download_task(
            "test-tool",
            "linux",
            "amd64",
            config,
            force=False,
        )

    # Should return None (skip download) since file exists
    assert result is None


def test_download_tool_asset_not_found(
    temp_dir: Path,
    requests_mock: MockFixture,
) -> None:
    """Test prepare_download_task when asset is not found."""
    # Mock GitHub API response with no matching Linux assets
    response_data = {
        "tag_name": "v1.0.0",
        "assets": [
            {
                "name": "tool-1.0.0-windows_amd64.zip",
                "browser_download_url": "https://example.com/tool-1.0.0-windows_amd64.zip",
            },
        ],  # No Linux asset
    }
    requests_mock.get(
        "https://api.github.com/repos/test/tool/releases/latest",
        json=response_data,
    )
    test_tool_config = build_tool_config(
        tool_name="test-tool",
        raw_data={
            "repo": "test/tool",
            "binary_name": "test-tool",
            "asset_patterns": "tool-{version}-linux_{arch}.tar.gz",
        },
    )
    # Setup environment
    config = Config(
        tools_dir=temp_dir,
        tools={"test-tool": test_tool_config},
    )

    # Mock find_asset to ensure it returns None for our specific pattern
    with patch("dotbins.download._find_asset") as mock_find_asset:
        mock_find_asset.return_value = None

        # Call the function
        result = dotbins.download._prepare_download_task(
            "test-tool",
            "linux",
            "amd64",
            config,
            force=False,
        )

        # Verify find_asset was called with the correct pattern
        mock_find_asset.assert_called_once()

        # Should return None since asset wasn't found
        assert result is None


def test_extract_from_archive_unknown_type(temp_dir: Path) -> None:
    """Test extract_from_archive with unknown archive type."""
    # Create a dummy file with unknown extension
    archive_path = str(temp_dir / "test.xyz")
    with open(archive_path, "w") as f:
        f.write("dummy content")

    # Setup tool config
    test_tool_config = build_tool_config(
        tool_name="test-tool",
        raw_data={
            "repo": "test/tool",
            "binary_name": "test-tool",
            "binary_path": "test-bin",
        },
    )

    # Create destination directory
    dest_dir = temp_dir / "bin"
    dest_dir.mkdir()

    # Call the function and check for exception
    with pytest.raises(ValueError, match="Unsupported archive format"):
        dotbins.download._extract_from_archive(
            archive_path,
            dest_dir,
            test_tool_config,
            "linux",
            "1.0.0",
            "amd64",
        )


def test_extract_from_archive_missing_binary(temp_dir: Path) -> None:
    """Test extract_from_archive when binary is not in archive."""
    # Create a test tarball without the binary
    import tarfile

    archive_path = str(temp_dir / "test.tar.gz")
    with tarfile.open(archive_path, "w:gz") as tar:
        # Create a dummy file instead of the binary
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(b"dummy content")
            tmp_path = tmp.name
        tar.add(tmp_path, arcname="dummy-file")
        os.unlink(tmp_path)

    # Setup tool config
    test_tool_config = build_tool_config(
        tool_name="test-tool",
        raw_data={
            "repo": "test/tool",
            "binary_name": "test-tool",
            "binary_path": "test-bin",  # This path doesn't exist in archive
        },
    )

    # Create destination directory
    dest_dir = temp_dir / "bin"
    dest_dir.mkdir()

    # Call the function and check for exception
    with pytest.raises(FileNotFoundError):
        dotbins.download._extract_from_archive(
            archive_path,
            dest_dir,
            test_tool_config,
            "linux",
            "1.0.0",
            "amd64",
        )


def test_extract_from_archive_multiple_binaries(temp_dir: Path) -> None:
    """Test extracting multiple binaries from an archive."""
    # Create a test tarball with multiple binaries
    import tarfile

    archive_path = str(temp_dir / "test.tar.gz")
    bin_content = b"#!/bin/sh\necho test"

    # Create a tarball with two binaries inside
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create subdirectory for first binary
        primary_dir = os.path.join(tmpdir, "test-1.0.0")
        os.makedirs(primary_dir)

        # Add two binaries
        bin1_path = os.path.join(primary_dir, "primary-bin")
        bin2_path = os.path.join(primary_dir, "secondary-bin")

        for path in [bin1_path, bin2_path]:
            with open(path, "wb") as f:
                f.write(bin_content)
            os.chmod(path, 0o755)  # noqa: S103

        with tarfile.open(archive_path, "w:gz") as tar:
            tar.add(primary_dir, arcname="test-1.0.0")

    # Setup tool config with multiple binaries
    test_tool_config = build_tool_config(
        tool_name="test-tool",
        raw_data={
            "repo": "test/tool",
            "binary_name": ["primary-tool", "secondary-tool"],
            "binary_path": ["test-1.0.0/primary-bin", "test-1.0.0/secondary-bin"],
        },
    )

    # Create destination directory
    dest_dir = temp_dir / "bin"
    dest_dir.mkdir()

    # Call the function
    dotbins.download._extract_from_archive(
        archive_path,
        dest_dir,
        test_tool_config,
        "linux",
        "1.0.0",
        "amd64",
    )

    # Verify both binaries were extracted and renamed correctly
    for bin_name in ["primary-tool", "secondary-tool"]:
        extracted_bin = dest_dir / bin_name
        assert extracted_bin.exists(), f"Binary {bin_name} not found"
        assert extracted_bin.stat().st_mode & 0o100, f"Binary {bin_name} not executable"

    # Verify the contents of both extracted files
    for bin_name in ["primary-tool", "secondary-tool"]:
        with open(dest_dir / bin_name, "rb") as f:
            content = f.read()
        assert content == bin_content
