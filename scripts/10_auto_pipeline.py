#!/usr/bin/env python3
"""
scripts/10_auto_pipeline.py

Orchestrates the entire job application pipeline from intake to tracking.
Runs scripts 01 through 09 in sequence.

Usage:
    python scripts/10_auto_pipeline.py intake/my_job.md --method "LinkedIn"
"""

import argparse
import re
import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import Optional

import os

def run_command(cmd: list[str], capture_output: bool = False) -> str:
    """Run a shell command. Exit on failure. Return stdout if capture_output=True."""
    print(f"\n🚀 Running: {' '.join(cmd)}")
    
    # Enforce UTF-8 for subprocesses to handle emojis/unicode on Windows
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"

    try:
        # If capturing output, we still want to see it in real-time if possible, 
        # but for parsing we need to capture it. 
        # For script 01, we capture to find UUID. For others, we just stream to stdout.
        if capture_output:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True, encoding='utf-8', env=env)
            return result.stdout
        else:
            subprocess.run(cmd, check=True, env=env)
            return ""
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Pipeline failed at step: {' '.join(cmd)}")
        if capture_output and e.stdout:
            print(f"Stdout: {e.stdout}")
        if capture_output and e.stderr:
            print(f"Stderr: {e.stderr}")
        sys.exit(e.returncode)

def extract_uuid(output: str) -> str:
    """Parse '🆔 Job UUID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx' from script 01 output."""
    match = re.search(r"🆔 Job UUID:\s*([a-f0-9\-]+)", output)
    if not match:
        print("❌ Could not find Job UUID in script 01 output.")
        print("Output was:\n", output)
        sys.exit(1)
    return match.group(1).strip()

def main():
    parser = argparse.ArgumentParser(description="Run full job application pipeline (01-09)")
    parser.add_argument("intake_file", nargs="?", help="Path to intake markdown file (optional if --uuid provided)")
    parser.add_argument("--uuid", help="Job UUID to reuse (skips intake/scoring/decision steps)")
    
    # Overrides
    parser.add_argument("--model", default="grok-3", help="LLM model to use")
    parser.add_argument("--version", default="v1", help="Version tag for outputs")
    parser.add_argument("--temperature", default="0.5", help="Temperature for scoring")
    
    # Apply status args
    parser.add_argument("--method", default="Company Website", help="Application method")
    parser.add_argument("--date", default=date.today().isoformat(), help="Application date (YYYY-MM-DD)")
    parser.add_argument("--notes", default="Pipeline application", help="Notes for tracking")
    
    # Flags
    parser.add_argument("--no-move", action="store_true", help="Pass --no-move to script 01")
    
    args = parser.parse_args()
    
    python = sys.executable
    
    # Validation
    if not args.intake_file and not args.uuid:
        parser.error("❌ You must provide either an INTAKE_FILE or --uuid.")
    
    if args.uuid:
        print("="*60)
        print(f"🔄 RESUMING PIPELINE for Job UUID: {args.uuid}")
        print("="*60)
        job_uuid = args.uuid
        
        # If intake file provided, overwrite the raw_intake.md in the job folder
        if args.intake_file:
            # Find the job folder
            jobs_dir = Path("data/jobs")
            job_folder = next((p for p in jobs_dir.iterdir() if p.is_dir() and args.uuid in p.name), None)
            
            if not job_folder:
                print(f"❌ Could not find job folder for UUID {args.uuid}")
                sys.exit(1)
                
            raw_path = job_folder / "raw" / "raw_intake.md"
            print(f"📝 Overwriting {raw_path} with content from {args.intake_file}...")
            
            try:
                # Read new content
                with open(args.intake_file, 'r', encoding='utf-8') as f:
                    new_content = f.read()
                
                # Write to raw path
                raw_path.parent.mkdir(parents=True, exist_ok=True)
                with open(raw_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print("✅ intake file updated.")
            except Exception as e:
                print(f"❌ Failed to update intake file: {e}")
                sys.exit(1)

        # Skip Step 00, 01, 02 which are for creating/scoring new jobs
        
    else:
        print("="*60)
        print(f"🤖 AUTO PIPELINE STARTING for {args.intake_file}")
        print("="*60)

        # --- Step 00: Duplicate Check ---
        print(f"Running Step 00 (Duplicate Check)...")
        run_command([
            python, "scripts/00_check_applied_before.py",
            args.intake_file
        ])

        # --- Step 01: Score ---
        cmd_01 = [
            python, "scripts/01_score_job.py", 
            args.intake_file,
            "--model", args.model,
            "--temperature", args.temperature
        ]
        if args.no_move:
            cmd_01.append("--no-move")
            
        print(f"Running Step 01 (Scoring)...")
        output_01 = run_command(cmd_01, capture_output=True)
        print(output_01) # Show output so user sees score
        
        job_uuid = extract_uuid(output_01)
        print(f"✅ Extracted UUID: {job_uuid}")

        # --- Step 02: Decide (Accept) ---
        run_command([
            python, "-m", "scripts.02_decide_job",
            "--uuid", job_uuid,
            "--accept",
            "--reason", "Auto-accepted by pipeline"
        ])

    # --- Step 03: Tailor ---
    run_command([
        python, "scripts/03_tailor_job_data.py",
        "--uuid", job_uuid,
        "--version", args.version
    ])

    # --- Step 04: Resume Gen ---
    run_command([
        python, "scripts/04_generate_resume_intermediate.py",
        "--uuid", job_uuid,
        "--version", args.version,
        "--model", args.model
    ])

    # --- Step 05: Render Resume ---
    run_command([
        python, "scripts/05_render_resume.py",
        "--uuid", job_uuid,
        "--version", args.version,
        "--all"
    ])
    
    # --- Step 06: Company Research ---
    run_command([
        python, "scripts/06_company_research.py",
        "--uuid", job_uuid,
        "--version", args.version,
        "--model", args.model
    ])

    # --- Step 07: Cover Letter Gen ---
    run_command([
        python, "scripts/07_generate_cover_intermediate.py",
        "--uuid", job_uuid,
        "--model", args.model
    ])
    
    # --- Step 08: Render Cover ---
    run_command([
        python, "scripts/08_render_cover_letter.py",
        "--uuid", job_uuid,
        "--version", args.version
    ])

    # --- Step 09: Update Status (Apply) ---
    run_command([
        python, "scripts/09_update_application_status.py",
        "--uuid", job_uuid,
        "apply",
        "--date", args.date,
        "--method", args.method,
        "--notes", args.notes
    ])



    print("\n" + "="*60)
    print("✅ PIPELINE COMPLETE")
    print(f"Job: {job_uuid}")
    print("="*60)

if __name__ == "__main__":
    main()
