"""Utilities to collect git history and GitHub metadata for multiple repositories."""
from __future__ import annotations

import argparse
import dataclasses
import importlib.util
import json
import logging
import os
import pathlib
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request
from typing import Dict, Iterable, List, Optional

if importlib.util.find_spec("pandas") is None:
    raise SystemExit("pandas is required to run this script. Install it with `pip install pandas pyarrow`.")

import pandas as pd

PYARROW_AVAILABLE = importlib.util.find_spec("pyarrow") is not None

@dataclasses.dataclass
class CommitRecord:
    repo: str
    sha: str
    author_name: str
    author_email: str
    authored_at: str
    subject: str
    files_changed: int
    insertions: int
    deletions: int
    tags: List[str]
    releases: List[str]

    def to_dict(self) -> Dict[str, object]:
        data = dataclasses.asdict(self)
        data["tags"] = ",".join(self.tags)
        data["releases"] = ",".join(self.releases)
        return data


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Clone and harvest git and GitHub metadata for multiple repositories.")
    parser.add_argument(
        "repos",
        nargs="*",
        help="Repositories to process. Accepts full GitHub URLs or owner/repo identifiers.",
    )
    parser.add_argument(
        "--repo-list-file",
        type=pathlib.Path,
        help="Optional file containing one repository per line. Lines starting with # are ignored.",
    )
    parser.add_argument(
        "--output-dir",
        default=pathlib.Path("data/raw"),
        type=pathlib.Path,
        help="Directory where CSV and Parquet files will be written.",
    )
    parser.add_argument(
        "--token",
        help="GitHub token used for API requests. Defaults to the GITHUB_TOKEN environment variable if set.",
    )
    parser.add_argument(
        "--skip-parquet",
        action="store_true",
        help="Skip writing Parquet files (useful when pyarrow or fastparquet are not installed).",
    )
    parser.add_argument(
        "--keep-clone",
        action="store_true",
        help="Keep the cloned repositories inside the output directory instead of deleting the temporary clone.",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging verbosity.",
    )
    return parser.parse_args(argv)


def gather_repos(cli_repos: Iterable[str], repo_list_path: Optional[pathlib.Path]) -> List[str]:
    repos = [repo.strip() for repo in cli_repos if repo.strip()]
    if repo_list_path and repo_list_path.exists():
        for line in repo_list_path.read_text(encoding="utf-8").splitlines():
            cleaned = line.strip()
            if cleaned and not cleaned.startswith("#"):
                repos.append(cleaned)
    return repos


def normalize_repo_input(repo: str) -> Dict[str, str]:
    if repo.startswith("git@github.com:"):
        path = repo.split(":", maxsplit=1)[1]
    elif "github.com" in repo:
        parsed = urllib.parse.urlparse(repo)
        path = parsed.path.lstrip("/")
    else:
        path = repo

    path = path.removesuffix(".git")
    parts = path.split("/")
    if len(parts) < 2:
        raise ValueError(f"Repository {repo!r} is not a recognized GitHub reference.")

    owner_repo = "/".join(parts[:2])
    repo_slug = owner_repo.replace("/", "_")
    clone_url = f"https://github.com/{owner_repo}.git"
    return {"owner_repo": owner_repo, "repo_slug": repo_slug, "clone_url": clone_url}


def run_git_command(repo_path: pathlib.Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=repo_path, check=True, capture_output=True, text=True)
    return result.stdout


def parse_git_numstat(log_output: str, repo_slug: str) -> List[CommitRecord]:
    commits: List[CommitRecord] = []
    current: Optional[CommitRecord] = None
    for line in log_output.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) >= 5 and len(parts[0]) == 40:
            if current:
                commits.append(current)
            sha, authored_at, author_name, author_email, subject = parts[:5]
            current = CommitRecord(
                repo=repo_slug,
                sha=sha,
                author_name=author_name,
                author_email=author_email,
                authored_at=authored_at,
                subject=subject,
                files_changed=0,
                insertions=0,
                deletions=0,
                tags=[],
                releases=[],
            )
            continue

        if current is None:
            continue

        if len(parts) >= 3:
            insertions, deletions = parts[:2]
            if insertions.isdigit():
                current.insertions += int(insertions)
            if deletions.isdigit():
                current.deletions += int(deletions)
            current.files_changed += 1
    if current:
        commits.append(current)
    return commits


