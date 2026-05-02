import argparse
import yaml
import sys
import re
from pathlib import Path
from typing import Any

# Try to import rich for pretty printing, fallback to standard print if not available
try:
    from rich.console import Console
    from rich.table import Table
    from rich import print as rprint
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

def load_job_data(job_folder):
    """
    Loads metadata and raw intake text for a given job folder.
    Returns a dictionary with searchable fields.
    """
    data = {
        'uuid': None,
        'job_id': job_folder.name,
        'company': 'Unknown',
        'role': 'Unknown',
        'status': 'Unknown',
        'submission_status': 'Unknown',
        'applied_date': 'N/A',
        'metadata_text': '',
        'description': '',
        'path': str(job_folder)
    }

    # 1. Load Metadata
    meta_path = job_folder / "metadata.yaml"
    if meta_path.exists():
        try:
            metadata_text = meta_path.read_text(encoding='utf-8')
            data['metadata_text'] = metadata_text
            meta = yaml.safe_load(metadata_text)
            if not isinstance(meta, dict):
                meta = {}
            if meta:
                data['uuid'] = meta.get('uuid')
                data['company'] = meta.get('company', 'Unknown')
                data['role'] = meta.get('role', 'Unknown')
                data['status'] = meta.get('status', 'Unknown')
                data['submission_status'] = meta.get('submission_status', 'Unknown')
                application = meta.get('application', {}) if isinstance(meta.get('application', {}), dict) else {}
                data['applied_date'] = (
                    application.get('applied_date')
                    or meta.get('apply_date')
                    or meta.get('applied_date')
                    or 'N/A'
                )
        except Exception:
            pass # Keep defaults if read fails

    # 2. Load Raw Intake (Description)
    raw_path = job_folder / "raw" / "raw_intake.md"
    if raw_path.exists():
        try:
            with open(raw_path, 'r', encoding='utf-8') as f:
                data['description'] = f.read()
        except Exception:
            pass

    return data

def parse_field_query(query: str) -> tuple[str | None, str]:
    """
    Supports simple metadata-prefix queries:
    - status: VALUE
    - submission_status: VALUE
    Returns (field_name_or_none, value)
    """
    match = re.match(r'^\s*(status|submission_status)\s*:\s*(.+?)\s*$', query, flags=re.IGNORECASE)
    if not match:
        return None, query.strip()
    return match.group(1).lower(), match.group(2).strip()

def search_jobs(query, jobs_dir):
    """
    Iterates through all jobs and finds matches.
    Returns a list of match objects.
    """
    results: list[dict[str, Any]] = []
    field_query, parsed_value = parse_field_query(query)
    query_lower = parsed_value.lower().strip()
    
    # Iterate over all folders in data/jobs
    # Only look at directories starting with digits (e.g. 00022_...)
    for job_folder in jobs_dir.iterdir():
        if job_folder.is_dir() and re.match(r'^\d{5}_', job_folder.name):
            job_data = load_job_data(job_folder)
            
            # Check for matches
            match_found = False
            fields_matched = []
            score = 0

            # Field-prefixed query mode: only check the specific field.
            if field_query:
                if query_lower in str(job_data.get(field_query, '')).lower():
                    match_found = True
                    fields_matched.append(field_query)
                    score += 10
            else:
                if query_lower and query_lower == job_data['job_id'].lower():
                    match_found = True
                    fields_matched.append("Job ID (exact)")
                    score += 100
                elif query_lower and query_lower in job_data['job_id'].lower():
                    match_found = True
                    fields_matched.append("Job ID")
                    score += 50

                # Check Metadata Fields
                if query_lower and query_lower in str(job_data['company']).lower():
                    match_found = True
                    fields_matched.append("Company")
                    score += 20
                if query_lower and query_lower in str(job_data['role']).lower():
                    match_found = True
                    fields_matched.append("Role")
                    score += 20
                if query_lower and query_lower in str(job_data['status']).lower():
                    match_found = True
                    fields_matched.append("Status")
                    score += 10
                if query_lower and query_lower in str(job_data['submission_status']).lower():
                    match_found = True
                    fields_matched.append("Submission Status")
                    score += 10
                if query_lower and query_lower in str(job_data['applied_date']).lower():
                    match_found = True
                    fields_matched.append("Applied Date")
                    score += 10

                # Check full metadata text
                if query_lower and query_lower in job_data['metadata_text'].lower():
                    match_found = True
                    fields_matched.append("Metadata")
                    score += 5

                # Check Description
                if query_lower and query_lower in job_data['description'].lower():
                    match_found = True
                    fields_matched.append("Description")
                    score += 5

            if match_found:
                results.append({
                    'job_id': job_data['job_id'],
                    'uuid_short': job_data['uuid'][:8] if job_data['uuid'] else "N/A",
                    'company': job_data['company'],
                    'role': job_data['role'],
                    'status': job_data['status'],
                    'submission_status': job_data['submission_status'],
                    'applied_date': job_data['applied_date'],
                    'score': score,
                    'matched_in': ", ".join(fields_matched)
                })

    # Deterministic ranking: best score first, then stable id ordering
    results.sort(key=lambda r: (-r.get('score', 0), r.get('job_id', '')))
    return results

def print_results(results, query):
    """Prints the search results in a table."""
    if not results:
        print(f"\nNo jobs found matching '{query}'.")
        return

    print(f"\nFound {len(results)} jobs matching '{query}':\n")

    if RICH_AVAILABLE:
        console = Console()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Job ID", style="dim", width=12)
        table.add_column("UUID", style="dim", width=10)
        table.add_column("Company", style="cyan", width=20)
        table.add_column("Role", style="green")
        table.add_column("Applied", style="magenta", width=12)
        table.add_column("Status", justify="center")
        table.add_column("Matched In", style="yellow")

        for r in results:
            status_style = "green" if r['status'] == 'ACCEPTED' else "red"
            status_text = f"[{status_style}]{r['status']}[/{status_style}]"
            
            table.add_row(
                r['job_id'],
                r['uuid_short'],
                r['company'],
                r['role'],
                str(r.get('applied_date', 'N/A')),
                status_text,
                r['matched_in']
            )
        console.print(table)
    else:
        # Fallback for standard terminal
        header = f"{'Job ID':<15} | {'UUID':<10} | {'Company':<20} | {'Role':<30} | {'Applied':<12} | {'Status':<10} | {'Matched In'}"
        print(header)
        print("-" * len(header))
        for r in results:
            print(f"{r['job_id']:<15} | {r['uuid_short']:<10} | {r['company']:<20} | {r['role']:<30} | {str(r.get('applied_date', 'N/A')):<12} | {r['status']:<10} | {r['matched_in']}")

def main():
    parser = argparse.ArgumentParser(description="Search job applications by keyword.")
    parser.add_argument("query", help="Text to search for (e.g. 'Python', 'Google')")
    parser.add_argument(
        "--jobs-dir",
        default="data/applied_jobs",
        help="Directory root to search (default: data/applied_jobs)",
    )
    args = parser.parse_args()

    base_dir = Path(args.jobs_dir)
    if not base_dir.exists():
        print(f"❌ Error: {base_dir} does not exist.")
        sys.exit(1)

    results = search_jobs(args.query, base_dir)
    print_results(results, args.query)

if __name__ == "__main__":
    main()
