import json
import urllib2

import miriam_datatype_identifiers


# Purpose: Profile web service by finding resource identifiers in web
# service response from MyGene.info.
# Flow: Read in file of web service calls to profile, make web service call,
# flatten JSON response so that all ids (single value or path) and their 
# value can be stored in a web service profile dictionary of ID mappings.
#
# Use the data from Identifiers.org as a Resource Name/ID mapping dictionary.
# For each identifier from MyGene.info web service, get information about 
# the resource (resource abbreviation and URL) and write the output JSON file. 
# Also collect data to generate table with path, URI, number of occurrences, 
# where occurrence can be reported as multiple columns 
# like: % of match, % of found, and number of found


# Get list of Web service call(s) per database to profile
def get_calls():
    with open('api_calls.json') as data_file:
        data = json.load(data_file)
    web_service_calls = []
    for key in data:
        web_service_calls.append(key["url"])
    return web_service_calls


# Iterate through web service calls and
# extract key/values and calculate id frequency
def build_api_profile(api_calls):
    # dictionary of all unique key/value pairs across all APIs profiled
    all_api_dictionary = {}

    # dictionary of unique keys and their frequency/count in APIs profiled
    id_frequency_dictionary = {}

    # master identifier dictionary with unique key and all values as a list for all APIs profiled
    master_identifier_dictionary = {}

    api_call_count = 0
    f = open('test-all_api_dictionary_file.txt', 'w')
    f_unique = open('test-id_frequency_dictionary.txt', 'w')
    f_master = open('test-master_identifier_dictionary.txt', 'w')

    # for each web service signature to profile, make call and get web service response
    for api_call in api_calls_to_profile:
        api_call_count +=1
        unique_api_identifier_dict = {}
        is_unique_api_identifier = False
        data = json.load(urllib2.urlopen(api_call))

        # iterate recursively through web service response to get key/values
        # a key is a single value concatenated with all previous parent keys, e.g. go.cc.id
        # a value is a single value or a list, a dictionary can not be a final value
        for p, v in iteritems_recursive(data):
            key_path = ''.join(map(str, p))
            # add unique keys and their value to dictionary
            all_api_dictionary[key_path] = v
            # write all_api_dictionary to file
            f.write(str(map(str, p))+"->"+str(v)+"\n")

            # keep count/percentage of times id is found in APIs profiled
            # but don't count repeating identifiers from the same API output
            if key_path in id_frequency_dictionary:
                # add to new values for existing key in the master_identifier_dictionary
                existing_values = master_identifier_dictionary[key_path.lower()]
                new_values = [str(v)]
                existing_values.extend(new_values)
                master_identifier_dictionary[key_path.lower()] = existing_values

                # check if this key was seen already for _this_ API call
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

                # keep track whether this key has been seen for this API response
                is_unique_api_identifier = True
                unique_api_identifier_dict[key_path] = is_unique_api_identifier

                # add key and value as list into master_identifier_dictionary
                unique_values = [str(v)]
                master_identifier_dictionary[key_path.lower()] = unique_values

    # write file with identifier frequency
    for k in sorted(id_frequency_dictionary):
        f_unique.write(k+"\t"+str(id_frequency_dictionary[k])+"\n")

    # write file with master dictionary
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


# Check if identifier from web service output is in Identifiers.org/MIRIAM
def get_resource_information(id_dict, miriam_dict):
        for k in id_dict:
            if k in miriam_dict:
                print "** Identifier %s exists in MIRIAM for resource '%s':" %(miriam_dict[k], k)
            else:
                print "The identifier '%s' does not exist" % k


# Main method
if __name__ == '__main__':
    # read in file of web service signature(s) to profile
    api_calls_to_profile = get_calls()

    # build dictionary of identifiers and values from WS response(s)
    master_identifier_dict = build_api_profile(api_calls_to_profile)

    # build dictionary of MIRIAM datatypes
    miriam_datatype_obj = miriam_datatype_identifiers.get_miriam_datatypes()
    miriam_datatype_dict = miriam_datatype_identifiers. \
        build_miriam_identifier_dictionary(miriam_datatype_obj)

    # check if identifier in WS response exists in MIRIAM data
    get_resource_information(master_identifier_dict, miriam_datatype_dict)
