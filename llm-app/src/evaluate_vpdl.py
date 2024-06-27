import os
import pathlib

from langchain_core.prompts.prompt import PromptTemplate
from utils.config import Config
from chain import execute_chain
from langsmith.evaluation import evaluate, LangChainStringEvaluator
from evaluators.vpdl_evaluators import matched_relations, matched_filters

from langsmith import Client

VIEWS_DIRECTORY = os.path.join(pathlib.Path(__file__).parent.absolute(), "..", "..", "Views_Baseline")

_PROMPT_TEMPLATE = """[Instruction]
Please act as an impartial judge and evaluate the quality of the response provided by an AI assistant to the user question displayed below. For this evaluation, you should primarily consider the following criteria:
helpfulness: How much effort would someone who knows the domain and the VPDL languange need to make to get the prediction to match the reference? The less effort needed, the higher the score.
[Ground truth]
{{vpdl_example}}
      
Begin your evaluation by providing a short explanation. Be as objective as possible. After providing your explanation, you must rate the response on a scale of 1 to 10 by strictly following this format: "[[rating]]", for example: "Rating: [[5]]".

[Question]
{{view_description}}

[The Start of Assistant's Answer]
{{vpdl_draft}}

[The End of Assistant's Answer]
"""  
  
def find(name):
    for root, _ , files in os.walk(VIEWS_DIRECTORY):
        if name in files:
            return os.path.join(root, name)
        
def execute_chain_wrapper(input_: dict):
    meta_1_path = find(input_["meta_1_path"])
    meta_2_path = find(input_["meta_2_path"])

    response = execute_chain(llm, input_["view_description"], meta_1_path, meta_2_path)
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
    dataset_name = "VPDL_FINAL_OneEX"

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
                    The less effort needed, the higher the score."""   
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
        evaluators=[matched_relations, matched_filters, string_distance_evaluator, llm_vpdl_evaluator],
        experiment_prefix="TestVPDL",
        # num_repetitions=3,
    )
