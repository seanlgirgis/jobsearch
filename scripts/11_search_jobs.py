import argparse
import yaml
import sys
import re
from pathlib import Path

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
        'description': '',
        'path': str(job_folder)
    }

    # 1. Load Metadata
    meta_path = job_folder / "metadata.yaml"
    if meta_path.exists():
        try:
            with open(meta_path, 'r', encoding='utf-8') as f:
                meta = yaml.safe_load(f)
                if meta:
                    data['uuid'] = meta.get('uuid')
                    data['company'] = meta.get('company', 'Unknown')
                    data['role'] = meta.get('role', 'Unknown')
                    data['status'] = meta.get('status', 'Unknown')
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

def search_jobs(query, jobs_dir):
    """
    Iterates through all jobs and finds matches.
    Returns a list of match objects.
    """
    results = []
    query_lower = query.lower()
    
    # Iterate over all folders in data/jobs
    # Only look at directories starting with digits (e.g. 00022_...)
    for job_folder in jobs_dir.iterdir():
        if job_folder.is_dir() and re.match(r'^\d{5}_', job_folder.name):
            job_data = load_job_data(job_folder)
            
            # Check for matches
            match_found = False
            fields_matched = []

            # Check Metadata Fields
            if query_lower in job_data['company'].lower():
                match_found = True
                fields_matched.append("Company")
            if query_lower in job_data['role'].lower():
                match_found = True
                fields_matched.append("Role")
            if query_lower in job_data['status'].lower():
                match_found = True
                fields_matched.append("Status")
            
            # Check Description
            if query_lower in job_data['description'].lower():
                match_found = True
                fields_matched.append("Description")

            if match_found:
                results.append({
                    'job_id': job_data['job_id'],
                    'uuid_short': job_data['uuid'][:8] if job_data['uuid'] else "N/A",
                    'company': job_data['company'],
                    'role': job_data['role'],
                    'status': job_data['status'],
                    'matched_in': ", ".join(fields_matched)
                })

    return results

def print_results(results, query):
    """Prints the search results in a table."""
    if not results:
        print(f"\n❌ No jobs found matching '{query}'.")
        return

    print(f"\n🔍 Found {len(results)} jobs matching '{query}':\n")

    if RICH_AVAILABLE:
        console = Console()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Job ID", style="dim", width=12)
        table.add_column("UUID", style="dim", width=10)
        table.add_column("Company", style="cyan", width=20)
        table.add_column("Role", style="green")
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
                status_text,
                r['matched_in']
            )
        console.print(table)
    else:
        # Fallback for standard terminal
        header = f"{'Job ID':<15} | {'UUID':<10} | {'Company':<20} | {'Role':<30} | {'Status':<10} | {'Matched In'}"
        print(header)
        print("-" * len(header))
        for r in results:
            print(f"{r['job_id']:<15} | {r['uuid_short']:<10} | {r['company']:<20} | {r['role']:<30} | {r['status']:<10} | {r['matched_in']}")

def main():
    parser = argparse.ArgumentParser(description="Search job applications by keyword.")
    parser.add_argument("query", help="Text to search for (e.g. 'Python', 'Google')")
    args = parser.parse_args()

    base_dir = Path("data/jobs")
    if not base_dir.exists():
        print(f"❌ Error: {base_dir} does not exist.")
        sys.exit(1)

    results = search_jobs(args.query, base_dir)
    print_results(results, args.query)

if __name__ == "__main__":
    main()
