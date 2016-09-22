import json

# Build dictionary of ID/URL from 
# full Identifiers.org resource information

# Build Identifier->URL dictionary
def build_miriam_url_dictionary():
    with open('./data/data_registry.json') as data_file:
        data = json.load(data_file)
    
    url_dict = {}
    # Iterate through list of resources
    for key in data:
        url_key = key["id"]
        url_value = key["url"]
        url_dict[url_key] = url_value
    return url_dict


# Main Program
if __name__ == '__main__':
    data_registry_url_dict = build_miriam_url_dictionary()

