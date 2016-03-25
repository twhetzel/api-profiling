#from __future__ import division
from decimal import *
getcontext().prec = 3
import json
import urllib2

import miriam_datatype_identifiers
import data_registry_synonyms
import rules_synonyms


# Purpose: Profile web service by finding resource identifiers in web
# service responses, e.g. MyGene.info
# Program Flow: 
# (1) Read in file of web service calls to profile
# (2) Make web service call and get response
# (3) Flatten JSON response into a dictionary, with the the dict key as a single value 
# or key path resulting from flattening the JSON response and dict value as a the value(s).
# (4) Use the data from Identifiers.org as a Resource Name/ID mapping dictionary.
# (5) For each key_path from the API web service response, get information about 
# the resource (resource abbreviation and URL) and write the output JSON file. 
# 
# Also collect data to generate table with path, URI, number of occurrences, 
# where occurrence can be reported as multiple columns 
# like: % of match, % of found, and number of found


# Get list of Web service call(s) per Resource to profile
# Used with commandline option only 
def get_calls():
    with open('./data/api_calls.json') as data_file:
        data = json.load(data_file)
    web_service_calls = []
    for key in data:
        web_service_calls.append(key["url"])
        print "** URLS: ", web_service_calls
    return web_service_calls


# Get calls from form input value(s)
def get_calls_from_form(ws_input):
    web_service_calls = []
    web_service_calls.append(ws_input)
    return web_service_calls


# Iterate through web service calls and
# extract key/values and calculate id frequency
def build_api_profile(api_calls):
    # dictionary of all unique key/value pairs across all APIs profiled
    all_api_dictionary = {}

    # dictionary of unique keys and their frequency and count in APIs profiled
    id_frequency_dictionary = {}

    # master identifier dictionary with unique key and all values as a list
    # for all APIs profiled
    master_identifier_dictionary = {}

    api_call_count = 0
    f = open('test-all_api_dictionary_file.txt', 'w')
    f_unique = open('test-id_frequency_dictionary.txt', 'w')
    f_master = open('test-master_identifier_dictionary.txt', 'w')

    # For each web service signature to profile, make call and 
    # get web service response
    for api_call in api_calls:
        api_call_count +=1
        unique_api_identifier_dict = {}
        is_unique_api_identifier = False
        data = json.load(urllib2.urlopen(api_call))

        # Iterate recursively through web service response to get key_path and values
        # key_path is a single value concatenated with all previous parent keys, e.g. go.cc.id
        # value is a single value or a list, a dictionary can not be a final value
        for p, v in iteritems_recursive(data):
            key_path = ''.join(map(str, p))
            # add unique keys and their value to dictionary
            all_api_dictionary[key_path] = v
            # write all_api_dictionary to file
            f.write(str(map(str, p))+"->"+str(v)+"\n")

            # Keep count/percentage of times id is found in APIs profiled
            # but don't count repeating identifiers from the same API output
            if key_path in id_frequency_dictionary:
                # add to new values for existing key in the master_identifier_dictionary
                existing_values = master_identifier_dictionary[key_path.lower()]
                new_values = [str(v)]
                existing_values.extend(new_values)
                master_identifier_dictionary[key_path.lower()] = existing_values

                # Check if this key was seen already for _this_ API call
                if key_path in unique_api_identifier_dict:
                    test = 1 #just some filler for now
                    #print "We've seen this identifier for this API call: ", key_path+"\n"
                else:
                    new_count = id_frequency_dictionary[key_path] +1
                    id_frequency_dictionary[key_path] = new_count
                    is_unique_api_identifier = True
                    unique_api_identifier_dict[key_path] = is_unique_api_identifier
            else:
                found_count = 1
                id_frequency_dictionary[key_path] = found_count

                # Keep track whether this key has been seen for this API response
                is_unique_api_identifier = True
                unique_api_identifier_dict[key_path] = is_unique_api_identifier

                # Add key and value as list into master_identifier_dictionary
                unique_values = [str(v)]
                master_identifier_dictionary[key_path.lower()] = unique_values

    # Write file with identifier frequency
    for k in sorted(id_frequency_dictionary):
        #id_frequency = (id_frequency_dictionary[k]/float(api_call_count) * 100)
        id_frequency = (id_frequency_dictionary[k]/Decimal(api_call_count) * 100)
        f_unique.write(k+"\t"+str(id_frequency_dictionary[k])+"\t"+str(id_frequency)+"% \n")

    # Write file with master dictionary
    for k in sorted(master_identifier_dictionary):
        f_master.write(k+"\t"+str(master_identifier_dictionary[k])+"\n")

    return master_identifier_dictionary


