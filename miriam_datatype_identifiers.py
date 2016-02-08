import json
import urllib2


# Get MIRIAM Identifiers for Resources/Datatypes 
def getMiriamDatatypes():
	miriamws = "http://www.ebi.ac.uk/miriamws/main/rest/datatypes/"
	req = urllib2.Request(miriamws, None, {'Accept': 'application/json'})
	f = urllib2.urlopen(req)
	response = f.read()
	f.close()
	# Convert string to object
	data = json.loads(response)
	return data


# Build ID dictionary from WS Response
def buildMiriamIdDict(miriam_datatype_obj):
	datatype_dict = {}
	# Iterate through object and build dictionary
	for root, value_obj in miriam_datatype_obj.iteritems():
		for k_v_obj in value_obj:
			# Build-up dict with the name, e.g. pir, as Key and Miriam ID 
			# as the Value to lookup by the name 
			key = k_v_obj['name']
			value = k_v_obj['id']
			print "Key: ", k_v_obj['name']
			print "Value: ", k_v_obj['id'], "\n"
			datatype_dict[key] = value
	return datatype_dict


# Main Program
if __name__ == '__main__':
	miriam_datatype_obj = getMiriamDatatypes()
	miriam_datatype_dict = buildMiriamIdDict(miriam_datatype_obj)
	print "Test: ",miriam_datatype_dict['Yeast Intron Database v4.3']

