# Imports to enable Python2/3 compatible code
from __future__ import print_function
from future.utils import iteritems

import json
import urllib2

# from future.standard_library import install_aliases
# install_aliases()

# import requests
# import urllib.request
# from future.moves.urllib.parse import urlparse, urlencode
# from future.moves.urllib.request import urlopen, Request
# from future.moves.urllib.error import HTTPError

from collections import deque
from collections import OrderedDict
from operator import itemgetter


# Get MIRIAM Identifiers for Resources/Datatypes 
def get_miriam_datatypes():
    try:
        miriamws = "http://www.ebi.ac.uk/miriamws/main/rest/datatypes/"
        req = urllib.Request(miriamws, None, {'Accept': 'application/json'})
        f = urllib2.urlopen(req)
        response = f.read()
        f.close()
        # Convert string to object
        data = json.loads(response)
        return data
    except urllib.error.HTTPError as err:
        if err.code == 404:
            print('** Get data from local file')
            # Get data from file and return to continue processing
            with open('./data/miriam_datatypes.json') as data_file:
                data = json.load(data_file)
            return data
        # else:
        #     raise


# Build Resource Name->Identifier dictionary
# from web service response
def build_miriam_identifier_dictionary(miriam_datatype_obj):
    datatype_dict = {}
    # Iterate through object and build dictionary
    for (root, value_obj) in iteritems(miriam_datatype_obj):
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
    for (root, value_obj) in iteritems(miriam_datatype_obj):
        for k_v_obj in value_obj:
            # Build-up dict with the ID as Key and
            # resource name as the Value 
            key = k_v_obj['id']
            value = k_v_obj['name']
            miriam_name_dict[key] = value
    # Sort dict for display in autocomplete
    sorted_datatype_dict = OrderedDict(sorted(miriam_name_dict.items(), key=itemgetter(1)))
    #print "SDD:", sorted_datatype_dict
    return sorted_datatype_dict


# Build MIRIAM ID / Name Autocomplete data structure
# From this structure, [{'MIR:00000001': 'Wikipedia'}, {'MIR:0000007': 'Some Resource'}]
# To this e.g. [{value: 'MIR:00000001', label: 'Wikipedia'}, {value: 'MIR:0000007', label: 'Some Resource'}]
def build_miriam_autocomplete_data(miriam_datatype_obj):
    autocomplete_data = []
    # NOTE: Autocomplete data needs to be added into children section 
    # [{'text': 'All Resources', 'children': [{}]}]
    #autocomplete_data_deque = deque()

    for (root, value_obj) in iteritems(miriam_datatype_obj):
        for k_v_obj in value_obj:
            autocomplete_obj = {}
            autocomplete_obj['id'] = str(k_v_obj['id'])
            autocomplete_obj['text'] = str(k_v_obj['name'])
            # autocomplete_obj['category'] = ''
            autocomplete_data.append(autocomplete_obj)
    return autocomplete_data


# Main Program
if __name__ == '__main__':
    miriam_datatype_obj = get_miriam_datatypes()
    
    miriam_datatype_dict = build_miriam_identifier_dictionary(miriam_datatype_obj)

    build_miriam_name_dictionary(miriam_datatype_obj)
    
    miriam_autocomplete_data = build_miriam_autocomplete_data(miriam_datatype_obj)

