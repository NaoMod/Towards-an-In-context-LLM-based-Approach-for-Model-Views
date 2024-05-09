from operator import itemgetter
import json
import os
import pathlib

from langchain_core.runnables import RunnablePassthrough

from utils.config import Config
from runnables.select import Select
from runnables.join import Join
from runnables.where import Where
from utils.ecore.parser import EcoreParser

from langchain_community.document_loaders import TextLoader
from loaders.ecore_loader import EcoreLoader

VIEWS_DIRECTORY = os.path.join(pathlib.Path(__file__).parent.absolute(), "..", "..", "Views_Baseline")

parser = EcoreParser()

def check_if_classes_exist(relations, meta_1, meta_2):
    r = json.dumps(relations)
    relations_to_check = json.loads(r)
    metamodel_name_1 = meta_1[0].metadata["source"].replace(".txt", ".ecore").replace("PlantUML\\", "").replace("1_", "").replace("2_", "")
    metamodel_name_2 = meta_2[0].metadata["source"].replace(".txt", ".ecore").replace("PlantUML\\", "").replace("1_", "").replace("2_", "")
    for relation in relations_to_check:
        classes = list(relation.values())[0]        
        class_name_1 = classes[0]
        meta_1_checked = parser.check_ecore_class(metamodel_name_1, class_name_1)
        
        class_name_2 = classes[1]
        meta_2_checked = parser.check_ecore_class(metamodel_name_2, class_name_2)
        if not meta_1_checked or not meta_2_checked:
            return False
    return True

def check_if_attributtes_exists(select, meta_1, meta_2):
    r = json.dumps(select)
    filters_to_check = json.loads(r)
    metamodel_name_1 = meta_1[0].metadata["source"].replace(".txt", ".ecore").replace("PlantUML\\", "").replace("1_", "").replace("2_", "")
    metamodel_name_2 = meta_2[0].metadata["source"].replace(".txt", ".ecore").replace("PlantUML\\", "").replace("1_", "").replace("2_", "")
    filters_for_meta_1 = filters_to_check[0]
    filters_for_meta_2 = filters_to_check[1]
    for _, filters_1 in filters_for_meta_1.items():
        for class_to_test, attributes in filters_1.items():
            for attr in attributes:
                attr_checked = parser.check_ecore_attribute(metamodel_name_1, class_to_test, attr)
                if not attr_checked:
                    return False

    for _, filters_2 in filters_for_meta_2.items():
        for class_to_test, attributes in filters_2.items():
            for attr in attributes:
                attr_checked = parser.check_ecore_attribute(metamodel_name_2, class_to_test, attr)
                if not attr_checked:
                    return False            
    return True

def check_if_classes_exist_wrapper(input_:dict):
    return check_if_classes_exist(input_['relations'], input_['meta_1'], input_['meta_2'])

def check_if_attributtes_exists_wrapper(input_:dict):
    return check_if_attributtes_exists(input_['select'], input_['meta_1'], input_['meta_2'])

def generate_vpdl_skeleton_wrapper(input_:dict):
    return generate_vpdl_skeleton(input_, input_['meta_1'], input_['meta_2'])

def generate_vpdl_skeleton(input_vpdl, meta_1, meta_2):

    metamodel_name_1 = meta_1[0].metadata["source"].replace(".txt", ".ecore").replace("PlantUML\\", "").replace("1_", "").replace("2_", "")
    metamodel_name_2 = meta_2[0].metadata["source"].replace(".txt", ".ecore").replace("PlantUML\\", "").replace("1_", "").replace("2_", "")

    meta_1_uri, meta_1_prefix = parser.get_metamodel_uri(metamodel_name_1)
    meta_2_uri, meta_2_prefix = parser.get_metamodel_uri(metamodel_name_2)

    vpdl_skeleton = "create view NAME as\n\nselect "
    
    # FILTERS
    if input_vpdl['classes_exist'] != False and input_vpdl['filters_exist'] != False:
        filters_for_meta_1 = input_vpdl['select'][0]
        filters_for_meta_2 = input_vpdl['select'][1]
        for _, filters_1 in filters_for_meta_1.items():
            for class_to_include, attributes in filters_1.items():
                for attr in attributes:
                    vpdl_skeleton += f"{meta_1_prefix}.{class_to_include}.{attr},\n"
        for _, filters_2 in filters_for_meta_2.items():
            for class_to_include, attributes in filters_2.items():
                for attr in attributes:
                    vpdl_skeleton += f"{meta_2_prefix}.{class_to_include}.{attr},\n"
    
    
    # JOIN
    for relation in input_vpdl['relations']:
        classes = list(relation.values())[0]        
        class_name_1 = classes[0]
        class_name_2 = classes[1]

        vpdl_skeleton += f"{meta_1_prefix}.{class_name_1} join {meta_2_prefix}.{class_name_2},\n"
    
    # including the metamodels and its identifiers
    vpdl_skeleton += f"\n\nfrom '{meta_1_uri}' as {meta_1_prefix},\n     {meta_2_uri}' as {meta_2_prefix},\n\nwhere "
    
    # Adding join conditions
    for combination in input_vpdl['combinations']:
        for relation_name, relation_rules in combination.items():
            rules = ""
            for _ , r in relation_rules.items():
                rules += f"{r} and\n      "
            vpdl_skeleton += f"{rules} for {relation_name}\n"
        
    return vpdl_skeleton

