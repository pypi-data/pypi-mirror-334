# %%
import os
from dotenv import load_dotenv
from gretel_trainer.relational import *
from gretel_trainer.relational import RelationalData
import pandas as pd
from tqdm import tqdm
from IPython.display import display, HTML
from gretel_trainer.relational import MultiTable
from gretel_client import configure_session
from relsyndgb.metadata import Metadata
from relsyndgb.data import load_tables, save_tables, remove_sdv_columns
from pathlib import Path
import argparse

# %%
# get api key from .env
load_dotenv()

configure_session(api_key=os.environ.get("GRETEL_API_KEY"), validate=True)

DATASET_NAME = "rossmann-store-sales"
METHOD_NAME='gretel'
MODEL_NAME = "GRETEL"

args = argparse.ArgumentParser()
args.add_argument("--dataset-name", type=str, default="rossmann_subsampled")
args.add_argument("--real_data_path", type=str, default="/d/hpc/projects/FRI/mj5835/relsyndgb/data/downloads")
args.add_argument("--synthetic_data_path", type=str, default="/d/hpc/projects/FRI/mj5835/relsyndgb/data/synthetic/")
args.add_argument("--run_id", type=str, default="1")
args = args.parse_args([])
dataset_name = args.dataset_name
real_data_path = args.real_data_path
synthetic_data_path = args.synthetic_data_path
run_id = args.run_id

logger = logging.getLogger(f'{MODEL_NAME}_logger')

logger.debug("Loading real data...")
metadata = Metadata().load_from_json(Path(real_data_path) / f'{dataset_name}/metadata.json')
real_data = load_tables(Path(real_data_path) / f'{dataset_name}', metadata)
real_data, metadata = remove_sdv_columns(real_data, metadata)
metadata.validate_data(real_data)
logger.debug("Real data loaded")

synthetic_data = {}

# %%
# @title
# Alternatively, manually define relational data
# Uncomment code to run

csv_dir = real_data_path
parent_table = (f"store", "Store")
child1_table = (f"historical", "Id")
child1_table_fk = parent_table[1]
tables = [
    # ("table_name", "primary_key")
    parent_table,
    child1_table,
]

foreign_keys = [
    # ("fkey_table.fkey", "pkey_table.pkey")
    (f"{child1_table[0]}.{child1_table_fk}",
        f"{parent_table[0]}.{parent_table[1]}"),
]

relational_data = RelationalData()

# tables_train, tables_test = utils.get_train_test_split(DATASET_NAME, k)

for table, pk in tables:
    relational_data.add_table(
        name=table, primary_key=pk, data=real_data[table])

for fk, ref in foreign_keys:
    relational_data.add_foreign_key(foreign_key=fk, referencing=ref)

# print("\033[1m Source Data: \033[0m")
# source_data = join_tables(parent_table[0], child1_table[0], relational_data=relational_data)

gretel_model = "lstm"
multitable = MultiTable(
    relational_data,
    project_display_name=f"Synthesize {DATASET_NAME} - {gretel_model}",
    gretel_model=gretel_model,
    # refresh_interval=60
)
multitable.train()
multitable.generate(record_size_ratio=1)

table = "store"  # @param {type:"string"}

# source_table = multitable.relational_data.get_table_data(table).head(5)
# synth_table = multitable.synthetic_output_tables[table][source_table.columns].head(
#     5)
# print("\033[1m Source Table:")
# display(source_table)
# print("\n\n\033[1m Synthesized Table:")
# display(synth_table)

synthetic_data = multitable.synthetic_output_tables

logger.info("Saving synthetic data...")
save_data_path = Path(synthetic_data_path) / dataset_name / MODEL_NAME / run_id
save_tables(synthetic_data, save_data_path)
logger.info("COMPLETE GENERATION DONE.")
# utils.save_data(synthetic_data, DATASET_NAME, k, method=METHOD_NAME)

# %%
# METHOD_NAME='gretel'
# synthetic_data = multitable.synthetic_output_tables
# utils.save_data(synthetic_data, DATASET_NAME, k, method=METHOD_NAME)
# %%
