import json
from pprint import pprint
import re
import csv


# Open data input file to test pattern identification
def get_input_data():
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
# Each datatype is an object in the dict incl. name, miriam_id, 
# synonyms and pattern for value
def get_pattern_data():
	with open('./data/data_registry_MODIFIED2.json') as data_file:
		data = json.load(data_file)
	return data


# Find entries that match patterns for values in MIRIAM Registry
def find_pattern_matches(pattern_data, input_data_dict):
	# ids/names from MIRIAM Registry where API response value matches regex pattern
	all_pattern_matches_id_name = {}
	
	# Loop through all dictionary entries
	for k,v in input_data_dict.iteritems():
		all_pattern_matches = []
		for item in pattern_data:
			p = re.compile(item["pattern"])
			# Test if pattern in json matches test pattern
			if p.match(v):
				#all_pattern_matches.append(item["id"])
				#TODO: id should be keypath, but values need to be list of dict 
				# with miriam_id, and name as key/value to display in web site
				miriam_id = str(item["id"])
				name = str(item["name"])
				all_pattern_matches.append({miriam_id:name})
		#print "ALL PM:", all_pattern_matches
				
				all_pattern_matches_id_name[k] = all_pattern_matches
	return all_pattern_matches_id_name


# Build dictionary of All MIRIAM Registry entries
# Each datatype is an object in the dict incl. name, miriam_id, 
# synonyms and pattern for value
def get_all_pattern_data():
	with open('./data/data_registry.json') as data_file:
		all_registry_data = json.load(data_file)
	return all_registry_data

# Generate a pattern dictionary with the MIRIAM ID as the key 
# and the patterns as the value
def make_pattern_dictionary(all_pattern_data):
	all_pattern_dict = {}
	for item in all_pattern_data:
		miriam_id = str(item["id"])
		pattern = str(item["pattern"])
		all_pattern_dict[miriam_id] = pattern
	return all_pattern_dict


# Main Program
if __name__ == '__main__':
	input_data_dict = get_input_data()
	pattern_data = get_pattern_data()
	# all_pattern_matches_dict = findPatternMatches(pattern_data, input_data_dict)
	all_pattern_matches_dict = find_pattern_matches(d1, d2)
