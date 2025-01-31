from flask import Flask, request, jsonify

import os
import pathlib

from utils.api.config import Config

from core.vpdl_select_chain import execute_chain as execute_select_chain
from core.vpdl_where_chain import execute_chain as execute_where_chain
from core.vpdl_join_chain import execute_chain as execute_join_chain
from core.vpdl_chain import execute_chain as execute_vpdl_chain

VIEWS_DIRECTORY = os.path.join(pathlib.Path(__file__).parent.absolute(), "..", "..", "Views_Baseline")

app = Flask(__name__)

@app.route("/select", methods=["POST"])
def select():
    data = request.get_json()
    view_name = data.get("view_name")
    prompt_type = data.get("prompt_type")
    relations = data.get("relations")

    if not view_name or not relations or not prompt_type:
        return jsonify({"error": "view_name, prompt_type and relations are required"}), 400
    
    # Configure everything
    config = Config()
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
                    result = execute_select_chain(llm, view_description, relations, ecore_files[0], ecore_files[1])

    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)


