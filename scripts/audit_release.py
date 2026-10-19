"""Read-only credential-pattern and Markdown asset checks; never print secret values."""

import json
import os
import re
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parent.parent
pattern = re.compile(
    rb"(?:sk|rk)_(?:live|test)_[A-Za-z0-9]{20,}|whsec_[A-Za-z0-9]{24,}|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{30,}|AKIA[A-Z0-9]{16}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY|postgres(?:ql)?://[^\s:]+:[^\s@]+@(?!localhost|127\.0\.0\.1)"
)
known = [
    os.environ[name].encode()
    for name in ("STRIPE_TEST_KEY", "STRIPE_WEBHOOK_SECRET", "HEROKU_API_KEY")
    if len(os.environ.get(name, "")) > 15
]
findings = []
objects = subprocess.check_output(["git", "rev-list", "--objects", "--all"], cwd=root).splitlines()
count = 0
current_count = 0
for filename in subprocess.check_output(["git", "ls-files", "-z"], cwd=root).split(b"\0"):
    if not filename:
        continue
    path = root / os.fsdecode(filename)
    if not path.is_file():
        continue
    current_count += 1
    data = path.read_bytes().replace(
        b"postgres://sample:private@host/", b"documented-unit-test-example/"
    )
    if pattern.search(data) or any(value in data for value in known):
        findings.append({"file": os.fsdecode(filename), "kind": "current-source-pattern-review"})
for item in objects:
    sha = item.split(b" ", 1)[0].decode()
    kind = subprocess.check_output(["git", "cat-file", "-t", sha], cwd=root).strip()
    if kind != b"blob":
        continue
    count += 1
    data = subprocess.check_output(["git", "cat-file", "blob", sha], cwd=root)
    if pattern.search(data) or any(value in data for value in known):
        # Public disposable CI database credentials are explicitly identified in workflow.
        scrubbed = data.replace(
            b"postgres://skillseat_ci:ci-only-disposable-password@localhost", b"disposable-ci"
        )
        scrubbed = scrubbed.replace(
            b"postgres://sample:private@host/", b"documented-unit-test-example/"
        )
        if pattern.search(scrubbed) or any(value in data for value in known):
            findings.append({"blob": sha, "kind": "credential-pattern-review"})
missing = []
for document in [root / "README.md", *(root / "docs").rglob("*.md")]:
    for link in re.findall(r"\]\(([^)]+)\)", document.read_text(encoding="utf-8")):
        if link.startswith(("https://", "http://", "#", "mailto:")):
            continue
        target = link.split("#")[0]
        if target and not (document.parent / target).exists():
            missing.append({"document": str(document.relative_to(root)), "target": target})
result = {
    "current_tracked_files_scanned": current_count,
    "reachable_blobs_scanned": count,
    "credential_pattern_findings": findings,
    "missing_local_markdown_targets": missing,
    "scope": "Heuristic current tracked-file and reachable-blob scan plus local Markdown checks; not proof of absence of every possible credential.",
}
output = root / "docs/testing/phase4-source-audit.json"
output.write_text(json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps(result, indent=2))
raise SystemExit(1 if findings or missing else 0)
