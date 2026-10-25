from __future__ import annotations

import concurrent.futures
import hashlib
import json
from pathlib import Path
import urllib.request
import zipfile


ROOT = Path(__file__).resolve().parent / "tools"
HEADERS = {"User-Agent": "Cadence-Library-Upload", "Accept": "application/vnd.github+json"}
ASSETS = [
    ("git-for-windows/git", "v2.56.0.windows.3", "MinGit-2.56.0.3-64-bit.zip", "mingit", 39854943),
    ("cli/cli", "v2.103.2", "gh_2.103.2_windows_amd64.zip", "gh", 15195500),
    ("git-lfs/git-lfs", "v3.8.1", "git-lfs-windows-amd64-v3.8.1.zip", "git-lfs", 5870805),
]


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=60)


def prepare(spec):
    repo, tag, filename, dirname, size = spec
    with get(f"https://api.github.com/repos/{repo}/releases/tags/{tag}") as response:
        release = json.load(response)
    asset = next(a for a in release["assets"] if a["name"] == filename)
    digest = asset.get("digest") or ""
    if not digest.startswith("sha256:"):
        raise RuntimeError(f"No official SHA-256 digest present for {filename}")
    if asset["size"] != size:
        raise RuntimeError(f"Unexpected official size for {filename}")
    url = asset["browser_download_url"]
    expected_prefix = f"https://github.com/{repo}/releases/download/{tag}/"
    if not url.startswith(expected_prefix):
        raise RuntimeError(f"Unexpected asset origin for {filename}")
    download_path = ROOT / filename
    if not download_path.exists():
        part = ROOT / (filename + ".partial")
        with get(url) as response, part.open("wb") as output:
            while chunk := response.read(4 * 1024 * 1024):
                output.write(chunk)
        part.replace(download_path)
    actual_size = download_path.stat().st_size
    actual_sha = hashlib.file_digest(download_path.open("rb"), "sha256").hexdigest()
    if actual_size != size or actual_sha != digest.removeprefix("sha256:"):
        raise RuntimeError(f"Official size or SHA-256 verification failed: {filename}")
    destination = ROOT / dirname
    destination.mkdir(exist_ok=True)
    with zipfile.ZipFile(download_path) as archive:
        for member in archive.infolist():
            target = (destination / member.filename).resolve()
            if not target.is_relative_to(destination.resolve()):
                raise RuntimeError(f"Unsafe ZIP entry in {filename}")
        archive.extractall(destination)
    record = {
        "repository": repo,
        "tag": tag,
        "asset": filename,
        "url": url,
        "release_api_url": f"https://api.github.com/repos/{repo}/releases/tags/{tag}",
        "bytes": actual_size,
        "sha256": actual_sha,
        "official_digest": digest,
        "verification": "PASS_OFFICIAL_GITHUB_RELEASE_DIGEST",
        "extracted_to": str(destination),
    }
    (ROOT / (dirname + "_verification.json")).write_text(json.dumps(record, indent=2), encoding="utf-8")
    return record


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    records = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(prepare, spec) for spec in ASSETS]
        for future in concurrent.futures.as_completed(futures):
            record = future.result()
            records.append(record)
            print(json.dumps(record), flush=True)
    (ROOT / "portable_tools_verification.json").write_text(json.dumps(records, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
