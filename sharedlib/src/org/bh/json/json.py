import json

def read_json_values(filename, *keys):
    """ Read values from a JSON file by keys """
    with open(filename, 'r') as f:
        data = json.load(f)
        values = []
        for key in keys:
            values.append(data[key])
        return values
