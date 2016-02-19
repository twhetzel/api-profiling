import xml.etree.ElementTree as ET
import json

# Convert MIRIAM Datatype Registry into a JSON file containing the
# MIRIAM Identifier, name, synonyms, and patterns

# Read data from local file
registry_data_file = "./registry/IdentifiersOrg-Registry_2016-02.xml"
root = ET.parse(registry_data_file).getroot()

content = []

# Iterate through XML to get elements of interest
for dt in root.findall('{http://www.biomodels.net/MIRIAM/}datatype'):
	name = dt.find('{http://www.biomodels.net/MIRIAM/}name')
	datatype_id = dt.get('id')
	pattern = dt.get('pattern')

	# Account for multiple synonym elements
	syn_values = []
	for synonyms in dt.findall('{http://www.biomodels.net/MIRIAM/}synonyms'):
		for s in synonyms:
			syn_values.append(s.text)
		
	registry_dict = dict(id=datatype_id, name=name.text, pattern=pattern, synonyms=syn_values)

	content.append(registry_dict.copy())

# print to file 
with open('data_registry.json', 'a') as outfile:
	json.dump(content, outfile)



# print value from inner node by attribute name
# for child in root:
# 	for datatype in root.findall(child.tag):
# 		datatype_id = datatype.get('id')
# 		pattern = datatype.get('pattern')
		#print "ID: ", datatype_id, "Pattern: ", pattern

