"""
LeetCode → GitHub Sync Agent
=============================
Fetches your accepted C# submissions from LeetCode and pushes any new ones
to your GitHub repo (Raphsodyz/LeetCodes) following the project's code structure.

Required environment variables (set as GitHub Actions secrets):
  LEETCODE_SESSION   — your LeetCode session cookie
  LEETCODE_CSRF      — your LeetCode CSRF token
  LEETCODE_USERNAME  — your LeetCode username
  GH_PAT             — GitHub Personal Access Token (repo scope)

Optional:
  GH_REPO_OWNER      — default: Raphsodyz
  GH_REPO_NAME       — default: LeetCodes
  GH_BRANCH          — default: main
  DRY_RUN            — set to "true" to preview without committing
"""

import os
import sys
import time

from leetcode_client import fetch_accepted_problems, fetch_submission_code
from github_client import (
    fetch_existing_problem_names,
    fetch_factory_file,
    commit_new_solution,
    update_factory_file,
)
from code_formatter import slugify_to_classname, format_solution_file, inject_into_factory

DRY_RUN = os.environ.get("DRY_RUN", "false").lower() == "true"


def validate_env():
    required = ["LEETCODE_SESSION", "LEETCODE_CSRF", "LEETCODE_USERNAME", "GH_PAT"]
    missing = [k for k in required if not os.environ.get(k)]
    if missing:
        print(f"❌ Missing required environment variables: {', '.join(missing)}")
        sys.exit(1)


def main():
    print("🚀 LeetCode → GitHub Sync Agent starting...")
    if DRY_RUN:
        print("🔍 DRY RUN mode — no commits will be made.\n")

    validate_env()

    # 1. Fetch all accepted C# problems from LeetCode
    lc_problems = fetch_accepted_problems()
    if not lc_problems:
        print("ℹ️  No accepted C# problems found on LeetCode. Exiting.")
        return

    # 2. Fetch existing problems already in the GitHub repo
    existing_names = fetch_existing_problem_names()

    # 3. Determine which problems are new (not yet in GitHub)
    new_problems = []
    for problem in lc_problems:
        class_name = slugify_to_classname(problem["title"])
        if class_name not in existing_names:
            new_problems.append({**problem, "class_name": class_name})

    if not new_problems:
        print("✨ Everything is up to date! No new problems to sync.")
        return

    print(f"\n🆕 Found {len(new_problems)} new problem(s) to sync:")
    for p in new_problems:
        print(f"   - {p['title']} → {p['class_name']}.cs")

    if DRY_RUN:
        print("\n🔍 DRY RUN: would commit the above. Set DRY_RUN=false to apply.")
        return

    # 4. Fetch the current SolutionsFactory.cs (we'll update it once at the end)
    factory_content, factory_sha = fetch_factory_file()
    updated_factory = factory_content
    classes_added = []

    # 5. For each new problem: fetch code, format it, commit it
    print("\n📤 Syncing new problems...\n")
    for problem in new_problems:
        slug = problem["titleSlug"]
        class_name = problem["class_name"]

        try:
            print(f"⬇️  Fetching submission for: {problem['title']}")
            code, question_id, title, difficulty = fetch_submission_code(slug)

            # Format into the project's .cs structure
            file_content = format_solution_file(
                class_name=class_name,
                question_id=question_id,
                title=title,
                difficulty=difficulty,
                raw_code=code,
            )

            # Commit the new .cs file
            commit_new_solution(
                class_name=class_name,
                file_content=file_content,
                question_id=question_id,
                title=title,
            )

            # Queue factory update
            updated_factory = inject_into_factory(updated_factory, class_name)
            classes_added.append(class_name)

            time.sleep(1)  # polite rate limiting between commits

        except Exception as e:
            print(f"  ⚠️  Skipping {problem['title']}: {e}")
            continue

    # 6. Update SolutionsFactory.cs once with all new entries
    if classes_added:
        print(f"\n🔧 Updating SolutionsFactory.cs...")
        update_factory_file(
            new_content=updated_factory,
            sha=factory_sha,
            class_names_added=classes_added,
        )

    print(f"\n🎉 Done! Synced {len(classes_added)} new problem(s) to GitHub.")


if __name__ == "__main__":
    main()
