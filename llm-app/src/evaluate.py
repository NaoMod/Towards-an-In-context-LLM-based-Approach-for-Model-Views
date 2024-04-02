import os
import pathlib

from langchain.schema import StrOutputParser
from langchain_core.output_parsers import JsonOutputParser

from utils.config import Config
from runnables.select import Select
from runnables.join import Join
from runnables.where import Where

from langchain_community.document_loaders import TextLoader
from langchain.evaluation import ExactMatchStringEvaluator
import langsmith
from langchain.smith import RunEvalConfig
from langsmith.evaluation import EvaluationResult, run_evaluator

VIEWS_DIRECTORY = os.path.join(pathlib.Path(__file__).parent.absolute(), "..", "..", "Views_Baseline")

def find(name):
    for root, _ , files in os.walk(VIEWS_DIRECTORY):
        if name in files:
            return os.path.join(root, name)

def execute_join(input_: dict):

    json_parser = llm | JsonOutputParser()

    meta_1_path = find(input_["meta_1"])

    meta_1_loader = TextLoader(meta_1_path)
    meta_1 = meta_1_loader.load()

    meta_2_path = find(input_["meta_2"])

    meta_2_loader = TextLoader(meta_2_path)
    meta_2 = meta_2_loader.load()

    join_runnable = Join()
    join_chain = join_runnable.get_runnable(json_parser)

    response = join_chain.invoke({
            "user_input": input_["user_input"],
            "meta_1": meta_1, 
            "meta_2": meta_2
    })

    return response

@run_evaluator
def compare_label(run, example) -> EvaluationResult:
    prediction = run.outputs.get("relations") or ""
    target = example.outputs.get("relations") or ""
    match = prediction and prediction == target
    return EvaluationResult(key="matches_label", score=int(match == True))

# Configure everything
config = Config()
config.load_keys()
llm = config.get_llm()
open_ai_key = config.get_open_ai_key()

client = langsmith.Client()
dataset_name = "JOIN_dataset_w_path_2"

eval_config = RunEvalConfig(
    evaluators=["exact_match"],
    custom_evaluators=[compare_label],
)

client.run_on_dataset(
    dataset_name=dataset_name,
    llm_or_chain_factory=execute_join,
    evaluation=eval_config,
    verbose=True,
    project_metadata={"version": "1.0.0", "model": llm},
)

