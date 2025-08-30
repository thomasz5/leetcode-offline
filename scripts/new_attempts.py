#!/usr/bin/env python3
import argparse
import importlib.util
import inspect
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

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


def infer_public_method_signature(cls: Any) -> Optional[inspect.Signature]:
    methods = [m for n, m in inspect.getmembers(cls, predicate=inspect.isfunction) if not n.startswith('_')]
    if not methods:
        return None
    # Prefer method named 'solve' if present, else first public
    by_name: Dict[str, Any] = {m.__name__: m for m in methods}
    target = by_name.get('solve', None) or methods[0]
    return inspect.signature(target)


def choose_target_method_name(cls: Any) -> str:
    public = [n for n, m in inspect.getmembers(cls, predicate=inspect.isfunction) if not n.startswith('_')]
    if 'solve' in public:
        return 'solve'
    return public[0] if public else 'solve'


def render_attempt_stub(module_name: str, method_name: str, sig: inspect.Signature) -> str:
    # Ensure there is a self param
    params = list(sig.parameters.values())
    if not params or params[0].name != 'self':
        params = [inspect.Parameter('self', inspect.Parameter.POSITIONAL_OR_KEYWORD)] + params
    new_sig = inspect.Signature(parameters=params, return_annotation=sig.return_annotation)

    return (
        "class Solution:\n"
        f"    def {method_name}{new_sig}:\n"
        "        raise NotImplementedError\n"
    )


def create_attempt_from_answer(answer_py: Path, dry_run: bool = False) -> Optional[Path]:
    module_name = to_module_name(answer_py.stem)
    attempt_py = ATTEMPT_DIR / f"{module_name}.py"
    if attempt_py.exists():
        return None

    mod = load_module_from_path(f"answer_{module_name}", answer_py)
    if mod is None:
        return None
    sol = get_solution_class(mod)
    if sol is None:
        return None

    sig = infer_public_method_signature(sol)
    method_name = choose_target_method_name(sol)
    if sig is None:
        # Fallback to a generic signature
        content = (
            "class Solution:\n"
            f"    def {method_name}(self, *args, **kwargs):\n"
            "        raise NotImplementedError\n"
        )
    else:
        content = render_attempt_stub(module_name, method_name, sig)

    if dry_run:
        print(f"Would create: {attempt_py}")
        print(content)
        return attempt_py

    attempt_py.write_text(content, encoding="utf-8")
    return attempt_py


def main():
    parser = argparse.ArgumentParser(description="Generate attempt stubs from existing answers")
    parser.add_argument("--name", help="Specific problem name (matches answer stem)")
    parser.add_argument("--all", action="store_true", help="Generate for all answers without attempt file")
    parser.add_argument("--dry-run", action="store_true", help="Do not write files; print output")
    args = parser.parse_args()

    ATTEMPT_DIR.mkdir(parents=True, exist_ok=True)

    created: List[Path] = []

    if args.name:
        target = to_module_name(args.name)
        candidates = [ANSWER_DIR / f"{target}.py"]
        # also try known dotted variants
        dotted_variants = [
            target.replace('_', '.'),
        ]
        for v in dotted_variants:
            candidates.append(ANSWER_DIR / f"{v}.py")
        answer_path = next((p for p in candidates if p.exists()), None)
        if not answer_path:
            print(f"Answer not found for: {args.name}")
            return 2
        out = create_attempt_from_answer(answer_path, dry_run=args.dry_run)
        if out:
            created.append(out)
    else:
        if not args.all:
            print("Provide --name or --all")
            return 2
        for py in sorted(ANSWER_DIR.glob("*.py")):
            if py.name == "__init__.py":
                continue
            out = create_attempt_from_answer(py, dry_run=args.dry_run)
            if out:
                created.append(out)

    for p in created:
        print(f"Created: {p}")
    if not created:
        print("No attempt files created (all up to date or answers missing)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


