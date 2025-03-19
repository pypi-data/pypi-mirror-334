import os
import argparse
from pathlib import Path
import glob
import sys

import pandas as pd
from rctgan import Metadata
from rctgan.relational import RCTGAN
import logging

MODEL_NAME = "RCTGAN"

args = argparse.ArgumentParser()
args.add_argument("--dataset-name", type=str, default="rossmann_subsampled")
args.add_argument("--real_data_path", type=str, default="/d/hpc/projects/FRI/mj5835/relsyndgb/data/downloads")
args.add_argument("--synthetic_data_path", type=str, default="/d/hpc/projects/FRI/mj5835/relsyndgb/data/synthetic/")
args.add_argument("--full_sensitivity", type=bool, default=True)
args.add_argument("--retrain", type=bool, default=True)
args.add_argument("--run_id", type=str, default="1")
args = args.parse_args()
dataset_name = args.dataset_name
full_sensitivity = args.full_sensitivity
retrain = args.retrain
real_data_path = args.real_data_path
synthetic_data_path = args.synthetic_data_path
run_id = args.run_id

logger = logging.getLogger(f'{MODEL_NAME}_logger')

# logger.basicConfig(
#     level=logging.DEBUG,  # Set the desired log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     # filename=f"{MODEL_NAME}_{dataset_name}.log",  # Specify the file where logs should be stored
#     stream=sys.stdout,
# )

logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.info(f"START LOGGING...")

os.environ["WANDB_PROJECT"]=f"{MODEL_NAME}_{dataset_name}"

# save your trained model checkpoint to wandb
os.environ["WANDB_LOG_MODEL"]="true"

# turn off watch to log faster
os.environ["WANDB_WATCH"]="false"

# os.environ["WANDB_DISABLED"] = "true"

os.environ["PYTORCH_CUDA_ALLOC_CONF"]= "expandable_segments:True"


logger.info(f"START {MODEL_NAME}...")

# utils
def load_tables(data_path, metadata):
    tables = {}
    for file_name in os.listdir(data_path):
        if not file_name.endswith('.csv'):
            continue
        table_name = file_name.split('.')[0]
        dtypes = {}
        parse_dates = []
        for column, column_info in metadata.to_dict()['tables'][table_name]['fields'].items():
            if column_info['type'] == 'categorical':
                dtypes[column] = 'object'
            elif column_info['type'] == 'boolean':
                dtypes[column] = 'bool'
            elif column_info['type'] == 'datetime':
                parse_dates.append(column)
            # for ids and numerical values let pandas infer the type
        table = pd.read_csv(f'{data_path}/{file_name}', low_memory=False, dtype=dtypes, parse_dates=parse_dates)
        tables[table_name] = table
    return tables

def remove_sdv_columns(tables, metadata, update_metadata=True):
    """
    "_v1" Versions of the relational demo datasets in SDV have some columns that are not present in the original datasets.
    We created this function to remove these columns from the tables and the metadata.
    We have also created the following issue in the SDV repo which adresses this problem: https://github.com/sdv-dev/SDV/issues/1776
    """
    for table_name, table in tables.items():
        for column in table.columns:
            if any(prefix in column for prefix in ['add_numerical', 'nb_rows_in', 'min(', 'max(', 'sum(']):
                table = table.drop(columns = column, axis=1)

                if not update_metadata:
                    continue
                metadata._metadata['tables'][table_name]['fields'].pop(column)

        tables[table_name] = table
    metadata.validate(tables)
    return tables, metadata


def save_tables(tables, path):
    if not os.path.exists(path):
        os.makedirs(path)
    for table_name, table in tables.items():
        table.to_csv(os.path.join(path, f"{table_name}.csv"), index=False)

# GENERATE SYNTHETIC DATA ---------------------------------
logger.debug("Loading real data...")
metadata = Metadata(metadata=str(Path(real_data_path) / f'{dataset_name}/metadata_v0.json'))
real_data = load_tables(Path(real_data_path) / f'{dataset_name}', metadata)
real_data, metadata = remove_sdv_columns(real_data, metadata)
metadata.validate_data(real_data)
logger.debug("Real data loaded")

synthetic_data = {}

model = RCTGAN(metadata=metadata)
logger.info("Fitting model...")
model.fit(real_data)

logger.info("Sampling and saving synthetic data...")
for i in range(3):
    model.seed = i
    synthetic_data = model.sample()
    save_data_path = Path(synthetic_data_path) / dataset_name / MODEL_NAME / run_id / f"sample{i}"
    save_tables(synthetic_data, save_data_path)

# SAVE DATA ---------------------------------
# save_data_path = Path(synthetic_data_path) / dataset_name / MODEL_NAME / run_id
# save_tables(synthetic_data, save_data_path)
logger.info("COMPLETE GENERATION DONE.")