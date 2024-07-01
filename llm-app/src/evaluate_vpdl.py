import os
import pathlib

import vpdl_chain

from utils.config import Config
from langsmith.evaluation import evaluate, LangChainStringEvaluator
from evaluators.vpdl_evaluators import matched_relations, matched_filters

from langsmith import Client

VIEWS_DIRECTORY = os.path.join(pathlib.Path(__file__).parent.absolute(), "..", "..", "Views_Baseline")
  
def find(name):
    for root, _ , files in os.walk(VIEWS_DIRECTORY):
        if name in files:
            return os.path.join(root, name)
        
def execute_chain_wrapper(input_: dict):
    meta_1_path = find(input_["meta_1_path"])
    meta_2_path = find(input_["meta_2_path"])

    #### LINE TO BE CHANGED FOR EACH PROMPT TYPE####
    prompt_type = "1sCoT"

    response = vpdl_chain.execute_chain(llm, input_["view_description"], meta_1_path, meta_2_path, prompt_type)
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
    dataset_name = "VPDL_FINAL_4"

    # string_distance_evaluator = LangChainStringEvaluator(  
    #         "string_distance",  
    #         config={"distance": "levenshtein", "normalize_score": True},
    #         prepare_data=prepare_data  
    # )
 
    # llm_vpdl_evaluator = LangChainStringEvaluator(  
    #     "labeled_score_string",  
    #     config={  
    #         "criteria": {  
    #             "helpfulness": (  
    #                 """The given input is a view description that should be specified using the VPDL language. 
    #                 Given that, how much effort would someone who knows the domain, the underlying metamodels and the VPDL languange syntax need to make to get the prediction to match the reference? 
    #                 The less effort needed, the higher the score.
    #                 You should consider the VPDL language syntax, the metamodels, and the domain knowledge to evaluate the response, but you can ignore the where part."""   
    #             )  
    #         },
    #         "llm": llm,
    #     },
    #     prepare_data=lambda run, example: {
    #         "prediction": run.outputs["vpdl_draft"],
    #         "reference": example.outputs["vpdl_draft"],
    #         "input": example.inputs["view_description"]}
    # )

    results = evaluate(
        execute_chain_wrapper,
        data=client.list_examples(dataset_name=dataset_name),
        evaluators=[matched_relations,matched_filters],
        experiment_prefix="FinalVPDL",
        num_repetitions=3,
    )
