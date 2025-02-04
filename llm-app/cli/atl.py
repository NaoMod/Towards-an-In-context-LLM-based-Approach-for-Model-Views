import os
import pathlib
import sys

from utils.config import Config

from core.atl_chain import execute_chain

ATL_DIRECTORY = os.path.join(pathlib.Path(__file__).parent.absolute(), "..", "..", "ATL_Baseline")

if __name__ == "__main__":
    transformation_name = "BibTex2DocBlock"
    prompt_type = "baseline"
    if len(sys.argv) < 3:
        print("Not all arguments were provided")
        print("Usage: python -m cli.atl <transformation_name> <prompt_type>. Assuming default values: BibTex2DocBlock, baseline")
        print("transformation_name: BibTex2DocBlock, Class2Relational, Families2Persons, RSS2Atom, Tree2List")
        print("prompt_type: baseline, alternative, few-shot-cot, few-shot, simplified")       
    else:
        transformation_name = sys.argv[1].strip()
        prompt_type = sys.argv[2].strip()

    # Configure everything
    config = Config("SLE-Presentation-ATL")
    config.load_keys()
    llm = config.get_llm()

    folder_path = os.path.join(ATL_DIRECTORY, transformation_name)
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
                    try:
                        execute_chain(llm, transformation_description, ecore_files[0], ecore_files[1], prompt_type)
                        print("Finished processing chain")
                    except Exception as e:
                        print("Error processing chain")
                        print(e)