# PDB Last Week
This repository contains a single python file. The file edits a PDB Search API query between two dates to retrieve files from yesterday and the 7 days prior (inclusive). The search query output is then used as the input to check each PDB code and make a nicely formatted output in a second document detailing each uniuqe citation from that period with a link containing a PDB code from that citation. 

The code is easily adaptabile for different PDB Search API queries as well as any date range outide of the retrieved queries. 

**System Requirements:**
Code was run on Windows with Python 3.8.5 and may need additional re-formatting for Linux or MacOS.
**Required Libraries:** 
requests
json
os
difflib

