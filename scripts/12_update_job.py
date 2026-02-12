"""
scripts/12_update_job.py

🚀 Update Job Application command-line tool.

Features:
- Fuzzy search by Company, Role, Status, or UUID.
- Interactive selection if multiple matches found.
- Updates metadata.yaml (Status, Notes, Follow-up).
- Records history of all changes.

Run with --help for detailed usage and examples.
"""

import argparse
import sys
import yaml
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

# Try to import rich for pretty printing
try:
    from rich.console import Console
    from rich.table import Table
    from rich import print as rprint
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

JOB_ROOT = Path("data/jobs")

def load_job_data(job_folder: Path) -> dict:
    """Loads metadata and raw intake for search context."""
    data = {
        'uuid': None,
        'job_id': job_folder.name,
        'company': 'Unknown',
        'role': 'Unknown',
        'status': 'Unknown',
        'description': '',
        'path': job_folder
    }

    meta_path = job_folder / "metadata.yaml"
    if meta_path.exists():
        try:
            with open(meta_path, 'r', encoding='utf-8') as f:
                meta = yaml.safe_load(f) or {}
                data['uuid'] = meta.get('uuid')
                data['company'] = meta.get('company', 'Unknown')
                data['role'] = meta.get('role', 'Unknown')
                # Prioritize application status, fall back to root status
                app_status = meta.get('application', {}).get('last_status')
                data['status'] = app_status if app_status else meta.get('status', 'Unknown')
        except Exception:
            pass

    return data

def find_matches(queries: List[str]) -> List[dict]:
    """Fuzzy searches for jobs matching ANY of the query terms, summing scores."""
    matches = []
    
    # Parse queries into OR-groups (lists of AND-terms)
    groups = []
    current_group = []
    
    for term in queries:
        if term.upper() == "OR":
            if current_group:
                groups.append(current_group)
                current_group = []
        elif term.upper() == "AND":
            continue # Skip explicit AND, it's implied
        else:
            current_group.append(term)
    if current_group:
        groups.append(current_group)
    
    # Default to single group of all terms if no logic found (backward compatibility-ish, but our logic above handles it)
    if not groups:
       return []

    if not JOB_ROOT.exists():
        return []

    for job_folder in JOB_ROOT.iterdir():
        if job_folder.is_dir() and re.match(r'^\d{5}_', job_folder.name):
            data = load_job_data(job_folder)
            
            best_score = 0
            best_details = []
            is_match = False

            # Check each group (OR logic: match strictly if ANY group matches strictly)
            for group in groups:
                group_score = 0
                group_details = []
                all_terms_in_group_matched = True
                
                # Check each term in the group (AND logic)
                for q in [t.lower() for t in group]:
                    term_matched = False
                    
                    if q in data['company'].lower():
                        group_score += 3
                        group_details.append(f"Company({q})")
                        term_matched = True
                    if q in data['role'].lower():
                        group_score += 3
                        group_details.append(f"Role({q})")
                        term_matched = True
                    if q in data['status'].lower():
                        group_score += 1
                        group_details.append(f"Status({q})")
                        term_matched = True
                    if data['uuid'] and q in data['uuid'].lower():
                        group_score += 10
                        group_details.append("UUID")
                        term_matched = True
                    
                    if not term_matched:
                        all_terms_in_group_matched = False
                        break
                
                # If this group matched fully, consider it for the best score
                if all_terms_in_group_matched and group_score > 0:
                    is_match = True
                    if group_score > best_score:
                        best_score = group_score
                        best_details = group_details

            if is_match:
                data['match_score'] = best_score
                data['matched_because'] = ", ".join(best_details)
                matches.append(data)
    
    # Sort by score descending
    matches.sort(key=lambda x: x['match_score'], reverse=True)
    return matches

def print_history(job_data: dict):
    """Prints the history trail of the job."""
    job_folder = job_data['path']
    meta_path = job_folder / "metadata.yaml"
    
    if not meta_path.exists():
        print(f"❌ Error: metadata.yaml not found in {job_folder}")
        return

    try:
        with open(meta_path, 'r', encoding='utf-8') as f:
            meta = yaml.safe_load(f) or {}
    except Exception as e:
        print(f"❌ Error loading metadata: {e}")
        return

    company = meta.get('company', 'Unknown')
    role = meta.get('role', 'Unknown')
    
    print(f"\n📜 History Trail: {company} - {role}")
    print(f"📁 Path: {job_folder.absolute()}")
    print("=" * 60)
    
    history = meta.get('application', {}).get('history', [])
    # Sort history by date to ensure chronological order
    history.sort(key=lambda x: x.get('date', '0000-00-00'))
    
    if not history:
        print("   (No history recorded)")
    else:
        for event in history:
            date = event.get('date', '????-??-??')
            status = event.get('status', 'INFO')
            notes = event.get('notes', '')
            
            print(f"[{date}] {status}")
            if notes:
                print(f"   └─ {notes}")
            print("-" * 30)
    print("=" * 60 + "\n")

