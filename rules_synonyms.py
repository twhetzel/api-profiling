import json
import urllib2


# Build Identifier->Synonym(s) dictionary
def build_rules_synonym_dictionary():
    with open('rules.json') as data_file:
        data = json.load(data_file)
    
    syn_dict = {}
    # Iterate through list of resources
    for key in data:
        s_key = key["miriam_identifier"]
        s_value_list = key["synonyms"]
        lowercase_s_value_list = [x.lower() for x in s_value_list]
        syn_dict[s_key] = lowercase_s_value_list
    return syn_dict


# Main Program
if __name__ == '__main__':
    rules_synonym_dict = build_rules_synonym_dictionary()
