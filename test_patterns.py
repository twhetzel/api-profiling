import json
from pprint import pprint
import re
import csv

test_pattern_1 = "9606"
test_pattern_2 = "GO:0000307"


# Open data input file to test pattern identification
def getInputData():
	input_data_dict = {}
	with open('test-master_identifier_dictionary.txt') as input_file:
		reader = csv.reader(input_file, delimiter='\t')
		for line in reader:
			#print "Line:",line
			key = line[0]
			#print "K:",key
			#value = ''.join(line[1]).strip('[]').strip('\'')
			value = str(line[1])[1:-1]
			value = value.split(',').pop(0).strip('\'')
			# print "V:",value
			# print "\n"
			input_data_dict[key] = value
	return input_data_dict


# Build dictionary of MIRIAM Registry entries
def getPatternData():
	with open('data_registry.json') as data_file:
		data = json.load(data_file)
	return data


# Find entries that match patterns for values in MIRIAM Registry
def findPatternMatches(pattern_data, input_data_dict):
	# Loop through all dictionary entries
	#all_pattern_matches = [] #store all patterns that match API response value
	all_pattern_matches_id_name = {} #dict of ids/names from MIRIAM Registry where API response value matches pattern

	for k,v in input_data_dict.iteritems():
		#print "Checking for Key:",k,"with value:",v
		# if k == 'go.cc.id':
		# 	print "Checking for ",k
		all_pattern_matches = []
		for item in pattern_data:
			p = re.compile(item["pattern"])
			# Test if pattern in json matches test pattern
			if p.match(v):
				#all_pattern_matches.append(item["pattern"])
				all_pattern_matches.append(item["name"])
				# if k == 'go.cc.id':
				# 	print "V (",v,") matches:", item["pattern"], item["id"], item["name"]
				# 	print all_pattern_matches
				#all_pattern_matches_id_name[item["id"]] = item["name"]
				all_pattern_matches_id_name[k] = all_pattern_matches
 		#print "Matching ID/Name: ", all_pattern_matches_id_name
 		#print "\n"
	return all_pattern_matches_id_name


# Main Program
input_data_dict = getInputData()  # new

pattern_data = getPatternData()
all_pattern_matches_dict = findPatternMatches(pattern_data, input_data_dict)

#print "GO ID Match: ",all_pattern_matches_dict['go.cc.id']

print "Keypath\tValue\tPossible Values\tNumber of matching patterns\n"
for k,v in all_pattern_matches_dict.iteritems():
	print k,"\t",input_data_dict[k],"\t",v,"\t",len(v),"\n"




