import requests
import json
import os
import platform  # For detecting OS
import sys       # For exiting if OS is unsupported
from datetime import datetime, timedelta

print("Libraries Loaded")

# -------------------------------------------
# Section 1: Detect and Handle Operating System
# -------------------------------------------

# Detect the OS type
os_type = platform.system()

# Normalize and classify
if os_type == 'Darwin':
    detected_os = "MAC OS"
elif os_type == 'Windows':
    detected_os = "Windows"
elif os_type == 'Linux':
    detected_os = "Linux"
else:
    print("Unsupported OS. Exiting.")
    sys.exit(1)

print(f"Operating System Detected: {detected_os}")

# -------------------------------------------
# Section 2: Setup Date Parameters for Search
# -------------------------------------------

# Number of days before yesterday to begin the search
X = 7

# Get yesterday and X days ago
yesterday = datetime.now() - timedelta(days=1)
days_ago = datetime.now() - timedelta(days=1 + X)

End_Date = yesterday.strftime('%Y-%m-%d')
Start_Date = days_ago.strftime('%Y-%m-%d')

# -------------------------------------------
# Section 3: Build Query for PDB API
# -------------------------------------------

query = {
    "query": {
        "type": "group",
        "logical_operator": "and",
        "nodes": [
            {
                "type": "terminal",
                "service": "text",
                "parameters": {
                    "attribute": "rcsb_accession_info.initial_release_date",
                    "operator": "less",
                    "value": End_Date
                }
            },
            {
                "type": "terminal",
                "service": "text",
                "parameters": {
                    "attribute": "rcsb_accession_info.initial_release_date",
                    "operator": "greater_or_equal",
                    "value": Start_Date
                }
            }
        ],
        "label": "text"
    },
    "return_type": "entry",
    "request_options": {
        "paginate": {
            "start": 0,
            "rows": 10000
        },
        "results_content_type": ["experimental"],
        "sort": [{
            "sort_by": "score",
            "direction": "desc"
        }],
        "scoring_strategy": "combined"
    }
}

url = "https://search.rcsb.org/rcsbsearch/v2/query"
headers = {"Content-Type": "application/json"}

print("API Search Initiated")

# -------------------------------------------
# Section 4: Submit Search Request and Save Raw Output
# -------------------------------------------

response = requests.post(url, headers=headers, data=json.dumps(query))

if response.status_code == 200:
    results = response.json()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    raw_output_path = os.path.join(script_dir, f'{Start_Date}_{End_Date}_output.txt')

    with open(raw_output_path, 'w') as file:
        json.dump(results, file, indent=4)

    print(f"Results written to {raw_output_path}")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
    sys.exit(1)

# -------------------------------------------
# Section 5: Read Output and Write Clean Summary
# -------------------------------------------

print("Reading Search Output")

input_file_path = raw_output_path
clean_output_path = os.path.join(script_dir, f'{Start_Date}_{End_Date}_output_Clean.txt')

# Load JSON data
with open(input_file_path, 'r') as file:
    data = json.load(file)

# Extract PDB IDs
pdb_ids = [item['identifier'] for item in data.get('result_set', [])]

# Track unique citations
TITLES = []
COUNT = 0
TITLES_COUNT = 0

print("Accessing PDB Entries...")

# Open clean output file for writing
with open(clean_output_path, 'w') as output_file:
    output_file.write("Code Developed by Jacob Wolfe: https://linktr.ee/jawolfe97?utm_source=linktree_admin_share\n")
    output_file.write("Link to Code Library: https://github.com/jawolfe97/PDB_Last_Week\n")
    output_file.write("-" * 50 + "\n")

    for pdb_id in pdb_ids:
        COUNT += 1
        pdb_url = f"https://data.rcsb.org/rest/v1/core/entry/{pdb_id}"
        response = requests.get(pdb_url)

        if response.status_code == 200:
            entry_data = response.json()
            primary_citation = entry_data.get("rcsb_primary_citation", {}).get("title", "No title available")

            if primary_citation not in TITLES:
                TITLES.append(primary_citation)
                link = f"https://www.rcsb.org/structure/{pdb_id}"
                output_file.write(f"Title: {primary_citation}\n")
                output_file.write(f"Link: {link}\n")
                output_file.write("-" * 50 + "\n")
                TITLES_COUNT += 1
        else:
            output_file.write(f"Failed to retrieve data for PDB ID {pdb_id}\n")
            output_file.write(f"Status code: {response.status_code}\n\n")

        # Show progress every 50 entries
        if COUNT % 50 == 0:
            print(f"{COUNT} / {len(pdb_ids)} PDB entries processed.")

    # -------------------------------------------
    # Write Summary
    # -------------------------------------------
    output_file.write("=" * 7 + "\nSummary\n")
    output_file.write("=" * 7 + "\n")
    output_file.write(f"Total Codes: {len(pdb_ids)}\n")
    output_file.write(f"Individual Citations: {TITLES_COUNT}\n")
    output_file.write(f"Codes Released Between {Start_Date} and {End_Date}\n")
    output_file.write("Disclaimer: Only unique citations recorded for easy reading. This is not a comprehensive list :)\n")

print(f"Filtered results written to {clean_output_path}")
