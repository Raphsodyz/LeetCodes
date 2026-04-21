"""
Code Formatter
Wraps a raw LeetCode C# submission into the project's class structure,
matching the exact pattern used in the existing solution files.
"""

import re


def slugify_to_classname(title: str) -> str:
    """
    Converts a LeetCode problem title to a valid PascalCase C# class name.
    e.g. "Longest Substring Without Repeating Characters" -> "LongestSubstringWithoutRepeatingCharacters"
    e.g. "Two Sum" -> "TwoSum"
    """
    # Remove non-alphanumeric characters (keep spaces for splitting)
    cleaned = re.sub(r"[^a-zA-Z0-9 ]", "", title)
    # PascalCase each word
    return "".join(word.capitalize() for word in cleaned.split())


def format_solution_file(
    class_name: str,
    question_id: str,
    title: str,
    difficulty: str,
    raw_code: str,
) -> str:
    """
    Wraps the raw LeetCode submission code into the project's standard .cs format.

    The pattern (from existing files):
      - namespace LeetCodes.Solutions.Problems
      - public class <ClassName> : ISolutionContract
      - public void Solution() { ... }
      - Problem description in a comment block inside Solution()
      - Actual solution logic after the comment

    Since LeetCode submissions are typically just the class body (Solution method + helpers),
    we wrap them into our project structure.
    """

    # Clean up the raw code — LeetCode often wraps in a Solution class
    inner_code = _extract_inner_code(raw_code)

    file_content = f"""using LeetCodes.Solutions.Contract;

namespace LeetCodes.Solutions.Problems
{{
    public class {class_name} : ISolutionContract
    {{
        public void Solution()
        {{
            /*
            {question_id}. {title}
            Difficulty: {difficulty}
            https://leetcode.com/problems/{_title_to_slug(title)}/
            */

            // TODO: Add your test call here, e.g.:
            // Console.WriteLine(YourMethod(input));
        }}

{_indent(inner_code, 2)}
    }}
}}
"""
    return file_content


def _title_to_slug(title: str) -> str:
    """Converts title to leetcode URL slug."""
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def _extract_inner_code(raw_code: str) -> str:
    """
    LeetCode C# submissions are usually wrapped in:
        public class Solution {
            public int SomeMethod(...) { ... }
        }

    We extract everything INSIDE the outer Solution class braces,
    so it can be placed inside our ISolutionContract class.
    If no outer class is detected, returns raw_code as-is.
    """
    # Match "public class Solution {" wrapper
    pattern = re.compile(
        r"(?:public\s+class\s+Solution\s*\{)(.*)\}", re.DOTALL
    )
    match = pattern.search(raw_code)
    if match:
        inner = match.group(1).strip()
        return _dedent(inner)
    return raw_code.strip()


def _dedent(code: str) -> str:
    """Remove one level of leading 4-space or tab indentation from each line."""
    lines = code.split("\n")
    result = []
    for line in lines:
        if line.startswith("    "):
            result.append(line[4:])
        elif line.startswith("\t"):
            result.append(line[1:])
        else:
            result.append(line)
    return "\n".join(result)


def _indent(code: str, levels: int) -> str:
    """Add `levels * 4` spaces of indentation to each non-empty line."""
    prefix = "    " * levels
    lines = code.split("\n")
    return "\n".join(prefix + line if line.strip() else line for line in lines)


def inject_into_factory(factory_content: str, class_name: str) -> str:
    """
    Adds a new entry into SolutionsFactory.cs switch expression.

    Finds the last `nameof(...)` line in the switch and inserts after it:
        nameof(NewClassName) => new NewClassName(),
    """
    new_entry = f"                nameof({class_name}) => new {class_name}(),"

    # Find the last existing nameof(...) line and insert after it
    lines = factory_content.split("\n")
    last_nameof_idx = -1
    for i, line in enumerate(lines):
        if "nameof(" in line and "=>" in line:
            last_nameof_idx = i

    if last_nameof_idx == -1:
        raise ValueError("Could not find switch entries in SolutionsFactory.cs")

    # Check if already exists
    if class_name in factory_content:
        return factory_content

    lines.insert(last_nameof_idx + 1, new_entry)
    return "\n".join(lines)
