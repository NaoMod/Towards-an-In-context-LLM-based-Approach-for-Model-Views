import os
import sys
import pathlib
from langsmith import Client

from utils.config import Config

ATL_DIRECTORY = os.path.join(pathlib.Path(__file__).parent.absolute(), "..", "..", "..", "ATL_Baseline")

# Configure everything
config = Config()
config.load_keys()
llm = config.get_llm()

client = Client()
dataset_name = "ATL_FINAL_EVALUATION"

dataset = client.create_dataset(
    dataset_name=dataset_name, description="All transformations with paths and partial outputs",
)

for folder in os.listdir(ATL_DIRECTORY):
    folder_path = os.path.join(ATL_DIRECTORY, folder)
    if os.path.isdir(folder_path):
        metamodel_folder = os.path.join(folder_path, "metamodels")

        atl_files = [file for file in os.listdir(folder_path) if file.endswith('.atl')]
        atl_file_path = os.path.join(folder_path, atl_files[0])
        with open(atl_file_path, 'r') as file:
            atl_file_contents = file.read()

        transformation_description_file = os.path.join(folder_path, "transformation_description.txt")
        # Read the transformation description
        transformation_description = open(transformation_description_file, "r").read()

        relations_file = os.path.join(folder_path, "relations.json")
        # Read the transformation description
        relations = open(relations_file, "r").read()

        # List to hold .ecore files
        ecore_files = []
        for file in os.listdir(metamodel_folder):
            if file.endswith(".ecore"):
                ecore_files.append(file)
                if len(ecore_files) == 2:
                        meta_1_path = ecore_files[0]
                        meta_2_path = ecore_files[1]
                        break
        client.create_example(
            inputs={
                        "transformation_description": transformation_description,
                        "meta_1_path": meta_1_path,
                        "meta_2_path": meta_2_path,
                    },
            outputs={
                        "relations": relations,
                        "atl_file": atl_file_contents
                    },
            dataset_id=dataset.id,
        )
