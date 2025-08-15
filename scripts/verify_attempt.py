#!/usr/bin/env python3
import argparse
import importlib.util
import inspect
from pathlib import Path
from typing import Any, Callable, Dict, List, Tuple

REPO = Path("/Users/Thomas/PROJECT/Leetcode").resolve()
ATTEMPT_DIR = REPO / "attempt"
ANSWER_DIR = REPO / "question-answer"


def to_module_name(name: str) -> str:
    normalized = name.strip().lower()
    parts: List[str] = []
    token: List[str] = []
    for ch in normalized:
        if ch.isalnum():
            token.append(ch)
        else:
            if token:
                parts.append(''.join(token))
                token = []
    if token:
        parts.append(''.join(token))
    return '_'.join(parts) if parts else 'problem'


def load_module_from_path(module_name: str, file_path: Path):
    if not file_path.exists():
        return None
    spec = importlib.util.spec_from_file_location(module_name, str(file_path))
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[attr-defined]
    return module


def get_solution_class(module) -> Any:
    return getattr(module, 'Solution', None)


def get_public_methods(cls: Any) -> Dict[str, Callable]:
    methods: Dict[str, Callable] = {}
    for name, member in inspect.getmembers(cls, predicate=inspect.isfunction):
        if name.startswith('_'):
            continue
        # Exclude methods not defined on this class (inherited dunders etc.)
        owner = getattr(member, '__qualname__', '')
        if cls.__name__ in owner:
            methods[name] = member
    return methods


def known_tests() -> Dict[str, Dict[str, List[Tuple[Tuple[Any, ...], Any]]]]:
    """
    Mapping: module_name -> method_name -> list of ((args...), expected_or_None)
    For in-place methods, expected_or_None can be a callable that validates.
    """
    def rotate_check(pre: Tuple[Any, ...], post: Tuple[Any, ...]):
        nums_before, k = pre
        nums_after, _ = post
        n = len(nums_before)
        kk = k % n if n else 0
        expected_nums = nums_before[-kk:] + nums_before[:-kk] if n and kk else nums_before[:]
        return nums_after == expected_nums

    return {
        'candies': {
            'candy': [
                ((([1],), {}), 1),
                ((([1,0,2],), {}), 5),
                ((([1,2,2],), {}), 4),
                ((([1,3,4,5,2],), {}), 11),
            ]
        },
        'lastword_easy': {
            'lengthOfLastWord': [
                ((("Hello World",), {}), 5),
                ((("   fly me   to   the moon  ",), {}), 4),
                ((("a",), {}), 1),
            ]
        },
        'reverse': {
            'reverseWords': [
                ((("the sky is blue",), {}), "blue is sky the"),
                ((("  hello world  ",), {}), "world hello"),
                ((("a good   example",), {}), "example good a"),
            ]
        },
        'roman_easy': {
            'romanToInt': [
                ((("III",), {}), 3),
                ((("LVIII",), {}), 58),
                ((("MCMXCIV",), {}), 1994),
            ]
        },
        'roman_med': {
            'intToRoman': [
                (((3,), {}), "III"),
                (((58,), {}), "LVIII"),
                (((1994,), {}), "MCMXCIV"),
            ]
        },
        'rotate': {
            'rotate': [
                ((([1,2,3,4,5,6,7], 3), {}), rotate_check),
                ((([-1,-100,3,99], 2), {}), rotate_check),
            ]
        },
        'stock': {
            'maxProfit': [
                ((([7,1,5,3,6,4],), {}), 7),
                ((([1,2,3,4,5],), {}), 4),
                ((([7,6,4,3,1],), {}), 0),
            ]
        },
        'text_justification': {
            'fullJustify': [
                (((["This","is","an","example","of","text","justification."], 16), {}),
                 ["This    is    an","example  of text","justification.  "]),
            ]
        },
    }


