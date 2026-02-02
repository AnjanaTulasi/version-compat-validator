# Version Compatibility Validator (Python)

A lightweight CLI tool that validates software component versions against compatibility rules.

## Why this exists
In system validation and release workflows, mismatched component versions can break integrations.
This tool runs quick compatibility checks before deployment or testing.

## What it does
- Reads component versions from `versions.json`
- Reads compatibility constraints from `rules.json`
- Prints a PASS/FAIL report
- Returns exit codes suitable for CI usage

## Run
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 src/validate_versions.py

