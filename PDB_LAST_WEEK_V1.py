import requests
import json
import os
from datetime import datetime, timedelta
print(f"Libraries Loaded")
# Define Start_Date as yesterday's date in the proper format
X = 7
yesterday = datetime.now() - timedelta(days=1)
days_ago = datetime.now() - timedelta(days=1+X)

End_Date = yesterday.strftime('%Y-%m-%d')
Start_Date = days_ago.strftime('%Y-%m-%d')

# Define the PDB Search query, with dynamic substitution for Start_Date and End_Date
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
                    "negation": False,
                    "value": End_Date  # Directly using the End_Date variable
                }
            },
            {
                "type": "terminal",
                "service": "text",
                "parameters": {
                    "attribute": "rcsb_accession_info.initial_release_date",
                    "operator": "greater_or_equal",
                    "negation": False,
                    "value": Start_Date  # Directly using the Start_Date variable
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
        "results_content_type": [
            "experimental"
        ],
        "sort": [
            {
                "sort_by": "score",
                "direction": "desc"
            }
        ],
        "scoring_strategy": "combined"
    }
}

# The URL for the PDB Search API
url = "https://search.rcsb.org/rcsbsearch/v2/query"

# Set the headers
headers = {
    "Content-Type": "application/json"
}
print(f"API Search Initiated")
# Send the POST request
response = requests.post(url, headers=headers, data=json.dumps(query))

# Check if the request was successful
if response.status_code == 200:
    # Parse the response JSON
    results = response.json()

    # Get the current directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the file path for output.txt
    output_file_path = os.path.join(script_dir, f'{Start_Date}_{End_Date}_output.txt')

    # Write the results to output.txt
    with open(output_file_path, 'w') as file:
        json.dump(results, file, indent=4)
    
    print(f"Results have been written to {output_file_path}.")
else:
    print(f"Error: {response.status_code}")
    print(response.text)

####Part 2###
print(f"Writing Search Output")
# Define file paths
script_dir = os.path.dirname(os.path.abspath(__file__))
input_file_path = os.path.join(script_dir, f'{Start_Date}_{End_Date}_output.txt')
output_file_path = os.path.join(script_dir, f'{Start_Date}_{End_Date}_output_Clean.txt')

print(f"Writing Reading Output")
# Load the PDB IDs from output.txt
with open(input_file_path, 'r') as file:
    data = json.load(file)

# Extract the list of PDB IDs
pdb_ids = [item['identifier'] for item in data.get('result_set', [])]

# Initialize the list of unique titles
TITLES = []

print(f"Accessing Links")
COUNT = 0
TITLES_COUNT = 0
# Open the output file for writing
with open(output_file_path, 'w') as output_file:
    output_file.write(f"Code Developed by Jacob Wolfe: https://linktr.ee/jawolfe97?utm_source=linktree_admin_share \nLink to Code Library: https://github.com/jawolfe97/PDB_Last_Week\n")
    output_file.write("-" * 50 + "\n")
    # Iterate through each PDB ID
    for pdb_id in pdb_ids:
        COUNT = COUNT + 1
        url = f"https://data.rcsb.org/rest/v1/core/entry/{pdb_id}"
        response = requests.get(url)

        if response.status_code == 200:
            entry_data = response.json()
            title = entry_data.get("struct", {}).get("title", "No title available")
            primary_citation = entry_data.get("rcsb_primary_citation", {}).get("title", "No title available")
            
            if primary_citation not in TITLES:
                TITLES.append(primary_citation)
                link = f"https://www.rcsb.org/structure/{pdb_id}"
                ##output_file.write(f"PDB ID: {pdb_id}\n")
                ##output_file.write(f"Title: {title}\n")
                output_file.write(f"Title: {primary_citation}\n")
                output_file.write(f"Link: {link}\n")
                output_file.write("-" * 50 + "\n")
                TITLES_COUNT = TITLES_COUNT + 1
        else:
            output_file.write(f"Failed to retrieve data for PDB ID {pdb_id}\n")
            output_file.write(f"Status code: {response.status_code}\n\n")
        # Print progress every 50 titles
        if COUNT % 50 == 0:
            print(f"{COUNT} / {len(pdb_ids)}")
# -------------------------------------------
# Write Summary File
# -------------------------------------------
    output_file.write("=" * 7 + "\nSummary\n")
    output_file.write("=" * 7 + "\n")
    output_file.write(f"Total Codes: {len(pdb_ids)}\n")
    output_file.write(f"Individual Citations: {TITLES_COUNT}\n")
    output_file.write(f"Codes Released Between {Start_Date} and {End_Date}\n")
    output_file.write(f"Disclaimer: Only unique citations recorded for easy reading, this is not a comprehensive list :)")
    
print(f"Filtered results written to {output_file_path}")
