import os
import json
import argparse

from relsyndgb.metadata import Metadata
from relsyndgb.metadata import convert_metadata_to_v0

def parse_args():
    parser = argparse.ArgumentParser(description='Convert metadata to v0')
    parser.add_argument('--dataset', type=str, help='Dataset name', default = 'all')
    return parser.parse_args()

def convert_metadata_to_old_format(dataset):
    metadata = Metadata().load_from_json(f'../../data/downloads/{dataset}/metadata.json')
    meta_old = convert_metadata_to_v0(metadata)
    with open(f'../../data/downloads/{dataset}/metadata_v0.json', 'w') as f:
        json.dump(meta_old, f, indent=2)


def main():
    args = parse_args()
    dataset = args.dataset
    if dataset == 'all':
        for dataset in os.listdir('../../data/downloads'):
            if os.path.isdir(os.path.join('../../data/downloads', dataset)):
                print(f'Converting {dataset}', end='... ')
                convert_metadata_to_old_format(dataset)
                print('Done!')
    else:
        convert_metadata_to_old_format(dataset)



if __name__ == '__main__':
    main()