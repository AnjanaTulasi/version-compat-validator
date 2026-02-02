[![CI](https://github.com/AnjanaTulasi/version-compat-validator/actions/workflows/ci.yml/badge.svg)] (https://github.com/AnjanaTulasi/version-compat-validator/actions/workflows/ci.yml)

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

## CI / Automation Friendly Exit Codes

This tool is designed to integrate cleanly with CI/CD pipelines.

| Exit Code | Description |
|---------|-------------|
| `0` | All triggered compatibility checks passed |
| `1` | One or more compatibility checks failed |
| `2` | Configuration or rule validation error |

### Example CI Usage
```bash
python3 src/validate_versions.py
if [ $? -ne 0 ]; then
  echo "Compatibility validation failed"
  exit 1
fi

## CI Behavior

This pipeline is expected to fail when incompatible service versions are detected.

Example:
- API Gateway ≥ 2.3.0 requires Auth Service ≥ 1.7.0
- If this rule is violated, the validator exits with code `1`
- GitHub Actions marks the build as failed to prevent unsafe deployments

This mimics real-world release gating in regulated systems.

