"""
LeetCode Client
Fetches accepted C# submissions from LeetCode using the unofficial GraphQL API.
Requires LEETCODE_SESSION and LEETCODE_CSRF cookies from your browser.
"""

import os
import requests
import time

LEETCODE_BASE = "https://leetcode.com"
GRAPHQL_URL = f"{LEETCODE_BASE}/graphql"


def _get_headers():
    session = os.environ["LEETCODE_SESSION"]
    csrf = os.environ["LEETCODE_CSRF"]
    return {
        "Content-Type": "application/json",
        "Cookie": f"LEETCODE_SESSION={session}; csrftoken={csrf}",
        "x-csrftoken": csrf,
        "Referer": LEETCODE_BASE,
        "User-Agent": "Mozilla/5.0",
    }


def fetch_accepted_problems() -> list[dict]:
    """
    Returns a list of all problems where the user has an accepted C# submission.
    Each item: { "titleSlug": str, "title": str, "questionId": str }
    """
    print("📡 Fetching accepted submissions from LeetCode...")

    query = """
    query recentAcSubmissions($username: String!, $limit: Int!) {
      recentAcSubmissionList(username: $username, limit: $limit) {
        id
        title
        titleSlug
        timestamp
        lang
      }
    }
    """

    username = os.environ["LEETCODE_USERNAME"]
    # Fetch up to 1000 accepted submissions
    payload = {
        "query": query,
        "variables": {"username": username, "limit": 1000},
    }

    resp = requests.post(GRAPHQL_URL, json=payload, headers=_get_headers(), timeout=15)
    resp.raise_for_status()
    data = resp.json()

    submissions = data.get("data", {}).get("recentAcSubmissionList", [])

    # Filter only C# submissions and deduplicate by titleSlug (keep first/latest)
    seen = set()
    csharp_problems = []
    for sub in submissions:
        if sub["lang"] == "csharp" and sub["titleSlug"] not in seen:
            seen.add(sub["titleSlug"])
            csharp_problems.append(sub)

    print(f"✅ Found {len(csharp_problems)} accepted C# problems on LeetCode.")
    return csharp_problems


def fetch_submission_code(title_slug: str, submission_id: str) -> tuple[str, str, str, str]:
    """
    Fetches the accepted C# submission code and problem metadata.
    Uses the submission ID already returned by recentAcSubmissionList (step 1),
    then calls submissionDetails to get the actual code.
    Returns (code, question_id, title, difficulty)
    """

    # 1. Get question metadata (number, difficulty) via questionDetail
    detail_query = """
    query questionDetail($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        questionFrontendId
        title
        difficulty
      }
    }
    """
    resp = requests.post(
        GRAPHQL_URL,
        json={"query": detail_query, "variables": {"titleSlug": title_slug}},
        headers=_get_headers(),
        timeout=15,
    )
    resp.raise_for_status()
    question_data = resp.json().get("data", {}).get("question", {})
    question_id = question_data.get("questionFrontendId", "?")
    title = question_data.get("title", title_slug)
    difficulty = question_data.get("difficulty", "")

    time.sleep(0.5)  # polite rate limiting between requests

    # 2. Fetch the actual submission code using the submission ID
    # submissionDetails is the correct endpoint — submissionList requires a paid plan
    details_query = """
    query submissionDetails($submissionId: Int!) {
      submissionDetails(submissionId: $submissionId) {
        code
        lang {
          name
        }
        statusCode
      }
    }
    """
    resp = requests.post(
        GRAPHQL_URL,
        json={
            "query": details_query,
            "variables": {"submissionId": int(submission_id)},
        },
        headers=_get_headers(),
        timeout=15,
    )
    resp.raise_for_status()

    details = resp.json().get("data", {}).get("submissionDetails")
    if not details or not details.get("code"):
        raise ValueError(f"Could not fetch submission code for ID {submission_id} ({title_slug})")

    code = details["code"]
    return code, question_id, title, difficulty