def update_job(job_folder: Path, args):
    """Updates the metadata.yaml for the specific job."""
    meta_path = job_folder / "metadata.yaml"
    if not meta_path.exists():
        print(f"❌ Error: metadata.yaml not found in {job_folder}")
        return

    try:
        with open(meta_path, 'r', encoding='utf-8') as f:
            meta = yaml.safe_load(f) or {}
    except Exception as e:
        print(f"❌ Error loading metadata: {e}")
        return

    today = datetime.now().strftime("%Y-%m-%d")
    if args.date:
        try:
            # Validate format
            datetime.strptime(args.date, "%Y-%m-%d")
            today = args.date
        except ValueError:
            print(f"❌ Error: Invalid date format '{args.date}'. Use YYYY-MM-DD.")
            return

    app_section = meta.setdefault("application", {})
    history = app_section.setdefault("history", [])
    
    updates_made = []

    # 1. Update Status
    if args.status:
        base_status = args.status.strip().upper()
        app_section["last_status"] = base_status
        app_section["last_status_date"] = today
        # Sync root status as well
        meta["status"] = base_status
        
        # Add to history
        history.append({
            "date": today,
            "status": base_status,
            "notes": args.notes or "Status update via script"
        })
        updates_made.append(f"Status -> {base_status}")

    # 2. Update Follow-up
    if args.followup:
        app_section["followup_date"] = args.followup
        updates_made.append(f"Follow-up -> {args.followup}")

    # 3. Add Notes (if not already added via status update)
    if args.notes and not args.status:
        # If just adding a note without status change, append to history with current status
        current_status = app_section.get("last_status", "UNKNOWN")
        history.append({
            "date": today,
            "status": current_status,
            "notes": args.notes
        })
        app_section["application_notes"] = args.notes # Update top-level note too? Optional.
        updates_made.append("Added note")

    if not updates_made:
        print("⚠️ No updates specified. Use --status, --notes, or --follow-up.")
        return

    # Save
    with open(meta_path, 'w', encoding='utf-8') as f:
        yaml.safe_dump(meta, f, sort_keys=False, allow_unicode=True)

    print(f"\n✅ Updated {job_folder.name}")
    for u in updates_made:
        print(f"   - {u}")

