import yaml
from pprint import pprint

with open('example.yaml') as f:
    python_obj = yaml.safe_load(f.read())
    pprint(python_obj)
    python_obj['configs'][1]['config_data']['users'][0]['password'] = 'Cisc0123'

with open('changed.yaml', 'w') as f:
    yaml.dump(python_obj, f, default_flow_style=False, sort_keys=False, indent=4)
