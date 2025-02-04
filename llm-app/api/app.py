from flask import Flask, request, jsonify

import os
import pathlib

from utils.api.config import Config

from core.vpdl_select_chain import execute_chain as execute_select_chain
from core.vpdl_where_chain import execute_chain as execute_where_chain
from core.vpdl_join_chain import execute_chain as execute_join_chain
from core.vpdl_chain import execute_chain as execute_vpdl_chain
from core.atl_chain import execute_chain as execute_atl_chain

VIEWS_DIRECTORY = os.path.join(pathlib.Path(__file__).parent.absolute(), "..", "Views_Baseline")
ATL_DIRECTORY = os.path.join(pathlib.Path(__file__).parent.absolute(), "..", "ATL_Baseline")

app = Flask(__name__)

@app.route("/select", methods=["POST"])
def select():
    data = request.get_json()
    view_name = data.get("view_name")
    prompt_type = data.get("prompt_type")
    view_description = data.get("view_description")
    relations = data.get("relations")

    if not view_name or not relations or not prompt_type:
        return jsonify({"error": "view_name, prompt_type,view_description and relations are required"}), 400
    
    # Configure everything
    config = Config()
    config.load_keys()
    llm = config.get_llm()
    
    folder_path = os.path.join(VIEWS_DIRECTORY, view_name)
    if os.path.isdir(folder_path):
        metamodels_folder = os.path.join(folder_path, "metamodels")
        
        ecore_files = []
        for file in os.listdir(metamodels_folder):
            if file.endswith(".ecore"):
                ecore_files.append(os.path.join(metamodels_folder, file))
                print(os.path.join(metamodels_folder, file))
                if len(ecore_files) == 2:
                    result = execute_select_chain(llm, view_description, relations, ecore_files[0], ecore_files[1])

    return jsonify({"result": result})

@app.route("/where", methods=["POST"])
def where():
    data = request.get_json()
    view_name = data.get("view_name")
    prompt_type = data.get("prompt_type")
    view_description = data.get("view_description")
    relations = data.get("relations")

    if not view_name or not relations or not prompt_type:
        return jsonify({"error": "view_name, prompt_type,view_description and relations are required"}), 400
    
    # Configure everything
    config = Config()
    config.load_keys()
    llm = config.get_llm()
    
    folder_path = os.path.join(VIEWS_DIRECTORY, view_name)
    if os.path.isdir(folder_path):
        metamodels_folder = os.path.join(folder_path, "metamodels")
        
        ecore_files = []
        for file in os.listdir(metamodels_folder):
            if file.endswith(".ecore"):
                ecore_files.append(os.path.join(metamodels_folder, file))
                print(os.path.join(metamodels_folder, file))
                if len(ecore_files) == 2:
                    result = execute_where_chain(llm, view_description, relations, ecore_files[0], ecore_files[1])

    return jsonify({"result": result})

@app.route("/join", methods=["POST"])
def join():
    data = request.get_json()
    view_name = data.get("view_name")
    prompt_type = data.get("prompt_type")
    view_description = data.get("view_description")

    if not view_name or not prompt_type:
        return jsonify({"error": "view_name, prompt_type, and view_description are required"}), 400
    
    # Configure everything
    config = Config()
    config.load_keys()
    llm = config.get_llm()
    
    folder_path = os.path.join(VIEWS_DIRECTORY, view_name)
    if os.path.isdir(folder_path):
        metamodels_folder = os.path.join(folder_path, "metamodels")
        
        ecore_files = []
        for file in os.listdir(metamodels_folder):
            if file.endswith(".ecore"):
                ecore_files.append(os.path.join(metamodels_folder, file))
                print(os.path.join(metamodels_folder, file))
                if len(ecore_files) == 2:
                    result = execute_join_chain(llm, view_description, ecore_files[0], ecore_files[1])

    return jsonify({"result": result})

@app.route("/vpdl", methods=["POST"])
def vpdl():
    data = request.get_json()
    view_name = data.get("view_name")
    prompt_type = data.get("prompt_type")
    view_description = data.get("view_description")

    if not view_name or not prompt_type:
        return jsonify({"error": "view_name, prompt_type, and view_description are required"}), 400
    
    # Configure everything
    config = Config()
    config.load_keys()
    llm = config.get_llm()
    
    folder_path = os.path.join(VIEWS_DIRECTORY, view_name)
    if os.path.isdir(folder_path):
        metamodels_folder = os.path.join(folder_path, "metamodels")
        
        ecore_files = []
        for file in os.listdir(metamodels_folder):
            if file.endswith(".ecore"):
                ecore_files.append(os.path.join(metamodels_folder, file))
                print(os.path.join(metamodels_folder, file))
                if len(ecore_files) == 2:
                    result = execute_vpdl_chain(llm, view_description, ecore_files[0], ecore_files[1])

    return jsonify({"result": result})

@app.route("/atl", methods=["POST"])
def atl():
    data = request.get_json()
    transformation_name = data.get("view_name")
    prompt_type = data.get("prompt_type")
    view_description = data.get("view_description")

    if not transformation_name or not prompt_type:
        return jsonify({"error": "view_name, prompt_type, and view_description are required"}), 400
    
    # Configure everything
    config = Config()
    config.load_keys()
    llm = config.get_llm()
    
    folder_path = os.path.join(ATL_DIRECTORY, transformation_name)
    if os.path.isdir(folder_path):
        metamodels_folder = os.path.join(folder_path, "metamodels")
        
        ecore_files = []
        for file in os.listdir(metamodels_folder):
            if file.endswith(".ecore"):
                ecore_files.append(os.path.join(metamodels_folder, file))
                print(os.path.join(metamodels_folder, file))
                if len(ecore_files) == 2:
                    result = execute_atl_chain(llm, view_description, ecore_files[0], ecore_files[1])

    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)


