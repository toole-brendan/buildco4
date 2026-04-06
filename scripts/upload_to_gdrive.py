#!/usr/bin/env python3
"""
Upload files from this repository to Google Drive.

Usage:
    # Upload a single file to the root of your Drive
    python scripts/upload_to_gdrive.py output/tam_workbook.xlsx

    # Upload a file into a specific Drive folder (by folder ID)
    python scripts/upload_to_gdrive.py output/tam_workbook.xlsx --folder 1aBcDeFgHiJkLmNoPqRsTuVwXyZ

    # Upload an entire directory (preserves structure)
    python scripts/upload_to_gdrive.py output/

    # Upload files matching a glob pattern
    python scripts/upload_to_gdrive.py "output/*.xlsx"

    # Dry run — show what would be uploaded without uploading
    python scripts/upload_to_gdrive.py output/ --dry-run

Authentication:
    Uses a Google service account. Set one of these:
      1. GOOGLE_SERVICE_ACCOUNT_JSON env var  (path to the JSON key file)
      2. Place a file named 'service_account.json' in the repo root

    To set up a service account:
      - Go to https://console.cloud.google.com/iam-admin/serviceaccounts
      - Create a service account and download the JSON key
      - Enable the Google Drive API for the project
      - Share the target Drive folder with the service account email
"""

import argparse
import glob
import json
import mimetypes
import os
import sys
from pathlib import Path

try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
except ImportError:
    print(
        "ERROR: Google API dependencies not installed.\n"
        "Run:  pip install google-api-python-client google-auth\n"
        "Or:   pip install -r requirements-gdrive.txt",
        file=sys.stderr,
    )
    sys.exit(1)

SCOPES = ["https://www.googleapis.com/auth/drive.file"]
REPO_ROOT = Path(__file__).resolve().parent.parent


def get_credentials():
    """Load service account credentials from env var or default path."""
    key_path = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not key_path:
        key_path = REPO_ROOT / "service_account.json"
    key_path = Path(key_path)
    if not key_path.exists():
        print(
            f"ERROR: Service account key not found at {key_path}\n"
            "Set GOOGLE_SERVICE_ACCOUNT_JSON env var or place service_account.json in repo root.",
            file=sys.stderr,
        )
        sys.exit(1)
    return service_account.Credentials.from_service_account_file(str(key_path), scopes=SCOPES)


def get_drive_service(credentials):
    return build("drive", "v3", credentials=credentials)


def find_or_create_folder(service, name, parent_id=None):
    """Find an existing folder by name under parent, or create it."""
    query = f"name = '{name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    if parent_id:
        query += f" and '{parent_id}' in parents"
    results = service.files().list(q=query, fields="files(id, name)", pageSize=1).execute()
    files = results.get("files", [])
    if files:
        return files[0]["id"]
    # Create it
    metadata = {"name": name, "mimeType": "application/vnd.google-apps.folder"}
    if parent_id:
        metadata["parents"] = [parent_id]
    folder = service.files().create(body=metadata, fields="id").execute()
    return folder["id"]


def upload_file(service, local_path, parent_folder_id=None, dry_run=False):
    """Upload a single file to Google Drive."""
    local_path = Path(local_path)
    mime_type, _ = mimetypes.guess_type(str(local_path))
    mime_type = mime_type or "application/octet-stream"

    if dry_run:
        dest = f"folder {parent_folder_id}" if parent_folder_id else "Drive root"
        print(f"  [dry-run] Would upload: {local_path} -> {dest} ({mime_type})")
        return None

    metadata = {"name": local_path.name}
    if parent_folder_id:
        metadata["parents"] = [parent_folder_id]

    media = MediaFileUpload(str(local_path), mimetype=mime_type, resumable=True)
    uploaded = service.files().create(body=metadata, media_body=media, fields="id, name, webViewLink").execute()

    print(f"  Uploaded: {local_path.name} -> {uploaded.get('webViewLink', uploaded['id'])}")
    return uploaded


def upload_directory(service, local_dir, parent_folder_id=None, dry_run=False):
    """Recursively upload a directory, preserving folder structure."""
    local_dir = Path(local_dir)
    folder_id = find_or_create_folder(service, local_dir.name, parent_folder_id) if not dry_run else None

    if dry_run:
        print(f"  [dry-run] Would create folder: {local_dir.name}")

    count = 0
    for item in sorted(local_dir.iterdir()):
        if item.name.startswith("."):
            continue
        if item.is_dir():
            count += upload_directory(service, item, folder_id, dry_run)
        elif item.is_file():
            upload_file(service, item, folder_id, dry_run)
            count += 1
    return count


def resolve_targets(patterns):
    """Resolve file/dir paths and glob patterns into concrete paths."""
    targets = []
    for pattern in patterns:
        # Try as glob first
        matches = glob.glob(pattern, recursive=True)
        if matches:
            targets.extend(Path(m) for m in matches)
        else:
            p = Path(pattern)
            if p.exists():
                targets.append(p)
            else:
                print(f"  WARNING: No match for '{pattern}', skipping.", file=sys.stderr)
    return targets


def main():
    parser = argparse.ArgumentParser(description="Upload files from this repo to Google Drive.")
    parser.add_argument("targets", nargs="+", help="Files, directories, or glob patterns to upload.")
    parser.add_argument("--folder", default=None, help="Google Drive folder ID to upload into.")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be uploaded without uploading.")
    args = parser.parse_args()

    targets = resolve_targets(args.targets)
    if not targets:
        print("No files to upload.", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(targets)} target(s) to upload.")

    if not args.dry_run:
        creds = get_credentials()
        service = get_drive_service(creds)
    else:
        service = None

    total = 0
    for target in targets:
        if target.is_dir():
            total += upload_directory(service, target, args.folder, args.dry_run)
        elif target.is_file():
            upload_file(service, target, args.folder, args.dry_run)
            total += 1

    print(f"\nDone. {'Would upload' if args.dry_run else 'Uploaded'} {total} file(s).")


if __name__ == "__main__":
    main()
