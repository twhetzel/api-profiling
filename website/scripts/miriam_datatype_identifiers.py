import json
import urllib2


# Get MIRIAM Identifiers for Resources/Datatypes 
def get_miriam_datatypes():
    miriamws = "http://www.ebi.ac.uk/miriamws/main/rest/datatypes/"
    req = urllib2.Request(miriamws, None, {'Accept': 'application/json'})
    f = urllib2.urlopen(req)
    response = f.read()
    f.close()
    # Convert string to object
    data = json.loads(response)
    return data


# Build Resource Name->Identifier dictionary
# from web service response
def build_miriam_identifier_dictionary(miriam_datatype_obj):
    datatype_dict = {}
    # Iterate through object and build dictionary
    for root, value_obj in miriam_datatype_obj.iteritems():
        for k_v_obj in value_obj:
            # Build-up dict with the name, e.g. pir, as Key and
            # Miriam ID as the Value to lookup by the name
            key = k_v_obj['name'].lower()  #lowercase the name in the dictionary
            value = k_v_obj['id']
            datatype_dict[key] = value
    return datatype_dict


# Build dictionary of MIRIAM ID / Name 
def build_miriam_name_dictionary(miriam_datatype_obj):
    miriam_name_dict = {}
    # Iterate through object and build dictionary
    for root, value_obj in miriam_datatype_obj.iteritems():
        for k_v_obj in value_obj:
            # Build-up dict with the ID as Key and
            # resource name as the Value 
            key = k_v_obj['id']
            value = k_v_obj['name']
            miriam_name_dict[key] = value
    return miriam_name_dict


# Build MIRIAM ID / Name Autocomplete data structure
# E.g. [{value: 'MIR:00000001', label: 'Wikipedia'}, {value: 'MIR:0000007', label: 'Some Resource'}]
def build_miriam_autocomplete_data(miriam_datatype_obj):
    #print miriam_datatype_obj
    autocomplete_data = []

    for root, value_obj in miriam_datatype_obj.iteritems():
        for k_v_obj in value_obj:
            autocomplete_obj = {}
            autocomplete_obj['value'] = str(k_v_obj['id'])
            autocomplete_obj['label'] = str(k_v_obj['name'])
            autocomplete_obj['category'] = ''
            autocomplete_data.append(autocomplete_obj)
            print autocomplete_data

    return autocomplete_data


# Main Program
if __name__ == '__main__':
    miriam_datatype_obj = get_miriam_datatypes()
    miriam_datatype_dict = build_miriam_identifier_dictionary(miriam_datatype_obj)
    #print "Test: ", miriam_datatype_dict['Wikidata']

    miriam_autocomplete_data = build_miriam_autocomplete_data(miriam_datatype_obj)
