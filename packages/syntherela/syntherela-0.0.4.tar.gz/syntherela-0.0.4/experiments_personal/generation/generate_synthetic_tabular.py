import os
import argparse
from pathlib import Path

import relsyndgb
from synthcity.plugins import Plugins
from synthcity.benchmark import Benchmarks
from synthcity.plugins.core.constraints import Constraints
from synthcity.plugins.core.dataloader import GenericDataLoader
from relsyndgb.metadata import Metadata
from relsyndgb.data import load_tables, save_tables, remove_sdv_columns
import torch
from sklearn.impute import SimpleImputer
import pandas as pd
import numpy as np

Plugins(categories=["generic", "privacy"]).list()

args = argparse.ArgumentParser()
args.add_argument("--dataset-name", type=str, default="airbnb-simplified_subsampled")
args.add_argument("--real_data_path", type=str, default="/Users/martinjurkovic/Documents/github_projects/relsyndgb/data/downloads")
args.add_argument("--synthetic_data_path", type=str, default="/Users/martinjurkovic/Documents/github_projects/relsyndgb/data/synthetic/")
args.add_argument("--full_sensitivity", type=bool, default=True)
args.add_argument("--retrain", type=bool, default=True)
args.add_argument("--run_id", type=str, default="1")
args = args.parse_args([])
dataset_name = args.dataset_name
full_sensitivity = args.full_sensitivity
retrain = args.retrain
real_data_path = args.real_data_path
synthetic_data_path = args.synthetic_data_path
run_id = args.run_id

MODEL_NAMES = ['bayesian_network', 'ctgan', 'ddpm', 'nflow', 'tvae']

metadata = Metadata().load_from_json(Path(real_data_path) / f'{dataset_name}/metadata.json')
real_data = load_tables(Path(real_data_path) / f'{dataset_name}', metadata)
real_data, metadata = remove_sdv_columns(real_data, metadata, validate=False)
metadata.validate_data(real_data)

for MODEL_NAME in MODEL_NAMES:
    synthetic_data = {}
    for table in real_data.keys():
        X = real_data[table]
        X_orig = X.copy()
        syn_model = Plugins().get(MODEL_NAME)
        syn_model.strict = False

        # check if any column is constant
        constant_columns = X.columns[X.nunique() == 1]
        if len(constant_columns) > 0:
            X = X.drop(columns=constant_columns)


        numeric_columns = X.select_dtypes(include='number').columns
        if len(numeric_columns) > 0:
            imp = SimpleImputer(strategy='mean')
            X[numeric_columns] = pd.DataFrame(imp.fit_transform(X[numeric_columns]), columns=numeric_columns)
        
        syn_model.fit(X)
        synthetic_data[table] = syn_model.generate(len(X))
        synthetic_data[table] = synthetic_data[table].dataframe()

        # append comstant columns
        for column in constant_columns:
            synthetic_data[table][column] = X_orig[column]

    save_data_path = Path(synthetic_data_path) / dataset_name / MODEL_NAME / run_id / 'sample1'
    save_tables(synthetic_data, save_data_path)