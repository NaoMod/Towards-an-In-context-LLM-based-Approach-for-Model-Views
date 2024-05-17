import os
import pathlib

from utils.config import Config
from runnables.atl.join import Join

from utils.ecore.parser import EcoreParser

from loaders.ecore_loader import EcoreLoader

VIEWS_DIRECTORY = os.path.join(pathlib.Path(__file__).parent.absolute(), "..", "..", "Views_ATL_Baseline")

ecore_parser = EcoreParser()

def execute_chain(llm, transformation_description , meta_1_path, meta_2_path):

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

    full_result = join_chain.invoke(
        {
            "transformation_description": transformation_description ,
            "meta_1": meta_1_content, 
            "meta_2": meta_2_content,
            "meta_1_path": meta_1_path,
            "meta_2_path": meta_2_path
        },
        config=cfg)

    print(full_result['relations'])

# Configure everything
config = Config("FULL-CHAIN")
config.load_keys()
llm = config.get_llm()
open_ai_key = config.get_open_ai_key()

for folder in os.listdir(VIEWS_DIRECTORY):
    # ignore yakindu2state folder (don't have reference output)
    if folder == "Yakindu2StateCharts":
        continue
    # #TODO temporary if to process only one view
    # if folder != "RSS2Atom":
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
        transformation_description_file = os.path.join(folder_path, "transformation_description.txt")
        transformation_description = open(transformation_description_file, "r").read()
        ecore_files = []
        for file in os.listdir(metamodels_folder):
            if file.endswith(".ecore"):
                ecore_files.append(os.path.join(metamodels_folder, file))
                print(os.path.join(metamodels_folder, file))
                if len(ecore_files) == 2:
                    try:
                        execute_chain(llm, transformation_description, ecore_files[0], ecore_files[1])
                        print("Finished processing chain")
                    except Exception as e:
                        print("Error processing chain")
                        print(e)