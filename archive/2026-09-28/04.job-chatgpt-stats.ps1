# 04.job-chatgpt-stats.ps1
# Show applied-job stats over trailing N days.
#
# Usage:
#   .\04.job-chatgpt-stats.ps1 -d 1
#   .\04.job-chatgpt-stats.ps1 -d 10

param(
    [Parameter(Mandatory = $true)]
    [ValidateRange(1, 3650)]
    [int]$d
)

Set-Location $PSScriptRoot
. .\env_setter.ps1

$env:PYTHONIOENCODING = "utf-8"

$py = @'
from pathlib import Path
from datetime import datetime, timedelta
import yaml
import sys

days = int(sys.argv[1])
now = datetime.now()
cutoff = now - timedelta(days=days)

roots = [Path("data/jobs"), Path("data/applied_jobs")]

rows = []
timestamp_matches = 0
date_fallback_matches = 0

def parse_timestamp(value):
    if not isinstance(value, str):
        return None
    txt = value.strip()
    if not txt:
        return None
    try:
        dt = datetime.fromisoformat(txt.replace("Z", "+00:00"))
        if dt.tzinfo is not None:
            dt = dt.astimezone().replace(tzinfo=None)
        return dt
    except Exception:
        return None

def parse_date(value):
    if not isinstance(value, str):
        return None
    txt = value.strip()
    if len(txt) < 10:
        return None
    try:
        return datetime.strptime(txt[:10], "%Y-%m-%d").date()
    except Exception:
        return None

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

        app = meta.get("application") or {}
        method = str(app.get("applied_method", "Unknown")).strip() or "Unknown"
        applied_date = str(app.get("applied_date", "")).strip()
        applied_at = app.get("applied_at", meta.get("applied_at"))

        matched = False

        dt = parse_timestamp(applied_at)
        if dt is not None and dt >= cutoff:
            matched = True
            timestamp_matches += 1

        if not matched:
            dd = parse_date(applied_date)
            if dd is not None and dd >= cutoff.date():
                matched = True
                date_fallback_matches += 1

        if matched:
            rows.append({
                "root": root.as_posix(),
                "job_id": folder.name,
                "method": method,
                "applied_date": applied_date or "N/A",
            })

rows.sort(key=lambda x: (x["applied_date"], x["job_id"]))

by_method = {}
for r in rows:
    by_method[r["method"]] = by_method.get(r["method"], 0) + 1

print("")
print(f"=== JOB APPLY STATS (LAST {days} DAY{'S' if days != 1 else ''}) ===")
print(f"Now:            {now.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Window Start:   {cutoff.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Total Applied:  {len(rows)}")
print(f"Timestamp Hits: {timestamp_matches}")
print(f"Date Fallback:  {date_fallback_matches}")
print("")
print("By Method:")
if by_method:
    for k in sorted(by_method.keys()):
        print(f"- {k}: {by_method[k]}")
else:
    print("- none")

print("")
print("Jobs:")
if rows:
    for r in rows:
        print(f"- {r['applied_date']} | {r['method']} | {r['job_id']} | {r['root']}")
else:
    print("- none")
'@

$tempPy = Join-Path $env:TEMP "job_chatgpt_stats_window.py"
Set-Content -LiteralPath $tempPy -Value $py -Encoding utf8
python $tempPy $d
$exitCode = $LASTEXITCODE
Remove-Item -LiteralPath $tempPy -ErrorAction SilentlyContinue
exit $exitCode
