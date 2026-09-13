#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import time


def config_directory():
    return Path(
        os.environ.get(
            "XDG_CONFIG_HOME",
            Path.home() / ".config"
        )
    ) / "gui4rivalcfg"


def write_result(status, version, detail=""):
    directory = config_directory()
    directory.mkdir(parents=True, exist_ok=True)
    result_file = directory / "update-result.json"
    temporary_file = directory / "update-result.json.tmp"
    temporary_file.write_text(
        json.dumps(
            {
                "status": status,
                "version": version,
                "detail": detail,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    temporary_file.replace(result_file)


def verify_archive(path, expected_digest):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    if digest.hexdigest().lower() != expected_digest.lower():
        raise RuntimeError("SHA-256 checksum mismatch")


def extract_archive(path, destination, version):
    expected_root = f"gui4rivalcfg-{version}"
    destination_resolved = destination.resolve()

    with tarfile.open(path, "r:gz") as archive:
        for member in archive.getmembers():
            member_path = (destination / member.name).resolve()
            if destination_resolved not in member_path.parents and member_path != destination_resolved:
                raise RuntimeError("Unsafe path in release archive")
            if member.issym() or member.islnk() or member.isdev():
                raise RuntimeError("Unsupported entry in release archive")
            if (
                member.name != expected_root
                and not member.name.startswith(expected_root + "/")
            ):
                raise RuntimeError("Unexpected release archive layout")
        # Paths and entry types were validated above; omit the newer filter
        # argument to retain compatibility with older supported Python 3.
        archive.extractall(destination)

    release_directory = destination / expected_root
    installer = release_directory / "install.sh"
    if not installer.is_file():
        raise RuntimeError("install.sh is missing from release archive")
    return installer


def run_update(archive_path, expected_digest, version):
    verify_archive(archive_path, expected_digest)
    with tempfile.TemporaryDirectory(prefix="gui4rivalcfg-update-") as temp_dir:
        installer = extract_archive(
            archive_path,
            Path(temp_dir),
            version,
        )
        result = subprocess.run(
            [str(installer)],
            cwd=installer.parent,
            text=True,
            capture_output=True,
        )
        if result.returncode != 0:
            detail = result.stderr.strip() or result.stdout.strip()
            raise RuntimeError(detail or "Installer failed")


def restart_application(launcher):
    subprocess.Popen(
        [launcher],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )


def wait_for_process(process_id, timeout=30):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            os.kill(process_id, 0)
        except ProcessLookupError:
            return
        except PermissionError:
            return
        time.sleep(0.1)
    raise RuntimeError("Application did not close before update")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", required=True)
    parser.add_argument("--sha256", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--launcher", required=True)
    parser.add_argument("--wait-pid", required=True, type=int)
    args = parser.parse_args()

    archive_path = Path(args.archive)
    try:
        wait_for_process(args.wait_pid)
        run_update(archive_path, args.sha256, args.version)
        write_result("success", args.version)
    except Exception as error:
        write_result("error", args.version, str(error))
    finally:
        try:
            archive_path.unlink(missing_ok=True)
        finally:
            restart_application(args.launcher)


if __name__ == "__main__":
    sys.exit(main())
