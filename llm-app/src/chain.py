from operator import itemgetter
import os
import pathlib

from langchain_core.runnables import RunnablePassthrough

from utils.config import Config
from runnables.views.select import Select
from runnables.views.join import Join
from runnables.views.where import Where

from utils.ecore.parser import EcoreParser

from loaders.ecore_loader import EcoreLoader

VIEWS_DIRECTORY = os.path.join(pathlib.Path(__file__).parent.absolute(), "..", "..", "Views_Baseline")

ecore_parser = EcoreParser()

def generate_vpdl_skeleton_wrapper(input_:dict):
    return generate_vpdl_skeleton(input_, input_['meta_1_path'], input_['meta_2_path'])

def generate_vpdl_skeleton(input_vpdl, meta_1, meta_2):

    meta_1_uri, meta_1_prefix = ecore_parser.get_metamodel_uri(meta_1)
    meta_2_uri, meta_2_prefix = ecore_parser.get_metamodel_uri(meta_2)

    vpdl_skeleton = "create view NAME as\n\nselect "
    
    # FILTERS (SELECT clause)
    for filter_per_relation in input_vpdl['select']['filters']:

        # relation_name = filter_per_relation['name'] # not used
        class_attributes = filter_per_relation['classAttributes']
        for class_to_include, attributes in class_attributes.items():
            for attr in attributes:
                vpdl_skeleton += f"{meta_1_prefix}.{class_to_include}.{attr},\n"
    
    # JOIN
    for relation in input_vpdl['join']['relations']:
                   
        class_name_1 = relation['classes'][0]
        class_name_2 = relation['classes'][0]
    
        vpdl_skeleton += f"{meta_1_prefix}.{class_name_1}, {meta_2_prefix}.{class_name_2} as {relation['name']},\n"
    
    # including the metamodels and its identifiers
    vpdl_skeleton += f"\n\nfrom '{meta_1_uri}' as {meta_1_prefix},\n     {meta_2_uri}' as {meta_2_prefix},\n\nwhere "
    
    # Adding join conditions (WHERE clause)
    for combination in input_vpdl['where']['rules']:
        relation_name = combination['name']
        combination_rules_list = combination['rules']
        rules = ""        
        for rule in combination_rules_list:            
            rules += f"{rule['metaclass_1']}, {rule['combination_rule']}, {rule['metaclass_2']} \n      "
        vpdl_skeleton += f"{rules} for {relation_name}\n"
        
    return vpdl_skeleton

def execute_chain(llm, view_description , meta_1_path, meta_2_path):

    # LOADERS
    meta_1_loader = EcoreLoader(meta_1_path)    
    meta_1 = meta_1_loader.load()
    meta_1_content = meta_1[0].page_content

    meta_2_loader = EcoreLoader(meta_2_path)
    meta_2 = meta_2_loader.load()
    meta_2_content = meta_2[0].page_content

    join_runnable = Join()
    join_runnable.set_model(llm)
    join_runnable.set_parser(meta_1=meta_1_path, meta_2=meta_2_path)
    join_runnable.set_prompt()
    join_chain = join_runnable.get_runnable()
    cfg = {"tags": join_runnable.get_tags()}

    select_runnable = Select()
    select_runnable.set_model(llm)
    select_runnable.set_parser(meta_1=meta_1_path, meta_2=meta_2_path)
    select_runnable.set_prompt()
    select_chain = select_runnable.get_runnable()
    cfg['tags'] += select_runnable.get_tags()

    where_runnable = Where()
    where_runnable.set_model(llm)
    where_runnable.set_parser()
    where_runnable.set_prompt()
    where_chain = where_runnable.get_runnable()
    cfg['tags'] += where_runnable.get_tags()

    full_chain = RunnablePassthrough.assign(join=join_chain).with_config({"run_name": "JOIN"}) | {
            "meta_1": itemgetter("meta_1"),
            "meta_2": itemgetter("meta_2"),
            "meta_1_path": itemgetter("meta_1_path"),
            "meta_2_path": itemgetter("meta_2_path"),
            "view_description": itemgetter("view_description"),
            "join": itemgetter("join"),
            } | RunnablePassthrough.assign(select=select_chain).with_config({"run_name": "SELECT"}) | \
                RunnablePassthrough.assign(where=where_chain).with_config({"run_name": "WHERE"}) | \
                RunnablePassthrough.assign(vpdl_draft=generate_vpdl_skeleton_wrapper).with_config({"run_name": "VPDL_DRAFT"})
    

    full_result = full_chain.invoke(
        {
            "view_description": view_description ,
            "meta_1": meta_1_content, 
            "meta_2": meta_2_content,
            "meta_1_path": meta_1_path,
            "meta_2_path": meta_2_path
        },
        config=cfg)

    print(full_result['join'])
    print(full_result['select'])
    print(full_result['where'])
    print(full_result['vpdl_draft'])

    return full_result


if __name__ == "__main__":
    # Configure everything
    config = Config("FULL-CHAIN")
    config.load_keys()
    llm = config.get_llm()
    open_ai_key = config.get_open_ai_key()

    for folder in os.listdir(VIEWS_DIRECTORY):
        #TODO temporary if to process only one view
        # if folder != "Book_Publication":
        #     continue
        folder_path = os.path.join(VIEWS_DIRECTORY, folder)
        if os.path.isdir(folder_path):
            metamodels_folder = os.path.join(folder_path, "metamodels")
            # check for extra folder for complementary metamodels
            extra_folder = os.path.join(metamodels_folder, "extra")
            if os.path.isdir(extra_folder):
                for extra_ecore_file in os.listdir(extra_folder):
                    if extra_ecore_file.endswith(".ecore"):
                        ecore_parser.register_metamodel(os.path.join(extra_folder, extra_ecore_file))
            view_description_file = os.path.join(folder_path, "view_description.txt")
            view_description = open(view_description_file, "r").read()
            ecore_files = []
            for file in os.listdir(metamodels_folder):
                if file.endswith(".ecore"):
                    ecore_files.append(os.path.join(metamodels_folder, file))
                    print(os.path.join(metamodels_folder, file))
                    if len(ecore_files) == 2:
                        # try:
                            execute_chain(llm, view_description, ecore_files[0], ecore_files[1])
                            print("Finished processing chain")
                        # except Exception as e:
                        #     print("Error processing chain")
                        #     print(e)