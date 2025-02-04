import os
import sys
import pathlib

from utils.config import Config

from core.vpdl_select_chain import execute_chain

VIEWS_DIRECTORY = os.path.join(pathlib.Path(__file__).parent.absolute(), "..", "..", "Views_Baseline")

if __name__ == "__main__":
    view_name = "Book_Publication"
    prompt_type = "baseline"
    relations = "{'relations': [{'name': 'BookToPublication', 'classes': ['Book', 'Publication']}, {'name': 'ChapterToPublication', 'classes': ['Chapter', 'Publication']}]}"
    if len(sys.argv) < 4:
        print("Not all arguments were provided")
        print("Usage: python -m cli.inner.select <view_name> <prompt_type> <relations>. Assuming default values: Book_Publication, baseline, book_publications_relations")
        print("view_name: Book_Publication, EA_Application, Evolution, Safety")
        print("prompt_type: baseline, alternative, few-shot-cot, few-shot, simplified")       
    else:
        view_name = sys.argv[1].strip()
        prompt_type = sys.argv[2].strip()
        relations = sys.argv[3].strip()

    # Configure everything
    config = Config("SLE-Presentation-Select")
    config.load_keys()
    llm = config.get_llm()
    
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
                    execute_chain(llm, view_description, relations, ecore_files[0], ecore_files[1], prompt_type)
                    print("Finished processing chain")