def fetch_paginated(endpoint: str, token: Optional[str]) -> List[Dict[str, object]]:
    items: List[Dict[str, object]] = []
    page = 1
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "repo-harvester"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    while True:
        url = f"{endpoint}?per_page=100&page={page}"
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
        if not payload:
            break
        items.extend(payload)
        page += 1
    return items


def build_tag_and_release_maps(owner_repo: str, token: Optional[str]) -> Dict[str, Dict[str, List[str]]]:
    tags_endpoint = f"https://api.github.com/repos/{owner_repo}/tags"
    releases_endpoint = f"https://api.github.com/repos/{owner_repo}/releases"

    tags = fetch_paginated(tags_endpoint, token)
    releases = fetch_paginated(releases_endpoint, token)

    tag_by_commit: Dict[str, List[str]] = {}
    for tag in tags:
        commit_sha = tag.get("commit", {}).get("sha")
        if commit_sha:
            tag_by_commit.setdefault(commit_sha, []).append(tag.get("name", ""))

    release_by_commit: Dict[str, List[str]] = {}
    for release in releases:
        tag_name = release.get("tag_name")
        if not tag_name:
            continue
        matching_shas = [sha for sha, tag_names in tag_by_commit.items() if tag_name in tag_names]
        for sha in matching_shas:
            release_by_commit.setdefault(sha, []).append(release.get("name") or tag_name)

    return {"tags": tag_by_commit, "releases": release_by_commit}


def write_outputs(commits: List[CommitRecord], output_dir: pathlib.Path, repo_slug: str, skip_parquet: bool) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame([commit.to_dict() for commit in commits])

    csv_path = output_dir / f"{repo_slug}.csv"
    df.to_csv(csv_path, index=False)

    if skip_parquet:
        logging.info("Skipping Parquet export because --skip-parquet was provided.")
        return

    if not PYARROW_AVAILABLE:
        logging.warning("pyarrow is not available; skipping Parquet export.")
        return

    parquet_path = output_dir / f"{repo_slug}.parquet"
    df.to_parquet(parquet_path, index=False)


def process_repo(repo: str, output_dir: pathlib.Path, token: Optional[str], keep_clone: bool, skip_parquet: bool) -> None:
    details = normalize_repo_input(repo)
    owner_repo = details["owner_repo"]
    repo_slug = details["repo_slug"]
    clone_url = details["clone_url"]

    logging.info("Processing %s", owner_repo)
    repo_destination = output_dir / f"{repo_slug}_clone"

    with tempfile.TemporaryDirectory(dir=output_dir if keep_clone else None) as tmp_dir:
        clone_path = pathlib.Path(tmp_dir) / repo_slug
        subprocess.run(["git", "clone", "--quiet", clone_url, str(clone_path)], check=True)

        if keep_clone:
            repo_destination.mkdir(parents=True, exist_ok=True)
            run_git_command(clone_path, "bundle", "create", str(repo_destination / "repo.bundle"), "--all")

        git_log_stat = run_git_command(clone_path, "log", "--stat")
        (output_dir / f"{repo_slug}_git_log.txt").write_text(git_log_stat, encoding="utf-8")

        numstat_output = run_git_command(
            clone_path,
            "log",
            "--date=iso-strict",
            "--pretty=format:%H\t%ad\t%an\t%ae\t%s",
            "--numstat",
        )
        commits = parse_git_numstat(numstat_output, repo_slug)

        metadata_maps = build_tag_and_release_maps(owner_repo, token)
        tags_by_commit = metadata_maps["tags"]
        releases_by_commit = metadata_maps["releases"]

        for commit in commits:
            commit.tags = tags_by_commit.get(commit.sha, [])
            commit.releases = releases_by_commit.get(commit.sha, [])

        write_outputs(commits, output_dir, repo_slug, skip_parquet)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    logging.basicConfig(level=getattr(logging, args.log_level), format="[%(levelname)s] %(message)s")

    repos = gather_repos(args.repos, args.repo_list_file)
    if not repos:
        logging.error("No repositories provided. Specify them as arguments or via --repo-list-file.")
        return 1

    token = args.token or os.getenv("GITHUB_TOKEN")

    for repo in repos:
        try:
            process_repo(repo, args.output_dir, token, args.keep_clone, args.skip_parquet)
        except Exception as exc:  # noqa: BLE001
            logging.error("Failed to process %s: %s", repo, exc)
            continue

    return 0


if __name__ == "__main__":
    sys.exit(main())
