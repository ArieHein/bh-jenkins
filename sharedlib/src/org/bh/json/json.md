# Example usage

filename = 'data.json'
keys = ['value1', 'value2', 'value3']
values = read_json_values(filename, *keys)
for key, value in zip(keys, values):
    print(f'{key}: {value}')
