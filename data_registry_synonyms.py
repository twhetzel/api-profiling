import json
import urllib2


# Build dictionary of ID/Synonyms from ful MIRIAM information

# Build Identifier->Synonym(s) dictionary
def build_miriam_synonym_dictionary():
    with open('data_registry.json') as data_file:
        data = json.load(data_file)
    
    syn_dict = {}
    # Iterate through list of resources
    for key in data:
        s_key = key["id"]
        s_value_list = key["synonyms"]
        lowercase_s_value_list = [x.lower() for x in s_value_list]
        s_name = key["name"].lower()
        # Add name field value also as synonym value(s)
        lowercase_s_value_list.append(s_name)
        syn_dict[s_key] = lowercase_s_value_list
    return syn_dict


# Main Program
if __name__ == '__main__':
    data_registry_synonym_dict = build_miriam_synonym_dictionary()
