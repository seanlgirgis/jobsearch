<#
.SYNOPSIS
Search jobs by keyword with optional applied-site and status filters.

.DESCRIPTION
Searches metadata across data/jobs and data/applied_jobs and prints matching rows.
Each result row starts with Job Title and Company Name.

.PARAMETER q
Required keyword text to search across role/title, company, notes, status, and other metadata fields.

.PARAMETER a
Optional applied-site filter (substring match), such as Dice, LinkedIn, Indeed, or Company Site.

.PARAMETER s
Optional status filter (exact, case-insensitive), such as ACCEPTED, APPLIED, REJECTED, or PENDING.

.EXAMPLE
.\05.job-chatgpt-search.ps1 -q "data engineer"

.EXAMPLE
.\05.job-chatgpt-search.ps1 -q "python" -a "LinkedIn"

.EXAMPLE
.\05.job-chatgpt-search.ps1 -q "aws" -a "Dice" -s "ACCEPTED"

.EXAMPLE
Get-Help .\05.job-chatgpt-search.ps1 -Detailed

.EXAMPLE
Get-Help .\05.job-chatgpt-search.ps1 -Examples
#>

param(
    [Parameter(Mandatory = $true)]
    [string]$q,

    [Parameter(Mandatory = $false)]
    [string]$a = "",

    [Parameter(Mandatory = $false)]
    [string]$s = ""
)

Set-Location $PSScriptRoot
. .\env_setter.ps1

$env:PYTHONIOENCODING = "utf-8"

$py = @'
from pathlib import Path
import yaml
import sys

query = sys.argv[1].strip().lower()
applied_site_filter = (sys.argv[2] if len(sys.argv) > 2 else "").strip().lower()
status_filter = (sys.argv[3] if len(sys.argv) > 3 else "").strip().lower()

roots = [Path("data/jobs"), Path("data/applied_jobs")]
seen = set()
rows = []

def norm_text(value):
    if value is None:
        return ""
    return str(value).strip()

def gather_blob(meta):
    app = meta.get("application") or {}
    parts = [
        norm_text(meta.get("job_id")),
        norm_text(meta.get("role")),
        norm_text(meta.get("title")),
        norm_text(meta.get("company")),
        norm_text(meta.get("location")),
        norm_text(meta.get("status")),
        norm_text(meta.get("notes")),
        norm_text(meta.get("original_filename")),
        norm_text(app.get("applied_method")),
        norm_text(app.get("application_notes")),
    ]
    return "\n".join(parts).lower()

for root in roots:
    if not root.exists():
        continue
    for folder in root.iterdir():
        if not folder.is_dir():
            continue
        meta_path = folder / "metadata.yaml"
        if not meta_path.exists():
            continue

        try:
            meta = yaml.safe_load(meta_path.read_text(encoding="utf-8")) or {}
        except Exception:
            continue

        job_id = norm_text(meta.get("job_id")) or folder.name
        if job_id in seen:
            continue

        app = meta.get("application") or {}
        role = norm_text(meta.get("role")) or norm_text(meta.get("title")) or "Unknown Role"
        company = norm_text(meta.get("company")) or "Unknown Company"
        status = norm_text(meta.get("status")) or "UNKNOWN"
        applied_method = norm_text(app.get("applied_method")) or "N/A"
        applied_date = norm_text(app.get("applied_date")) or "N/A"

        blob = gather_blob(meta)
        if query and query not in blob:
            continue
        if applied_site_filter and applied_site_filter not in applied_method.lower():
            continue
        if status_filter and status_filter != status.lower():
            continue

        rows.append({
            "job_id": job_id,
            "title": role,
            "company": company,
            "status": status,
            "applied_method": applied_method,
            "applied_date": applied_date,
            "root": root.as_posix(),
        })
        seen.add(job_id)

rows.sort(key=lambda x: (x["company"].lower(), x["title"].lower(), x["job_id"]))

print("")
print("=== JOB SEARCH RESULTS ===")
print(f"Query:         {query or '(none)'}")
print(f"Applied Site:  {applied_site_filter or '(any)'}")
print(f"Status:        {status_filter or '(any)'}")
print(f"Matches:       {len(rows)}")
print("")

if rows:
    print("List:")
    for r in rows:
        # Required output shape: job title + company name in the list.
        print(
            f"- {r['title']} | {r['company']} | {r['status']} | "
            f"{r['applied_method']} | {r['applied_date']} | {r['job_id']}"
        )
else:
    print("List:")
    print("- none")
'@

$tempPy = Join-Path $env:TEMP "job_chatgpt_search.py"
Set-Content -LiteralPath $tempPy -Value $py -Encoding utf8
python $tempPy $q $a $s
$exitCode = $LASTEXITCODE
Remove-Item -LiteralPath $tempPy -ErrorAction SilentlyContinue
exit $exitCode
