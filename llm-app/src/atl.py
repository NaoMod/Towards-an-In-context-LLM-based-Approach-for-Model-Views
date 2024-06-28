import os
import pathlib
import sys

from utils.config import Config

from atl_chain import execute_chain

ATL_DIRECTORY = os.path.join(pathlib.Path(__file__).parent.absolute(), "..", "..", "Views_ATL_Baseline")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python chain.py <prompt_type>. Assuming default value: zsCoT")
        print("prompt_type: zsCoT, 1sCoT")
        prompt_type = "zsCoT"
    else:
        prompt_type = sys.argv[1].strip()

    # Configure everything
    config = Config("FULL-CHAIN")
    config.load_keys()
    llm = config.get_llm()
    open_ai_key = config.get_open_ai_key()

    for folder in os.listdir(ATL_DIRECTORY):
        if folder != "BibTex2DocBlock":
            continue
        folder_path = os.path.join(ATL_DIRECTORY, folder)
        if os.path.isdir(folder_path):
            metamodels_folder = os.path.join(folder_path, "metamodels")
            
            transformation_description_file = os.path.join(folder_path, "transformation_description.txt")
            transformation_description = open(transformation_description_file, "r").read()
            ecore_files = []
            for file in os.listdir(metamodels_folder):
                if file.endswith(".ecore"):
                    ecore_files.append(os.path.join(metamodels_folder, file))
                    print(os.path.join(metamodels_folder, file))
                    if len(ecore_files) == 2:
                        # try:
                            execute_chain(llm, transformation_description, ecore_files[0], ecore_files[1], prompt_type)
                            print("Finished processing chain")
                        # except Exception as e:
                        #     print("Error processing chain")
                        #     print(e)