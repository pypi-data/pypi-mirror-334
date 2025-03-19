import os
import argparse
from pathlib import Path
import glob
import sys

import pandas as pd
from realtabformer import REaLTabFormer
import logging
import wandb
from relsyndgb.metadata import Metadata
from relsyndgb.data import load_tables, save_tables, remove_sdv_columns

MODEL_NAME = "REALTABFORMER"
BATCH_SIZE_PARENT = 1024
BATCH_SIZE_CHILD = 1

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


logger.debug("Loading real data...")
metadata = Metadata().load_from_json(Path(real_data_path) / f'{dataset_name}/metadata.json')
real_data = load_tables(Path(real_data_path) / f'{dataset_name}', metadata)
real_data, metadata = remove_sdv_columns(real_data, metadata)
metadata.validate_data(real_data)
logger.debug("Real data loaded")

synthetic_data = {}

# GENERATE SYNTHETIC DATA ---------------------------------


# SAVE DATA ---------------------------------
logger.info("Saving synthetic data...")
save_data_path = Path(synthetic_data_path) / dataset_name / MODEL_NAME / run_id
save_tables(synthetic_data, save_data_path)
logger.info("COMPLETE GENERATION DONE.")