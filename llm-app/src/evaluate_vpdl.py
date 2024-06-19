import os
import pathlib


from utils.config import Config
from chain import execute_chain
from langsmith.evaluation import evaluate
from evaluators.vpdl_evaluators import similarity_check, mock_check


import langsmith
from langchain.smith import RunEvalConfig

VIEWS_DIRECTORY = os.path.join(pathlib.Path(__file__).parent.absolute(), "..", "..", "Views_Baseline")

def find(name):
    for root, _ , files in os.walk(VIEWS_DIRECTORY):
        if name in files:
            return os.path.join(root, name)
        
def execute_chain_wrapper(input_: dict):
    meta_1_path = find(input_["meta_1_path"])
    meta_2_path = find(input_["meta_2_path"])

    response = execute_chain(llm, input_["view_description"], meta_1_path, meta_2_path)
    return response

# Configure everything
config = Config()
config.load_keys()
llm = config.get_llm()
open_ai_key = config.get_open_ai_key()

if __name__ == "__main__":
    client = langsmith.Client()
    dataset_name = "VPDL_FINAL_OneEX"

    results = evaluate(
        execute_chain_wrapper,
        data=client.list_examples(dataset_name=dataset_name),
        evaluators=[similarity_check, mock_check],
        experiment_prefix="Test 1",
    )
