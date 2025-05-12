# PDB Last Week
This repository contains a single python file. The file edits a PDB Search API query between two dates to retrieve files from yesterday and the 7 days prior (inclusive). The search query output is then used as the input to check each PDB code and make a nicely formatted output in a second document detailing each uniuqe citation from that period with a link containing a PDB code from that citation. 

The code is easily adaptabile for different PDB Search API queries as well as any date range outide of the retrieved queries. 

**System Requirements:**  

Code was written with a lot of assistance from ChatGPT and the PDB API. It was designed to be compatible with MAC, Windows, and Linux but was only tested on Windows with Python 3.8.5 and run through the Python Shell. This and may need additional re-formatting for Linux or MacOS.  

**Required Python Libraries:**    
requests  
json  
os  
platform  
sys
