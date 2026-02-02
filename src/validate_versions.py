#!/usr/bin/env python3
import argparse
import json
import sys
from dataclasses import dataclass
from typing import Dict, List, Tuple

from packaging.specifiers import SpecifierSet
from packaging.version import Version


@dataclass
class CheckResult:
    ok: bool
    message: str


def load_json(path: str) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise SystemExit(f"ERROR: File not found: {path}")
    except json.JSONDecodeError as e:
        raise SystemExit(f"ERROR: Invalid JSON in {path}: {e}")


def get_component_version(versions: Dict[str, str], component: str) -> Version:
    if component not in versions:
        raise SystemExit(f"ERROR: Missing component in versions file: {component}")
    try:
        return Version(str(versions[component]))
    except Exception as e:
        raise SystemExit(f"ERROR: Invalid version for {component}: {versions[component]} ({e})")


def satisfies(version: Version, spec: str) -> bool:
    # spec examples: ">=2.3.0", "<3.0", "==1.7.0"
    try:
        return version in SpecifierSet(spec)
    except Exception as e:
        raise SystemExit(f"ERROR: Invalid specifier '{spec}': {e}")


def evaluate_constraints(
    versions: Dict[str, str],
    constraints: List[dict]
) -> Tuple[List[CheckResult], bool]:
    results: List[CheckResult] = []
    all_ok = True

    for idx, rule in enumerate(constraints, start=1):
        if_clause = rule.get("if", {})
        then_clause = rule.get("then", [])
        reason = rule.get("reason", f"Rule {idx}")

        if_comp = if_clause.get("component")
        if_spec = if_clause.get("version")

        if not if_comp or not if_spec:
            results.append(CheckResult(False, f"[RULE {idx}] Invalid rule: missing 'if.component' or 'if.version'"))
            all_ok = False
            continue

        if_version = get_component_version(versions, if_comp)
        triggered = satisfies(if_version, if_spec)

        if not triggered:
            results.append(CheckResult(True, f"[RULE {idx}] SKIP — {if_comp} {if_version} does not match '{if_spec}'"))
            continue

        # If triggered, all "then" constraints must pass
        rule_ok = True
        failures = []

        for req in then_clause:
            req_comp = req.get("component")
            req_spec = req.get("version")
            if not req_comp or not req_spec:
                rule_ok = False
                failures.append("Invalid 'then' entry (missing component/version)")
                continue

            req_version = get_component_version(versions, req_comp)
            if not satisfies(req_version, req_spec):
                rule_ok = False
                failures.append(f"{req_comp} {req_version} must satisfy '{req_spec}'")

        if rule_ok:
            results.append(CheckResult(True, f"[RULE {idx}] PASS — Triggered: {if_comp} {if_version} matches '{if_spec}'. {reason}"))
        else:
            all_ok = False
            results.append(CheckResult(False, f"[RULE {idx}] FAIL — Triggered: {if_comp} {if_version} matches '{if_spec}'. {reason}. Issues: " + "; ".join(failures)))

    return results, all_ok


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate component versions against compatibility rules."
    )
    parser.add_argument("--versions", default="versions.json", help="Path to versions.json")
    parser.add_argument("--rules", default="rules.json", help="Path to rules.json")
    parser.add_argument("--strict", action="store_true", help="Fail if any rule is invalid")
    args = parser.parse_args()

    versions_data = load_json(args.versions)
    rules_data = load_json(args.rules)

    constraints = rules_data.get("constraints", [])
    if not isinstance(constraints, list):
        print("ERROR: rules.json must contain a list at key 'constraints'.", file=sys.stderr)
        return 2

    results, ok = evaluate_constraints(versions_data, constraints)

    print("\n=== VERSION COMPATIBILITY REPORT ===")
    for r in results:
        status = "OK" if r.ok else "NOT OK"
        print(f"{status}: {r.message}")

    print("===================================")
    if ok:
        print("RESULT: ✅ All triggered compatibility checks passed.")
        return 0

    print("RESULT: ❌ Some compatibility checks failed.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

