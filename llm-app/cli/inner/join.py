import os
import sys
import pathlib

from utils.config import Config

from core.vpdl_join_chain import execute_chain

VIEWS_DIRECTORY = os.path.join(pathlib.Path(__file__).parent.absolute(), "..", "..", "Views_Baseline")

if __name__ == "__main__":
    view_name = "Book_Publication"
    prompt_type = "baseline"
    if len(sys.argv) < 4:
        print("Not all arguments were provided")
        print("Usage: python -m cli.inner.join <view_name> <prompt_type>. Assuming default values: Book_Publication, baseline")
        print("view_name: Book_Publication, EA_Application, Evolution, Safety")
        print("prompt_type: baseline, alternative, few-shot-cot, few-shot, simplified")       
    else:
        view_name = sys.argv[1].strip()
        prompt_type = sys.argv[2].strip()

    # Configure everything
    config = Config("SLE-Presentation-Join")
    config.load_keys()
    llm = config.get_llm()
    open_ai_key = config.get_open_ai_key()
    
    folder_path = os.path.join(VIEWS_DIRECTORY, view_name)
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