def execute_chain(llm, view_description , meta_1_path, meta_2_path):

    # LOADERS
    meta_1_loader = EcoreLoader(meta_1_path)
    meta_1 = meta_1_loader.load()

    meta_2_loader = EcoreLoader(meta_2_path)
    meta_2 = meta_2_loader.load()

    join_runnable = Join(llm)
    join_chain = join_runnable.get_runnable()
    cfg = {"tags": join_runnable.get_tags()}

    select_runnable = Select(llm)
    select_chain = select_runnable.get_runnable()
    cfg['tags'] += select_runnable.get_tags()

    where_runnable = Where(llm)
    where_chain = where_runnable.get_runnable()
    cfg['tags'] += where_runnable.get_tags()

    full_chain = RunnablePassthrough.assign(relations=join_chain) | {
            "meta_1": itemgetter("meta_1"),
            "meta_2": itemgetter("meta_2"),
            "view_description": itemgetter("view_description"),
            "relations": itemgetter("relations"),
            } | RunnablePassthrough.assign(classes_exist=check_if_classes_exist_wrapper) | \
                RunnablePassthrough.assign(select=select_chain) | \
                RunnablePassthrough.assign(filters_exist=check_if_attributtes_exists_wrapper) | \
                RunnablePassthrough.assign(combinations=where_chain) | \
                RunnablePassthrough.assign(vpdl_skeleton=generate_vpdl_skeleton_wrapper)
    

    full_result = full_chain.invoke(
        {
            "view_description": view_description ,
            "meta_1": meta_1, 
            "meta_2": meta_2
        },
        config=cfg)

    print(full_result['relations'])
    print(full_result['select'])
    print(full_result['combinations'])
    print(full_result['classes_exist'])
    print(full_result['filters_exist'])
    print(full_result['vpdl_skeleton'])

# Configure everything
config = Config("FULL-CHAIN")
config.load_keys()
llm = config.get_llm()
open_ai_key = config.get_open_ai_key()

for folder in os.listdir(VIEWS_DIRECTORY):
    folder_path = os.path.join(VIEWS_DIRECTORY, folder)
    folder_quantity = 0
    if os.path.isdir(folder_path):
        metamodels_folder = os.path.join(folder_path, "metamodels")
        view_description_file = os.path.join(folder_path, "view_description.txt")
        view_description = open(view_description_file, "r").read()
        folder_quantity += 1
        ecore_files = []
        for file in os.listdir(metamodels_folder):
            if file.endswith(".ecore"):
                ecore_files.append(os.path.join(metamodels_folder, file))
                print(os.path.join(metamodels_folder, file))
                if len(ecore_files) == 2:
                    try:
                        execute_chain(llm, view_description, ecore_files[0], ecore_files[1])
                        print("Finished processing chain")
                    except Exception as e:
                        print("Error processing chain")
                        print(e)
        # plant_uml_folder = os.path.join(folder_path, "metamodels", "PlantUML")
        # view_description_file = os.path.join(folder_path, "view_description.txt")
        # view_description = open(view_description_file, "r").read()
        # folder_quantity += 1
        # plant_uml_files = []
        # for file in os.listdir(plant_uml_folder):
        #     if file.endswith(".txt"):
        #         plant_uml_files.append(os.path.join(plant_uml_folder, file))
        #         print(os.path.join(plant_uml_folder, file))
        #         if len(plant_uml_files) == 2:
        #             try:
        #                 execute_chain(llm, view_description, plant_uml_files[0], plant_uml_files[1])
        #                 print("Finished processing chain")
        #             except Exception as e:
        #                 print("Error processing chain")
        #                 print(e)
        if folder_quantity >= 1:
            break
