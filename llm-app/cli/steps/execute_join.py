import os
import sys
import pathlib

from core.runnables.views.join import Join
from core.loaders.ecore_loader import EcoreLoader

from utils.ecore.parser import EcoreParser
from utils.config import Config

ecore_parser = EcoreParser()

def execute_chain(llm, view_description, meta_1_path, meta_2_path, pe_type = "baseline", examples_no = 1):

    # LOADERS
    meta_1_loader = EcoreLoader(meta_1_path)    
    meta_1 = meta_1_loader.load()
    meta_1_content = meta_1[0].page_content

    meta_2_loader = EcoreLoader(meta_2_path)
    meta_2 = meta_2_loader.load()
    meta_2_content = meta_2[0].page_content

    join_runnable = Join(prompt_label=pe_type, examples_no=examples_no)
    join_runnable.set_model(llm)
    join_runnable.set_parser(meta_1=meta_1_path, meta_2=meta_2_path)
    join_runnable.set_prompt()
    join_chain = join_runnable.get_runnable()
    cfg = {"tags": join_runnable.get_tags()}

    full_result = join_chain.invoke(
        {
            "view_description": view_description,
            "meta_1": meta_1_content, 
            "meta_2": meta_2_content,
            "meta_1_path": meta_1_path,
            "meta_2_path": meta_2_path
        },
        config=cfg)
   
    print(full_result)

    return full_result

VIEWS_DIRECTORY = os.path.join(pathlib.Path(__file__).parent.absolute(), "..", "..","..", "Views_Baseline")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python vpdl.py <prompt_type>. Assuming default value: baseline")
        print("prompt_type: baseline, alternative, few-shot-cot, few-shot, simplified")
        prompt_type = "baseline"
    else:
        prompt_type = sys.argv[1].strip()

    # Configure everything
    config = Config("Test-Only-Where")
    config.load_keys()
    llm = config.get_llm()
    open_ai_key = config.get_open_ai_key()
    
    folder_path = os.path.join(VIEWS_DIRECTORY, "Book_Publication")
    if os.path.isdir(folder_path):
        metamodels_folder = os.path.join(folder_path, "metamodels")
        
        view_description_file = os.path.join(folder_path, "view_description_paper.txt")
        if not os.path.isfile(view_description_file):
            view_description_file = os.path.join(folder_path, "view_description.txt")
        view_description = open(view_description_file, "r").read()

        ecore_files = []
        for file in os.listdir(metamodels_folder):
            if file.endswith(".ecore"):
                ecore_files.append(os.path.join(metamodels_folder, file))
                print(os.path.join(metamodels_folder, file))
                if len(ecore_files) == 2:
                    execute_chain(llm, view_description, ecore_files[0], ecore_files[1], prompt_type)
                    print("Finished processing chain")