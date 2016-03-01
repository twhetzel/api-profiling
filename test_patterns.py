import json
from pprint import pprint
import re

test_pattern_1 = "9606"
test_pattern_2 = "GO:0000307"


# Build dictionary of MIRIAM Registry entries
def getData():
	with open('data_registry.json') as data_file:
		data = json.load(data_file)
	#pprint(data)
	# find specific entry
	#print data[0]["id"], data[0]["synonyms"]
	return data


# Find entries that match patterns for values in MIRIAM Registry
def findPatternMatches(data):
	# Loop through all dictionary entries
	all_pattern_matches = [] #store all patterns that match API response value
	all_pattern_matche_id_name = {} #dict of ids/names from MIRIAM Registry where API response value matches pattern

	for item in data:
		#print "Id: ", item["id"], item["pattern"]
		p = re.compile(item["pattern"])
		#print p
		# Test if pattern in json matches test pattern
		if p.match(test_pattern_2):
			#print "FOUND MATCH: ", item["id"], item["name"], item["pattern"]
			all_pattern_matches.append(item["pattern"])
			all_pattern_matche_id_name[item["id"]] = item["name"]

	#print "Matching Patterns: ", all_pattern_matches
	print "Matching ID/Name: ", all_pattern_matche_id_name


# Main Program
data = getData()
findPatternMatches(data)