# Get all(recursive) keys and values in JSON Object/Python Dictionary
# Iterate through all dictionaries to generate a key_path with a single 
# value of list of values
# http://stackoverflow.com/questions/15436318/traversing-a-dictionary-recursively
def iteritems_recursive(d):
    for k, v in d.iteritems():
        if isinstance(v, dict):
            for k1, v1 in iteritems_recursive(v):
                k_str = ".".join((k,) + k1),
                if isinstance(v1, list):
                    for item in v1:
                        if isinstance(item, dict):
                            for k2, v2 in item.iteritems():
                                full_k_str = ".".join((k,) + k1 + (k2,)),
                                yield full_k_str, v2
                        else:
                            yield k_str, item
                else:
                    yield k_str, v1
        else:
            if isinstance(v, list):
                for list_item in v:
                    if isinstance(list_item, dict):
                        for k3, v3 in iteritems_recursive(list_item):
                            full_key_str = ".".join((k,) + k3),
                            yield full_key_str, v3
            else:
                yield (k,), v


# Combine synonyms from rules and data_regsitry dictionaries
def combine_dict(rules_dict, data_registry_dict):
    for k,v in rules_dict.iteritems():
        if k in data_registry_dict:
            # If key exists, add new value to list of values
            v.extend(data_registry_dict[k])
            print "New value list: ", v
            # Add new value list back to dict
            data_registry_dict[k] = v
        else:
            # Add key/value(s) to dict
            data_registry_dict[k] = v
    return data_registry_dict


# Check if identifier from web service output is in Identifiers.org/MIRIAM
def get_resource_information(id_dict, miriam_dict):
    annotation_results = {}
    for k in id_dict:
        if k in miriam_dict:
            print "** Identifier %s exists in MIRIAM for resource '%s'"\
                %(miriam_dict[k], k)
            annotation_results[k] = miriam_dict[k]
        else:
            key_path_split = k.split(".")
            for key in key_path_split:
                if key in miriam_dict:
                    annotation_results[key] = miriam_dict[key]
                    print "*-* Identifier %s exists in MIRIAM for resource '%s'"\
                        %(miriam_dict[key], key) +"\n"
                    break
                # else:
                #     print "The identifier '%s' in key_path '%s' does not exist"\
                #         % (key, k)
            #print "The Identifier '%s' does not exist" % k
            #annotation_results[k] = mapped_resource
            # Check for resource name in data type synonyms
            temp_dict = check_syn_dict(k)
            for k,v in temp_dict.iteritems():
                print "TempDict: ",k,v, "\n"
            # Merge dictionaries
            annotation_results.update(temp_dict)
    return annotation_results


# Check for resource name in synonym dictionary (from rules and full MIRIAM registry info)
def check_syn_dict(resource_keypath):
    temp_dict = {}
    # Check for matches for keypath in synonym dict
    print "Checking dict for ", resource_keypath
    for key, value in data_registry_dict.iteritems():
        # Check for resource name in list of synonym values
        if resource_keypath in value:
            print "** Found mapping to synonym ", resource_keypath, key
            # NOTE: identifier could match two MIRIAM IDs based on synonyms, e.g. pharmgkb
            temp_dict[resource_keypath] = key
        else:
            # Check if any values in the keypath match an identifier in Identifiers.org/MIRIAM
            key_path_split = resource_keypath.split(".")
            for key_path_item in key_path_split:
                if key_path_item in value:
                    print "** Found match to part of keypath to synonym ",\
                        resource_keypath, key
                    temp_dict[resource_keypath] = key
                    break
    return temp_dict



# Execute scripts from web page
def main(ws_input):
    # Read in file of web service signature(s) to profile
    #api_calls_to_profile = get_calls()
    
    # Add form input to list
    api_calls_to_profile = get_calls_from_form(ws_input)
    
    # Build dictionary of identifiers and values from WS response(s)
    master_identifier_dict = build_api_profile(api_calls_to_profile)

    # Build dictionary of MIRIAM datatypes
    miriam_datatype_obj = miriam_datatype_identifiers.get_miriam_datatypes()
    miriam_datatype_dict = miriam_datatype_identifiers. \
        build_miriam_identifier_dictionary(miriam_datatype_obj)

    # Build dictionary of hand curated rules
    rules_dict = rules_synonyms.build_rules_synonym_dictionary()
    
    # Build dictionary of MIRIAM synonym datatypes
    global data_registry_dict
    data_registry_dict = data_registry_synonyms.build_miriam_synonym_dictionary()

    # Merge data registry and rules synonym dictionaries w/o wiping out existing synonyms
    combined_synonym_dict = combine_dict(rules_dict, data_registry_dict)

    # Check if identifier in WS response exists in MIRIAM data
    ann_results = get_resource_information(master_identifier_dict, combined_synonym_dict)

    # Return results of profiling
    return ann_results


# Main method
if __name__ == '__main__':
    main()

    # # Read in file of web service signature(s) to profile
    # api_calls_to_profile = get_calls()

    # # Build dictionary of identifiers and values from WS response(s)
    # master_identifier_dict = build_api_profile(api_calls_to_profile)

    # # Build dictionary of MIRIAM datatypes
    # miriam_datatype_obj = miriam_datatype_identifiers.get_miriam_datatypes()
    # miriam_datatype_dict = miriam_datatype_identifiers. \
    #     build_miriam_identifier_dictionary(miriam_datatype_obj)

    # # Check if identifier in WS response exists in MIRIAM data
    # get_resource_information(master_identifier_dict, miriam_datatype_dict)