def main():
    description = """
🚀 Update Job Application Status & Notes

This script allows you to update matching job applications without needing the exact UUID.
It performs a fuzzy search on Company, Role, Status, and UUID.

✨ FEATURES & EXAMPLES:

  1. SEARCH & VIEW
     # Search for jobs at "Amazon" (lists matches + paths)
     python scripts/12_update_job.py Amazon --search-only

     # View full history trail for "Netflix"
     python scripts/12_update_job.py Netflix --history

     # Complex Search: "Google" OR "Facebook"
     python scripts/12_update_job.py "Google OR Facebook" --search-only

  2. STATUS UPDATES
     # Update status to "INTERVIEW" for "CVS"
     python scripts/12_update_job.py CVS --status INTERVIEW

     # Reject a job by UUID (exact match)
     python scripts/12_update_job.py --uuid 402a89d6 --status REJECTED

  3. NOTES & FOLLOW-UPS
     # Add a note to a "Data Engineer" role
     python scripts/12_update_job.py "Data Engineer" --note "Hiring manager is Alice"

     # Set a follow-up date
     python scripts/12_update_job.py Spotify --followup 2025-01-15

  4. BACKDATING 
     # Record an event that happened in the past
     python scripts/12_update_job.py Oracle --status REJECTED --date 2023-10-01
"""
    
    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="✨ Tips: Use quotes for multi-word queries or notes."
    )
    
    parser.add_argument(
        "query", 
        nargs='*',
        help="Search query. Space='AND'. Use 'OR' for separate groups (e.g. 'CVS Engineer' = CVS AND Engineer; 'Google OR Amazon')."
    )
    
    parser.add_argument(
        "--uuid",
        help="Target a specific job by UUID (full or short). Bypasses text search."
    )
    
    parser.add_argument(
        "--status", 
        help="New status to set (e.g. 'INTERVIEW', 'REJECTED', 'OFFER'). Updates 'last_status'."
    )
    
    parser.add_argument(
        "--notes", "--note", 
        dest="notes",
        help="Add a note to the job history. If status is also provided, this note accompanies the status change."
    )
    
    parser.add_argument(
        "--followup", "--follow-up", 
        dest="followup",
        help="Set the next follow-up date (YYYY-MM-DD)."
    )

    parser.add_argument(
        "--search-only",
        action="store_true",
        help="List matches and exit. Do not prompt for update."
    )
    
    parser.add_argument(
        "--history",
        action="store_true",
        help="Show the full history trail of the job (company, role, events, dates)."
    )
    
    parser.add_argument(
        "--date",
        help="Specify the date for the update (YYYY-MM-DD). Defaults to today."
    )
    
    args = parser.parse_args()

    selected_job = None
    
    # ---------------------------------------------------------
    # Path A: Direct UUID Lookup
    # ---------------------------------------------------------
    if args.uuid:
        print(f"🔎 Looking up UUID: {args.uuid}")
        if not JOB_ROOT.exists():
            print("❌ Job data directory not found.")
            sys.exit(1)
            
        matches = []
        for job_folder in JOB_ROOT.iterdir():
            if job_folder.is_dir():
                # Check folder name first (fast)
                if args.uuid in job_folder.name:
                     matches.append(load_job_data(job_folder))
                     continue
                
                # Check loaded metadata (slower but thorough)
                data = load_job_data(job_folder)
                if data['uuid'] and args.uuid in data['uuid']:
                    matches.append(data)
        
        if not matches:
            print(f"❌ No job found with UUID matching '{args.uuid}'")
            sys.exit(1)
        elif len(matches) > 1:
            print(f"❌ Ambiguous UUID '{args.uuid}'. Matches: {len(matches)} jobs.")
            for m in matches:
                print(f"   - {m['job_id']} ({m['company']} - {m['role']})")
            sys.exit(1)
        else:
            selected_job = matches[0]
            if not args.history: # If history is requested, skip this summary line to avoid clutter
                print(f"✅ Found: {selected_job['company']} - {selected_job['role']} ({selected_job['job_id']})")
                print(f"   Path: {selected_job['path'].absolute()}")
            
    # ---------------------------------------------------------
    # Path B: Fuzzy Search
    # ---------------------------------------------------------
    elif args.query:
        matches = find_matches(args.query)

        if not matches:
            print(f"❌ No jobs found for '{' '.join(args.query)}'")
            sys.exit(1)

        # Print matches logic (refactored slightly to handle search-only)
        if len(matches) == 1 and not args.search_only:
            selected_job = matches[0]
            if not args.history:
                 print(f"🔍 Found 1 match: {selected_job['company']} - {selected_job['role']}")
                 print(f"   Path: {selected_job['path'].absolute()}")
        else:
            # Multiple matches OR search-only mode -> Show table
            print(f"🔍 Found {len(matches)} matches.")
            if RICH_AVAILABLE:
                console = Console()
                table = Table(show_header=True, header_style="bold magenta")
                table.add_column("#", style="dim")
                table.add_column("Company", style="cyan")
                table.add_column("Role", style="green")
                table.add_column("Status")
                table.add_column("Path", style="yellow")
                
                for idx, m in enumerate(matches):
                    table.add_row(str(idx+1), m['company'], m['role'], m['status'], str(m['path'].absolute()))
                console.print(table)
            else:
                for idx, m in enumerate(matches):
                    print(f"{idx+1}. {m['company']} - {m['role']} ({m['status']})")
                    print(f"   Path: {m['path'].absolute()}")
            
            if args.search_only:
                sys.exit(0)

            if sys.stdin.isatty():
                try:
                    action_word = "view history" if args.history else "update"
                    choice = input(f"\nEnter number to {action_word} (or Enter to cancel): ")
                    if choice.isdigit() and 1 <= int(choice) <= len(matches):
                        selected_job = matches[int(choice)-1]
                    else:
                        print("Cancelled.")
                        sys.exit(0)
                except KeyboardInterrupt:
                    sys.exit(0)
            else:
                print("❌ multiple matches found and not running interactively.")
                sys.exit(1)

    # ---------------------------------------------------------
    # No input provided
    # ---------------------------------------------------------
    else:
        parser.print_help()
        sys.exit(1)

    # ---------------------------------------------------------
    # Execute Action
    # ---------------------------------------------------------
    if selected_job:
        if args.history:
            print_history(selected_job)
        else:
            update_job(selected_job['path'], args)
if __name__ == "__main__":
    main()
