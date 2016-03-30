import json
from pprint import pprint
import re
import csv


# Open data input file to test pattern identification
def getInputData():
	input_data_dict = {}
	with open('test-master_identifier_dictionary.txt') as input_file:
		reader = csv.reader(input_file, delimiter='\t')
		for line in reader:
			key = line[0]
			value = str(line[1])[1:-1]
			value = value.split(',').pop(0).strip('\'')
			input_data_dict[key] = value
	return input_data_dict


# Build dictionary of MIRIAM Registry entries
def getPatternData():
	with open('data_registry_MODIFIED2.json') as data_file:
		data = json.load(data_file)
	return data


# Find entries that match patterns for values in MIRIAM Registry
def findPatternMatches(pattern_data, input_data_dict):
	# ids/names from MIRIAM Registry where API response value matches regex pattern
	all_pattern_matches_id_name = {} 

	# Loop through all dictionary entries
	for k,v in input_data_dict.iteritems():
		all_pattern_matches = []
		for item in pattern_data:
			p = re.compile(item["pattern"])
			# Test if pattern in json matches test pattern
			if p.match(v):
				all_pattern_matches.append(item["name"])
				all_pattern_matches_id_name[k] = all_pattern_matches
	return all_pattern_matches_id_name


# Main Program
input_data_dict = getInputData()
pattern_data = getPatternData()
all_pattern_matches_dict = findPatternMatches(pattern_data, input_data_dict)




