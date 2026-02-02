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
bash
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
bash
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

## Challenges Faced & How I Resolved Them

### 1. Designing CI-friendly failure behavior
**Challenge:**  
The tool needed to clearly signal success or failure to CI pipelines, not just print messages.

**Solution:**  
Implemented explicit exit codes:
- `0` → All compatibility checks passed
- `1` → One or more compatibility checks failed  

This allows GitHub Actions (and any CI system) to automatically block builds when incompatibilities are detected.

---

### 2. GitHub Actions failing even when the script worked locally
**Challenge:**  
The script ran fine locally, but GitHub Actions showed a failing workflow.

**Solution:**  
Realized this was expected behavior — the script was correctly exiting with code `1` due to a real compatibility violation.  
This confirmed the CI gate was working as intended, not broken.

---

### 3. YAML syntax errors in GitHub Actions
**Challenge:**  
Small indentation and syntax mistakes caused the workflow to be marked as an invalid YAML file.

**Solution:**  
Carefully validated indentation and structure, ensuring:
- Proper spacing
- Correct `run: |` usage
- Correct action versions  

After fixing syntax, the workflow executed reliably.

---

### 4. CI badge showing “failing”
**Challenge:**  
The GitHub Actions badge showed a failing status on the README.

**Solution:**  
Understood that the badge reflects the latest CI run.  
A failing badge correctly indicates that compatibility rules are being enforced — not that the pipeline is broken.

This mirrors real-world CI/CD behavior where intentional failures protect production systems.

