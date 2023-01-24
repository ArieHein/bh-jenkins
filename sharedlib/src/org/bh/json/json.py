import json

def read_json_values(filename, *keys):
    with open(filename, 'r') as f:
        data = json.load(f)
        values = []
        for key in keys:
            values.append(data[key])
        return values
