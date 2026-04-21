"""
GitHub Client
Reads the existing repo structure and pushes new solution files via GitHub REST API.
Requires GH_PAT (Personal Access Token with repo scope).
"""

import os
import base64
import requests

GITHUB_API = "https://api.github.com"
REPO_OWNER = os.environ.get("GH_REPO_OWNER", "Raphsodyz")
REPO_NAME = os.environ.get("GH_REPO_NAME", "LeetCodes")
BRANCH = os.environ.get("GH_BRANCH", "main")


def _get_headers():
    token = os.environ["GH_PAT"]
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def fetch_existing_problem_names() -> set[str]:
    """
    Returns a set of .cs filenames (without extension) already in
    LeetCodes.Solutions/Problems/ on GitHub.
    e.g. {"InvertBinaryTree", "StringToInteger", ...}
    """
    print("📂 Fetching existing problems from GitHub repo...")

    url = f"{GITHUB_API}/repos/{REPO_OWNER}/{REPO_NAME}/contents/LeetCodes.Solutions/Problems"
    resp = requests.get(url, headers=_get_headers(), timeout=15)

    if resp.status_code == 404:
        print("⚠️  Problems folder not found on GitHub, assuming empty.")
        return set()

    resp.raise_for_status()
    files = resp.json()
    names = {
        f["name"].replace(".cs", "")
        for f in files
        if f["name"].endswith(".cs")
    }
    print(f"✅ Found {len(names)} existing problems in repo.")
    return names


def fetch_factory_file() -> tuple[str, str]:
    """
    Fetches the current SolutionsFactory.cs content and its SHA from GitHub.
    Returns (content: str, sha: str)
    """
    url = f"{GITHUB_API}/repos/{REPO_OWNER}/{REPO_NAME}/contents/LeetCodes.Solutions/Factory/SolutionsFactory.cs"
    resp = requests.get(url, headers=_get_headers(), timeout=15)
    resp.raise_for_status()
    data = resp.json()
    content = base64.b64decode(data["content"]).decode("utf-8")
    return content, data["sha"]


def commit_new_solution(
    class_name: str,
    file_content: str,
    question_id: str,
    title: str,
) -> None:
    """
    Commits a new .cs solution file to LeetCodes.Solutions/Problems/.
    """
    path = f"LeetCodes.Solutions/Problems/{class_name}.cs"
    encoded = base64.b64encode(file_content.encode("utf-8")).decode("utf-8")
    commit_message = f"Add solution: #{question_id} - {title}"

    url = f"{GITHUB_API}/repos/{REPO_OWNER}/{REPO_NAME}/contents/{path}"
    payload = {
        "message": commit_message,
        "content": encoded,
        "branch": BRANCH,
    }

    resp = requests.put(url, json=payload, headers=_get_headers(), timeout=15)
    resp.raise_for_status()
    print(f"  ✅ Committed: {commit_message}")


def update_factory_file(
    new_content: str,
    sha: str,
    class_names_added: list[str],
) -> None:
    """
    Updates SolutionsFactory.cs on GitHub with the new class entries added.
    """
    path = "LeetCodes.Solutions/Factory/SolutionsFactory.cs"
    encoded = base64.b64encode(new_content.encode("utf-8")).decode("utf-8")
    added = ", ".join(class_names_added)
    commit_message = f"Update SolutionsFactory: add {added}"

    url = f"{GITHUB_API}/repos/{REPO_OWNER}/{REPO_NAME}/contents/{path}"
    payload = {
        "message": commit_message,
        "content": encoded,
        "sha": sha,
        "branch": BRANCH,
    }

    resp = requests.put(url, json=payload, headers=_get_headers(), timeout=15)
    resp.raise_for_status()
    print(f"  ✅ Updated SolutionsFactory.cs with: {added}")
