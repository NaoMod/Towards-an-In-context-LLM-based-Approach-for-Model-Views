import os
import pathlib
from langsmith import Client


VIEWS_DIRECTORY = os.path.join(pathlib.Path(__file__).parent.absolute(), "..", "..", "Views_Baseline")

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
            view_description_file = os.path.join(folder_path, "view_description.txt")
            view_description = open(view_description_file, "r").read()
            reference_folder = os.path.join(folder_path, "reference_output")                            
            filter_path = os.path.join(reference_folder, "filter.json")
            with open(filter_path, 'r') as filter_file:
                filter_contents = filter_file.read()
            relations_path = os.path.join(reference_folder, "filter.json")
            with open(relations_path, 'r') as relations_file:
                relations_contents = relations_file.read()
            rules_path = os.path.join(reference_folder, "filter.json")
            with open(rules_path, 'r') as rules_file:
                rules_contents = rules_file.read()
            client.create_example(
                inputs={"question": input_prompt},
                outputs={"answer": output_answer},
                dataset_id=dataset.id,
            )