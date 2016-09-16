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

	# Get Resource URI
	for uris in dt.findall('{http://www.biomodels.net/MIRIAM/}uris'):
		for uri in uris:
			url_type = uri.attrib

			# Exclude deprecated URLs
			key_deprecated = "deprecated"
			if key_deprecated in url_type:
				break
			else:
				for k,v in url_type.iteritems():
					if v == "URL":
						url = uri.text

		
	registry_dict = dict(id=datatype_id, name=name.text, pattern=pattern, synonyms=syn_values, url=url)

	content.append(registry_dict.copy())


# print to file 
with open('data_registry-TEST.json', 'a') as outfile:
	json.dump(content, outfile)

