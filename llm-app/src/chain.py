from operator import itemgetter
import json
import os
import pathlib

from langchain.schema import StrOutputParser
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

from utils.config import Config
from runnables.select import Select
from runnables.join import Join
from runnables.where import Where
from utils.ecore.parser import EcoreParser

from langchain_community.document_loaders import TextLoader

VIEWS_DIRECTORY = os.path.join(pathlib.Path(__file__).parent.absolute(), "..", "..", "Views_Baseline")

def check_if_classes_exists(relations, meta_1_document, meta_2_document):
    r = json.dumps(relations)
    relations_to_check = json.loads(r)
    parser = EcoreParser()
    for relation in relations_to_check:
        classes = list(relation.values())[0]
        metamodel_name_1 = meta_1_document[0].metadata["source"].replace(".txt", ".ecore").replace("PlantUML\\", "")
        class_name_1 = classes[0]
        meta_1_checked = parser.check_ecore_class(metamodel_name_1, class_name_1)

        metamodel_name_2 = meta_2_document[0].metadata["source"].replace(".txt", ".ecore").replace("PlantUML\\", "")
        class_name_2 = classes[1]
        meta_2_checked = parser.check_ecore_class(metamodel_name_2, class_name_2)
        if not meta_1_checked or not meta_2_checked:
            return False
    return True

def execute_chain(llm, user_input, meta_1_path, meta_2_path):

    text_parser = llm | StrOutputParser()
    json_parser = llm | JsonOutputParser()

    meta_1_loader = TextLoader(meta_1_path)
    meta_1 = meta_1_loader.load()

    meta_2_loader = TextLoader(meta_2_path)
    meta_2 = meta_2_loader.load()

    join_runnable = Join()
    join_chain = join_runnable.get_runnable(json_parser)
    cfg = {"tags": join_runnable.get_tags()}

    select_runnable = Select()
    select_chain = select_runnable.get_runnable(json_parser)
    cfg['tags'] += select_runnable.get_tags()

    where_runnable = Where()
    where_chain = where_runnable.get_runnable(text_parser)
    cfg['tags'] += where_runnable.get_tags()

    full_chain = RunnablePassthrough.assign(relations=join_chain) | {
            "meta_1": itemgetter("meta_1"),
            "meta_2": itemgetter("meta_2"),
            "user_input": itemgetter("user_input"),
            "relations": itemgetter("relations"),
            "select": RunnablePassthrough.assign(select=select_chain) } | RunnablePassthrough.assign(combinations=where_chain)

    full_result = full_chain.invoke(
        {
            "user_input": user_input,
            "meta_1": meta_1, 
            "meta_2": meta_2
        },
        config=cfg)

    if check_if_classes_exists(full_result['relations'], meta_1, meta_2):
        print("Classes exists")
    else:  
        print("Classes do not exist")

    print(full_result['relations'])
    print(full_result['select']['select'])
    print(full_result['combinations'])

# Configure everything
config = Config("FULL-CHAIN")
config.load_keys()
llm = config.get_llm()
open_ai_key = config.get_open_ai_key()

for folder in os.listdir(VIEWS_DIRECTORY):
    folder_path = os.path.join(VIEWS_DIRECTORY, folder)
    folder_quantity = 0
    if os.path.isdir(folder_path):
        plant_uml_folder = os.path.join(folder_path, "metamodels", "PlantUML")
        user_input_file = os.path.join(folder_path, "user_input.txt")
        user_input = open(user_input_file, "r").read()
        folder_quantity += 1
        plant_uml_files =[]
        for file in os.listdir(plant_uml_folder):
            if file.endswith(".txt"):
                plant_uml_files.append(os.path.join(plant_uml_folder, file))
                print(os.path.join(plant_uml_folder, file))
                if len(plant_uml_files) == 2:
                    # try:
                    execute_chain(llm, user_input, plant_uml_files[0], plant_uml_files[1])
                    print("Finished processing chain")
                    # except Exception as e:
                    #     print("Error processing chain")
                    #     print(e)
        if folder_quantity >= 1:
            break
