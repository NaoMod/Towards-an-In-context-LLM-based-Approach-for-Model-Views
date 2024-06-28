import os
import pathlib

import atl_chain

from utils.config import Config
from langsmith.evaluation import evaluate, LangChainStringEvaluator
from evaluators.atl_evaluators import matched_relations

from langsmith import Client

ATL_DIRECTORY = os.path.join(pathlib.Path(__file__).parent.absolute(), "..", "..", "Views_ATL_Baseline")
  
def find(name):
    for root, _ , files in os.walk(ATL_DIRECTORY):
        if name in files:
            return os.path.join(root, name)
        
def execute_chain_wrapper(input_: dict):
    meta_1_path = find(input_["meta_1_path"])
    meta_2_path = find(input_["meta_2_path"])

    #### LINE TO BE CHANGED FOR EACH PROMPT TYPE####
    prompt_type = "zsCoT"

    response = atl_chain.execute_chain(llm, input_["transformation_description"], meta_1_path, meta_2_path, prompt_type)
    return response

def prepare_data(run, example):
    return {
       "prediction": run.outputs['vpdl_draft'],
       "reference": example.outputs['vpdl_draft']
    }

# Configure everything
config = Config()
config.load_keys()
llm = config.get_llm()
open_ai_key = config.get_open_ai_key()

if __name__ == "__main__":
    client = Client()
    dataset_name = "ATL_FINAL_1"

    llm_vpdl_evaluator = LangChainStringEvaluator(  
        "labeled_score_string",  
        config={  
            "criteria": {  
                "helpfulness": (  
                    """The given input is a view description that should be specified using the VPDL language. 
                    Given that, how much effort would someone who knows the domain, the underlying metamodels and the VPDL languange syntax need to make to get the prediction to match the reference? 
                    The less effort needed, the higher the score.
                    You should consider the VPDL language syntax, the metamodels, and the domain knowledge to evaluate the response, but you can ignore the where part."""   
                )  
            },
            "llm": llm,
        },
        prepare_data=lambda run, example: {
            "prediction": run.outputs["vpdl_draft"],
            "reference": example.outputs["vpdl_draft"],
            "input": example.inputs["view_description"]} 
    )

    results = evaluate(
        execute_chain_wrapper,
        data=client.list_examples(dataset_name=dataset_name),
        evaluators=[matched_relations],
        experiment_prefix="testATL",
        num_repetitions=1,
    )
