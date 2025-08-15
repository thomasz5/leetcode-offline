#!/usr/bin/env python3
import argparse
from pathlib import Path

REPO_ROOT = Path("/Users/Thomas/PROJECT/Leetcode").resolve()
PROBLEMS_DIR = REPO_ROOT / "problems"
TESTS_DIR = REPO_ROOT / "tests"


PROBLEM_TEMPLATE = '''
from typing import List, Optional, Tuple, Dict, Any


def solve(*args, **kwargs):
    """
    Implement the solution for the problem:
    Title: {title}
    Slug: {slug}

    Replace the signature and body with the actual implementation.
    """
    raise NotImplementedError


if __name__ == "__main__":
    # Optional local debug
    print(solve())
'''


TEST_TEMPLATE = '''
import pytest

from problems.{module_name} import solve


def test_example():
    # Replace with real examples for {title}
    with pytest.raises(NotImplementedError):
        solve()
'''


def to_valid_module_name(name: str) -> str:
    # Convert to a valid Python identifier for module/filename: lowercase words separated by underscores
    normalized = name.strip().lower()
    parts = []
    word = []
    for ch in normalized:
        if ch.isalnum():
            word.append(ch)
        else:
            if word:
                parts.append(''.join(word))
                word = []
    if word:
        parts.append(''.join(word))
    module = '_'.join(p for p in parts if p)
    if not module:
        module = "problem"
    return module


def ensure_dirs():
    PROBLEMS_DIR.mkdir(parents=True, exist_ok=True)
    TESTS_DIR.mkdir(parents=True, exist_ok=True)


def write_file(path: Path, content: str):
    if path.exists():
        return
    path.write_text(content, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Create a new LeetCode problem scaffold")
    parser.add_argument("--name", required=True, help="Problem slug, e.g. 'two-sum'")
    parser.add_argument("--title", required=True, help="Human title, e.g. 'Two Sum'")
    args = parser.parse_args()

    module_name = to_valid_module_name(args.name)
    title = args.title

    ensure_dirs()

    problem_path = PROBLEMS_DIR / f"{module_name}.py"
    test_path = TESTS_DIR / f"test_{module_name}.py"

    write_file(problem_path, PROBLEM_TEMPLATE.format(title=title, slug=module_name))
    write_file(test_path, TEST_TEMPLATE.format(module_name=module_name, title=title))

    print(f"Created: {problem_path}")
    print(f"Created: {test_path}")
    print("Next steps:\n - Implement solve(...)\n - Add real tests\n - Run: pytest -q")


if __name__ == "__main__":
    main()