def run_tests_for_method(module_name: str, ref_cls: Any, att_cls: Any, method_name: str) -> int:
    tests = known_tests().get(module_name, {}).get(method_name, [])
    failures = 0
    ref = ref_cls()
    att = att_cls()

    for (args_kwargs, expected) in tests:
        args, kwargs = args_kwargs
        # Prepare deep copies for in-place tests
        import copy
        args_ref = copy.deepcopy(args)
        kwargs_ref = copy.deepcopy(kwargs)
        args_att = copy.deepcopy(args)
        kwargs_att = copy.deepcopy(kwargs)

        ref_fn = getattr(ref, method_name)
        att_fn = getattr(att, method_name)

        # Compute reference output (not currently used for comparison, but useful for parity)
        ref_out = ref_fn(*args_ref, **kwargs_ref)

        # Preserve a copy of pre-execution args for in-place validation
        pre_args_att = copy.deepcopy(args_att)
        att_out = att_fn(*args_att, **kwargs_att)

        ok: bool
        if callable(expected):
            # For in-place checks we pass (pre_args, post_args)
            ok = expected(pre_args_att, args_att)
        else:
            ok = (att_out == expected)

        if not ok:
            failures += 1
            print(f"FAIL: {module_name}.{method_name}{args} -> expected {expected} got {att_out}")
        else:
            print(f"PASS: {module_name}.{method_name}{args}")

    return failures


def main():
    parser = argparse.ArgumentParser(description="Verify attempt against reference and targeted tests")
    parser.add_argument("--name", required=True, help="Problem name/slug (e.g., 'candies', 'rotate', 'roman.easy')")
    args = parser.parse_args()

    module_name = to_module_name(args.name)
    attempt_path = ATTEMPT_DIR / f"{module_name}.py"
    answer_candidates = [
        ANSWER_DIR / f"{module_name}.py",
    ]

    # also try some aliases
    if module_name == 'candies':
        answer_candidates.append(ANSWER_DIR / "candies.py")
    if module_name == 'lastword_easy':
        answer_candidates.append(ANSWER_DIR / "lastword.easy.py")
    if module_name == 'roman_easy':
        answer_candidates.append(ANSWER_DIR / "roman.easy.py")
    if module_name == 'roman_med':
        answer_candidates.append(ANSWER_DIR / "roman.med.py")
    if module_name == 'text_justification':
        answer_candidates.append(ANSWER_DIR / "text.justification.py")

    answer_path = next((p for p in answer_candidates if p.exists()), None)

    att_mod = load_module_from_path(f"attempt_{module_name}", attempt_path)
    if att_mod is None:
        print(f"Attempt file not found: {attempt_path}")
        return 2
    ans_mod = load_module_from_path(f"answer_{module_name}", answer_path) if answer_path else None
    if ans_mod is None:
        print(f"Reference answer not found for {module_name}. Proceeding with known tests only.")

    att_sol = get_solution_class(att_mod)
    ans_sol = get_solution_class(ans_mod) if ans_mod else None
    if att_sol is None:
        print("No class Solution found in attempt file.")
        return 2

    att_methods = set(get_public_methods(att_sol).keys())
    ref_methods = set(get_public_methods(ans_sol).keys()) if ans_sol else set()
    method_name = None
    if ref_methods:
        inter = att_methods & ref_methods
        if len(inter) == 1:
            method_name = next(iter(inter))
        elif len(ref_methods) == 1 and next(iter(ref_methods)) in att_methods:
            method_name = next(iter(ref_methods))
    if method_name is None and att_methods:
        # Fallback to a single method if unambiguous
        if len(att_methods) == 1:
            method_name = next(iter(att_methods))

    if not method_name:
        print("Could not determine the method to test. Ensure method name matches the reference or there is only one public method in Solution.")
        return 2

    # If multiple variants exist in attempt, try them all: base name and any with base prefix (e.g., name_alt, name_v2)
    candidate_methods = [m for m in att_methods if m == method_name or m.startswith(method_name + "_")]
    if not candidate_methods:
        candidate_methods = [method_name]

    best_failures = None
    best_method = None
    for m in sorted(candidate_methods):
        print(f"\nTesting method variant: {m}")
        failures = run_tests_for_method(module_name, ans_sol if ans_sol else att_sol, att_sol, m)
        if best_failures is None or failures < best_failures:
            best_failures = failures
            best_method = m

    if best_failures:
        print(f"\nBest variant '{best_method}' still has {best_failures} failing case(s).")
        return 1
    print(f"\nAll targeted tests passed using variant '{best_method}'.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


