# API Profiling

## Functionality
Profile web service by finding resource identifiers in web service response from MyGene.info[1]. 

## Dependencies
Python 2.7

## Installation
Get a local copy of the code using any of the GitHub methods.

## How to run
Add API calls to profile in the file `api_calls.json`. 
Run the application as `python profiling.py`

## Output
The main output from the analysis is the file `results_profiling.txt`. This file contains 
a list of the identifiers and whether they were found in Identifiers.org. 
<br>
The file `test-id_frequency_dictionary.txt` contains each unique identifier found from 
profiling the API response across one or more API calls and the count of how often the 
identifier was found in the output from those API calls.
<br>
The file `test-master_identifier_dictionary.txt` contains a unique list of identifiers
from the profiling of the API response across one or more API calls and all of the values
from the API output of the API calls profiled.
<br>
The file `test-all_api_dictionary_file.txt` is a flattened representation of the output
from all API calls profiled and can be used for debugging of future API calls to profile. 
This file contains a key_path and one or more values for the key_path as a result of navigating
the JSON response of the API call to profile. The key_path is a '.' concatenated list
of the identifers found in the JSON output, one entry for each level in the JSON hierarchy. 


[1] http://mygene.info/
