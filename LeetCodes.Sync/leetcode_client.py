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


def fetch_submission_code(title_slug: str) -> tuple[str, str]:
    """
    Fetches the latest accepted C# submission code and the problem description
    for a given problem slug.
    Returns (code: str, description: str, question_number: str)
    """

    # 1. Get question detail (description + number)
    detail_query = """
    query questionDetail($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        questionFrontendId
        title
        content
        difficulty
        exampleTestcases
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

    time.sleep(0.5)  # polite rate limiting

    # 2. Get latest accepted C# submission code
    submissions_query = """
    query submissions($offset: Int!, $limit: Int!, $lastKey: String, $questionSlug: String!) {
      submissionList(
        offset: $offset
        limit: $limit
        lastKey: $lastKey
        questionSlug: $questionSlug
      ) {
        submissions {
          id
          lang
          statusDisplay
          code
          timestamp
        }
      }
    }
    """
    resp = requests.post(
        GRAPHQL_URL,
        json={
            "query": submissions_query,
            "variables": {
                "offset": 0,
                "limit": 20,
                "lastKey": None,
                "questionSlug": title_slug,
            },
        },
        headers=_get_headers(),
        timeout=15,
    )
    resp.raise_for_status()
    all_subs = resp.json().get("data", {}).get("submissionList", {}).get("submissions", [])

    code = None
    for sub in all_subs:
        if sub["lang"] == "csharp" and sub["statusDisplay"] == "Accepted":
            code = sub["code"]
            break

    if not code:
        raise ValueError(f"No accepted C# submission found for {title_slug}")

    return code, question_id, title, difficulty
