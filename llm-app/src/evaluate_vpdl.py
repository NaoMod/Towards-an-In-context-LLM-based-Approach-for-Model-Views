import os
import pathlib


from utils.config import Config
from chain import execute_chain
from evaluators.vpdl_evaluator import VpdlEvaluator


import langsmith
from langchain.smith import RunEvalConfig

VIEWS_DIRECTORY = os.path.join(pathlib.Path(__file__).parent.absolute(), "..", "..", "Views_Baseline")

def find(name):
    for root, _ , files in os.walk(VIEWS_DIRECTORY):
        if name in files:
            return os.path.join(root, name)



# Configure everything
config = Config()
config.load_keys()
llm = config.get_llm()
open_ai_key = config.get_open_ai_key()

def execute_chain_wrapper(input_: dict):
    meta_1_path = find(input_["meta_1"])
    meta_2_path = find(input_["meta_2"])

    response = execute_chain(llm, input_["view_description"], meta_1_path, meta_2_path)
    return response

if __name__ == "__main__":
    client = langsmith.Client()
    dataset_name = "VPDL_FINAL_OneEX"

    eval_config = RunEvalConfig(
        evaluators=["exact_match"],
        custom_evaluators=[VpdlEvaluator()],
    )

    client.run_on_dataset(
        dataset_name=dataset_name,
        llm_or_chain_factory=execute_chain_wrapper,
        evaluation=eval_config,
        verbose=True,
        project_metadata={"version": "1.0.0", "model": llm},
    )
