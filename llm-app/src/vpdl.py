import os
import sys
import pathlib

from utils.config import Config

from vpdl_chain import execute_chain

VIEWS_DIRECTORY = os.path.join(pathlib.Path(__file__).parent.absolute(), "..", "..", "Views_Baseline")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python vpdl.py <prompt_type>. Assuming default value: baseline")
        print("prompt_type: baseline, alternative, few-shot-cot, few-shot, simplified")
        prompt_type = "baseline"
    else:
        prompt_type = sys.argv[1].strip()

    # Configure everything
    config = Config("SLE-Presentation")
    config.load_keys()
    llm = config.get_llm()
    open_ai_key = config.get_open_ai_key()

    #execute the chain for each view
    for folder in os.listdir(VIEWS_DIRECTORY):
        # Uncomment below if want to proccess a single view. Use the name of the folder in Views_Baseline
        if folder != "Book_Publication":
            continue
        folder_path = os.path.join(VIEWS_DIRECTORY, folder)
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
                        try:
                            execute_chain(llm, view_description, ecore_files[0], ecore_files[1], prompt_type)
                            print("Finished processing chain")
                        except Exception as e:
                            print("Error processing chain")
                            print(e)