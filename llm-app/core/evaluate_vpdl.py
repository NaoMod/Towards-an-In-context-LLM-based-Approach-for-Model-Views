import os
import pathlib

import vpdl_chain

from utils.config import Config
from langsmith.evaluation import evaluate, LangChainStringEvaluator
from evaluators.vpdl_evaluators import matched_relations, matched_filters

from langsmith import Client

VIEWS_DIRECTORY = os.path.join(pathlib.Path(__file__).parent.absolute(), "..", "Views_Baseline")
PROMPT_TYPE = "baseline"
EXAMPLES_NO = 1
REPETITIONS = 1
TEMPERATURE = 0
LLM = None
  
def find(name):
    for root, _ , files in os.walk(VIEWS_DIRECTORY):
        if name in files:
            return os.path.join(root, name)
        
def execute_chain_wrapper(input_: dict):
    meta_1_path = find(input_["meta_1_path"])
    meta_2_path = find(input_["meta_2_path"])

    response = vpdl_chain.execute_chain(LLM, input_["view_description"], meta_1_path, meta_2_path, PROMPT_TYPE, EXAMPLES_NO)
    return response

def prepare_data(run, example):
    return {
       "prediction": run.outputs['vpdl_draft'],
       "reference": example.outputs['vpdl_draft']
    }

def execute_evaluation (dataset_name, prompt_type, temperature, examples_no = 1, repetitions = 1):

    global EXAMPLES_NO 
    global REPETITIONS 
    global PROMPT_TYPE
    global TEMPERATURE
    global LLM
    EXAMPLES_NO = examples_no
    REPETITIONS = repetitions
    PROMPT_TYPE = prompt_type
    TEMPERATURE = temperature

    print(f'Executing evaluation for dataset:{dataset_name} for prompt type:{prompt_type} with {examples_no} examples (if applicable) and {repetitions} repetitions. Temperature is: {temperature}')

    # Configure everything
    config = Config()
    config.load_keys()
    LLM = config.get_llm()

    client = Client()
    dataset_name = dataset_name

    string_distance_evaluator = LangChainStringEvaluator(  
            "string_distance",  
            config={"distance": "levenshtein", "normalize_score": True},
            prepare_data=prepare_data  
    )
 
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
            "llm": LLM,
        },
        prepare_data=lambda run, example: {
            "prediction": run.outputs["vpdl_draft"],
            "reference": example.outputs["vpdl_draft"],
            "input": example.inputs["view_description"]}
    )

    results = evaluate(
        execute_chain_wrapper,
        data=client.list_examples(dataset_name=dataset_name),
        evaluators=[string_distance_evaluator,matched_relations,matched_filters,llm_vpdl_evaluator],
        experiment_prefix=PROMPT_TYPE+"_T:"+str(TEMPERATURE)+"_E:"+str(EXAMPLES_NO),
        num_repetitions=REPETITIONS,
    )

    print(results)    

if __name__ == "__main__":

    execute_evaluation("VPDL_FINAL_1", "few-shot-cot", 1, 3)
