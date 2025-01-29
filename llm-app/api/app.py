from flask import Flask, request, jsonify

import os
import pathlib

from utils.config import Config

from cli.steps.execute_select import execute_chain as execute_select_chain
from cli.steps.execute_where import execute_chain as execute_where_chain
from cli.steps.execute_join import execute_chain as execute_join_chain
from core.vpdl_chain import execute_chain as execute_vpdl_chain

VIEWS_DIRECTORY = os.path.join(pathlib.Path(__file__).parent.absolute(), "..", "..", "Views_Baseline")


app = Flask(__name__)

@app.route("/select/execute", methods=["POST"])
def process_file1():
    print(request.data)  # Raw request body
    print(request.headers)
    data = request.get_json()
    arg1 = data.get("arg1")
    arg2 = data.get("arg2")

    if not arg1 or not arg2:
        return jsonify({"error": "arg1 and arg2 are required"}), 400
    
    # Configure everything
    config = Config("Test-API-Select")
    config.load_keys()
    llm = config.get_llm()
   
    relations = "{'relations': [{'name': 'BookToPublication', 'classes': ['Book', 'Publication']}, {'name': 'ChapterToPublication', 'classes': ['Chapter', 'Publication']}]}"
    
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
                    result = execute_select_chain(llm, view_description, relations, ecore_files[0], ecore_files[1])

    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)


