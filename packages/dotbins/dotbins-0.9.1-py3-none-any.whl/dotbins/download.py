"""Download and extraction functions for dotbins."""

from __future__ import annotations

import os
import re
import shutil
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import TYPE_CHECKING, NamedTuple

import requests

from .utils import calculate_sha256, extract_archive, get_latest_release, log

if TYPE_CHECKING:
    from .config import Config, ToolConfig
    from .versions import VersionStore


def _find_asset(assets: list[dict], pattern: str) -> dict | None:
    """Find an asset that matches the given pattern."""
    regex_pattern = (
        pattern.replace("{version}", ".*").replace("{arch}", ".*").replace("{platform}", ".*")
    )
    log(f"Looking for asset with pattern: {regex_pattern}", "info", "🔍")

    for asset in assets:
        if re.search(regex_pattern, asset["name"]):
            log(f"Found matching asset: {asset['name']}", "success")
            return asset

    return None


def download_file(url: str, destination: str) -> str:
    """Download a file from a URL to a destination path."""
    log(f"Downloading from {url}", "info", "📥")
    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        with open(destination, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return destination
    except requests.RequestException as e:
        log(f"Download failed: {e}", "error", print_exception=True)
        msg = f"Failed to download {url}: {e}"
        raise RuntimeError(msg) from e


def _extract_from_archive(
    archive_path: str,
    destination_dir: Path,
    tool_config: ToolConfig,
    platform: str,
    version: str,
    arch: str,
) -> None:
    """Extract binaries from an archive."""
    log(f"Extracting from {archive_path} for {platform}", "info", "📦")
    temp_dir = Path(tempfile.mkdtemp())

    try:
        extract_archive(str(archive_path), str(temp_dir))
        log(f"Archive extracted to {temp_dir}", "success", "📦")
        _log_extracted_files(temp_dir)
        binary_paths = tool_config.binary_path or _detect_binary_paths(
            temp_dir,
            tool_config.binary_name,
        )
        destination_dir.mkdir(parents=True, exist_ok=True)
        _process_binaries(
            temp_dir,
            destination_dir,
            tool_config.binary_name,
            binary_paths,
            version,
            tool_config.tool_arch(arch),
        )

    except Exception as e:
        log(f"Error extracting archive: {e}", "error", print_exception=True)
        raise
    finally:
        shutil.rmtree(temp_dir)


def _detect_binary_paths(temp_dir: Path, binary_names: list[str]) -> list[str]:
    """Auto-detect binary paths if not specified in configuration."""
    log("Binary path not specified, attempting auto-detection...", "info", "🔍")
    binary_paths = _auto_detect_binary_paths(temp_dir, binary_names)
    if not binary_paths:
        msg = f"Could not auto-detect binary paths for {', '.join(binary_names)}. Please specify binary_path in config."
        raise ValueError(msg)
    log(f"Auto-detected binary paths: {binary_paths}", "success")
    return binary_paths


def _process_binaries(
    temp_dir: Path,
    destination_dir: Path,
    binary_names: list[str],
    binary_paths: list[str],
    version: str,
    tool_arch: str,
) -> None:
    """Process each binary by finding it and copying to destination."""
    for binary_path_pattern, binary_name in zip(binary_paths, binary_names):
        source_path = _find_binary_in_extracted_files(
            temp_dir,
            binary_path_pattern,
            version,
            tool_arch,
        )
        _copy_binary_to_destination(source_path, destination_dir, binary_name)


def _auto_detect_binary_paths(temp_dir: Path, binary_names: list[str]) -> list[str]:
    """Automatically detect binary paths in an extracted archive.

    Args:
        temp_dir: Directory containing extracted archive
        binary_names: Names of binaries to look for

    Returns:
        List of detected binary paths or empty list if detection fails

    """
    detected_paths = []

    for binary_name in binary_names:
        # Look for exact match first
        exact_matches = list(temp_dir.glob(f"**/{binary_name}"))
        if len(exact_matches) == 1:
            detected_paths.append(str(exact_matches[0].relative_to(temp_dir)))
            continue

        # Look for files containing the name
        partial_matches = list(temp_dir.glob(f"**/*{binary_name}*"))
        executable_matches = [p for p in partial_matches if os.access(p, os.X_OK)]

        if len(executable_matches) == 1:
            detected_paths.append(str(executable_matches[0].relative_to(temp_dir)))
        elif len(executable_matches) > 1:
            # If we have multiple matches, try to find the most likely one
            # (e.g., in a bin/ directory or with exact name match)
            bin_matches = [p for p in executable_matches if "bin/" in str(p)]
            if len(bin_matches) == 1:
                detected_paths.append(str(bin_matches[0].relative_to(temp_dir)))
            else:
                # Give up - we need the user to specify
                return []
        else:
            # No matches found
            return []

    return detected_paths


def _log_extracted_files(temp_dir: Path) -> None:
    """Log the extracted files for debugging."""
    try:
        log("Extracted files:", "info", "ℹ️")  # noqa: RUF001
        for item in temp_dir.glob("**/*"):
            log(f"  - {item.relative_to(temp_dir)}", "info", "")
    except Exception:
        log("Could not list extracted files: {e}")


def _find_binary_in_extracted_files(
    temp_dir: Path,
    binary_path: str,
    version: str,
    tool_arch: str,
) -> Path:
    """Find a specific binary in the extracted files."""
    # Replace variables in the binary path
    binary_path = _replace_variables_in_path(binary_path, version, tool_arch)

    # Handle glob patterns in binary path
    if "*" in binary_path:
        matches = list(temp_dir.glob(binary_path))
        if not matches:
            msg = f"No files matching {binary_path} in archive"
            raise FileNotFoundError(msg)
        return matches[0]

    # Direct path
    source_path = temp_dir / binary_path
    if not source_path.exists():
        msg = f"Binary not found at {source_path}"
        raise FileNotFoundError(msg)

    return source_path


def _copy_binary_to_destination(
    source_path: Path,
    destination_dir: Path,
    binary_name: str,
) -> None:
    """Copy the binary to its destination and set permissions."""
    dest_path = destination_dir / binary_name

    # Copy the binary and set permissions
    shutil.copy2(source_path, dest_path)
    dest_path.chmod(dest_path.stat().st_mode | 0o755)
    log(f"Copied binary to {dest_path}", "success")


def _replace_variables_in_path(path: str, version: str, arch: str) -> str:
    """Replace variables in a path with their values."""
    if "{version}" in path and version:
        path = path.replace("{version}", version)

    if "{arch}" in path and arch:
        path = path.replace("{arch}", arch)

    return path


def _get_release_info(tool_config: ToolConfig) -> tuple[dict, str]:
    """Get release information for a tool."""
    repo = tool_config.repo
    release = get_latest_release(repo)
    version = release["tag_name"].lstrip("v")
    return release, version


def _find_matching_asset(
    tool_config: ToolConfig,
    release: dict,
    version: str,
    platform: str,
    arch: str,
) -> dict | None:
    """Find a matching asset for the tool."""
    asset_pattern = tool_config.asset_patterns[platform][arch]
    if asset_pattern is None:
        log(f"No asset pattern found for {platform}/{arch}", "warning")
        return None
    search_pattern = asset_pattern.format(
        version=version,
        platform=tool_config.tool_platform(platform),
        arch=tool_config.tool_arch(arch),
    )
    asset = _find_asset(release["assets"], search_pattern)
    if not asset:
        log(f"No asset matching '{search_pattern}' found", "warning")
        return None

    return asset


def make_binaries_executable(config: Config) -> None:
    """Make all binaries executable."""
    for platform, architectures in config.platforms.items():
        for arch in architectures:
            bin_dir = config.bin_dir(platform, arch)
            if bin_dir.exists():
                for binary in bin_dir.iterdir():
                    if binary.is_file():
                        binary.chmod(binary.stat().st_mode | 0o755)


class _DownloadTask(NamedTuple):
    """Represents a single download task."""

    tool_config: ToolConfig
    platform: str
    arch: str
    version: str
    asset_url: str
    asset_name: str
    destination_dir: Path
    temp_path: Path

    @property
    def tool_name(self) -> str:
        return self.tool_config.tool_name


def _download_task(task: _DownloadTask) -> tuple[_DownloadTask, bool]:
    """Download a file for a DownloadTask."""
    try:
        log(
            f"Downloading {task.asset_name} for {task.tool_name} ({task.platform}/{task.arch})...",
            "info",
            "📥",
        )
        download_file(task.asset_url, str(task.temp_path))
        return task, True
    except Exception as e:
        log(f"Error downloading {task.asset_name}: {e!s}", "error", print_exception=True)
        return task, False


def _exists_in_destination_dir(destination_dir: Path, tool_config: ToolConfig) -> bool:
    return all((destination_dir / binary_name).exists() for binary_name in tool_config.binary_name)


def _should_download(
    tool_name: str,
    config: Config,
    platform: str,
    arch: str,
    version: str,
    force: bool,
) -> bool:
    """Check if download should be skipped (binary already exists)."""
    tool_info = config.version_store.get_tool_info(tool_name, platform, arch)
    tool_config = config.tools[tool_name]
    destination_dir = config.bin_dir(platform, arch)
    all_exist = _exists_in_destination_dir(destination_dir, tool_config)
    if tool_info and tool_info["version"] == version and all_exist and not force:
        log(
            f"{tool_config.tool_name} {version} for {platform}/{arch} is already"
            f" up to date (installed on {tool_info['updated_at']}) use --force to re-download.",
            "success",
        )
        return False
    return True


def _prepare_download_task(
    tool_name: str,
    platform: str,
    arch: str,
    config: Config,
    force: bool,
) -> _DownloadTask | None:
    """Prepare a download task, checking if update is needed based on version."""
    tool_config = config.tools[tool_name]
    release, version = _get_release_info(tool_config)
    if not _should_download(tool_name, config, platform, arch, version, force):
        return None

    try:
        asset = _find_matching_asset(tool_config, release, version, platform, arch)
        if not asset:
            return None
        tmp_dir = Path(tempfile.gettempdir())
        temp_path = tmp_dir / asset["browser_download_url"].split("/")[-1]
        return _DownloadTask(
            tool_config=tool_config,
            platform=platform,
            arch=arch,
            version=version,
            asset_url=asset["browser_download_url"],
            asset_name=asset["name"],
            destination_dir=config.bin_dir(platform, arch),
            temp_path=temp_path,
        )

    except Exception as e:
        log(
            f"Error processing {tool_name} for {platform}/{arch}: {e!s}",
            "error",
            print_exception=True,
        )
        return None


def _process_downloaded_task(
    task: _DownloadTask,
    success: bool,
    version_store: VersionStore,
) -> bool:
    """Process a downloaded file."""
    if not success:
        return False

    try:
        # Calculate SHA256 hash before extraction
        sha256_hash = calculate_sha256(task.temp_path)
        log(f"SHA256: {sha256_hash}", "info", "🔐")

        task.destination_dir.mkdir(parents=True, exist_ok=True)
        if task.tool_config.extract_binary:
            _extract_from_archive(
                str(task.temp_path),
                task.destination_dir,
                task.tool_config,
                task.platform,
                task.version,
                task.arch,
            )
        else:
            binary_names = task.tool_config.binary_name
            if len(binary_names) != 1:
                log(
                    f"Expected exactly one binary name for {task.tool_name}, got {len(binary_names)}",
                    "error",
                )
                return False
            binary_name = binary_names[0]

            shutil.copy2(task.temp_path, task.destination_dir / binary_name)
            dest_file = task.destination_dir / binary_name
            dest_file.chmod(dest_file.stat().st_mode | 0o755)

        version_store.update_tool_info(
            task.tool_name,
            task.platform,
            task.arch,
            task.version,
            sha256=sha256_hash,
        )

        log(
            f"Successfully processed {task.tool_name} v{task.version} for {task.platform}/{task.arch}",
            "success",
        )
        return True
    except Exception as e:
        log(f"Error processing {task.tool_name}: {e!s}", "error", print_exception=True)
        return False
    finally:
        if task.temp_path.exists():
            task.temp_path.unlink()


def process_downloaded_files(
    downloaded_tasks: list[tuple[_DownloadTask, bool]],
    version_store: VersionStore,
) -> int:
    """Process downloaded files and return success count."""
    log(f"\nProcessing {len(downloaded_tasks)} downloaded tools...", "info", "🔄")
    success_count = 0

    for task, download_success in downloaded_tasks:
        if _process_downloaded_task(task, download_success, version_store):
            success_count += 1

    return success_count


def download_files_in_parallel(
    download_tasks: list[_DownloadTask],
) -> list[tuple[_DownloadTask, bool]]:
    """Download files in parallel using ThreadPoolExecutor."""
    log(f"\nDownloading {len(download_tasks)} tools in parallel...", "info", "🔄")
    downloaded_tasks = []
    with ThreadPoolExecutor(max_workers=min(8, len(download_tasks) or 1)) as ex:
        future_to_task = {ex.submit(_download_task, task): task for task in download_tasks}
        for future in as_completed(future_to_task):
            task, success = future.result()
            downloaded_tasks.append((task, success))

    return downloaded_tasks


def prepare_download_tasks(
    tools_to_update: list[str],
    platforms_to_update: list[str],
    architecture: str | None,
    config: Config,
    force: bool = False,
) -> tuple[list[_DownloadTask], int]:
    """Prepare download tasks for all tools and platforms."""
    download_tasks = []
    total_count = 0

    for tool_name in tools_to_update:
        for platform in platforms_to_update:
            if platform not in config.platforms:
                log(f"Skipping unknown platform: {platform}", "warning")
                continue

            archs_to_update = _determine_architectures(platform, architecture, config)
            if not archs_to_update:
                continue

            for arch in archs_to_update:
                total_count += 1
                task = _prepare_download_task(tool_name, platform, arch, config, force)
                if task:
                    download_tasks.append(task)

    return sorted(download_tasks, key=lambda t: t.asset_url), total_count


def _determine_architectures(
    platform: str,
    architecture: str | None,
    config: Config,
) -> list[str]:
    """Determine which architectures to update for a platform."""
    if architecture is not None:
        # Filter to only include the specified architecture if it's supported
        if architecture in config.platforms[platform]:
            return [architecture]
        log(
            f"Architecture {architecture} not configured for platform {platform}, skipping",
            "warning",
        )
        return []
    return config.platforms[platform]
