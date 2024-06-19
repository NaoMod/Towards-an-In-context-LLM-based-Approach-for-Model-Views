import os
import sys
import pathlib
from langsmith import Client

# Add the directory containing utils to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.config import Config

VIEWS_DIRECTORY = os.path.join(pathlib.Path(__file__).parent.absolute(), "..", "..", "..", "Views_Baseline")

# Configure everything
config = Config()
config.load_keys()
llm = config.get_llm()
open_ai_key = config.get_open_ai_key()

client = Client()
dataset_name = "VPDL_FINAL_FULL"

# Storing inputs in a dataset lets us
# run chains and LLMs over a shared set of examples.
dataset = client.create_dataset(
    dataset_name=dataset_name, description="All VPDL examples with paths and partial outputs",
)

for folder in os.listdir(VIEWS_DIRECTORY):
        folder_path = os.path.join(VIEWS_DIRECTORY, folder)
        if os.path.isdir(folder_path):
            src_folder = os.path.join(folder_path, "src")
            files_in_src = os.listdir(src_folder)
            vpdl_files = [file for file in files_in_src if file.endswith('.vpdl')]
            vpdl_file_path = os.path.join(src_folder, vpdl_files[0])
            with open(vpdl_file_path, 'r') as file:
                vpdl_file_contents = file.read()
            view_description_file = os.path.join(folder_path, "view_description.txt")
            view_description = open(view_description_file, "r").read()
            reference_folder = os.path.join(folder_path, "reference_output")                            
            filter_path = os.path.join(reference_folder, "filter.json")
            with open(filter_path, 'r') as filter_file:
                filter_contents = filter_file.read()
            relations_path = os.path.join(reference_folder, "relations.json")
            with open(relations_path, 'r') as relations_file:
                relations_contents = relations_file.read()
            rules_path = os.path.join(reference_folder, "rules.json")
            with open(rules_path, 'r') as rules_file:
                rules_contents = rules_file.read()
            metamodel_folder = os.path.join(folder_path, "metamodels")
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
                            "view_description": view_description,
                            "meta_1_path": meta_1_path,
                            "meta_2_path": meta_2_path
                        },
                outputs={
                            "join": relations_contents,
                            "select": filter_contents,
                            "where": rules_contents,
                            "vpdl_draft": vpdl_file_contents
                        },
                dataset_id=dataset.id,
            )