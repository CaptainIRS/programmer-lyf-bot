'''Config Loader'''

import json
from os.path import dirname, realpath


def load_config(file_name: str):
    '''
    Load config file to JSON
    '''
    pwd = dirname(realpath(__file__))

    with open(f'{pwd}/../config/{file_name}') as infile:
        config_file = json.load(infile)

    return config_file
