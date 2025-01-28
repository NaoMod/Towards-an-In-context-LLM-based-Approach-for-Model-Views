import os
import pathlib
from langsmith.schemas import Example, Run
import json

from utils.ecore.parser import EcoreParser

VIEWS_DIRECTORY = os.path.join(pathlib.Path(__file__).parent.absolute(), "..", "..", "..", "Views_Baseline")

def find(name):
    if name.startswith("c:") or name.startswith("C:") or name.startswith("file://") or name.startswith("http://") or name.startswith("https://"):
        return name
    for root, _ , files in os.walk(VIEWS_DIRECTORY):
        if name in files:
            return os.path.join(root, name)
        
def get_metamodel_uri(metamodel_path: str) -> str:
    ecore_parser = EcoreParser()
    return ecore_parser.get_metamodel_uri(metamodel_path)

def get_metamodel_plus_class_name(class_name: str, meta_1_path: str, meta_2_path: str) -> str:
    ecore_parser = EcoreParser()
    check_metamodel_1 = ecore_parser.check_ecore_class(meta_1_path, class_name)
    check_metamodel_2 = ecore_parser.check_ecore_class(meta_2_path, class_name)

    if check_metamodel_1:
        return f"{ecore_parser.get_metamodel_uri(meta_1_path)[0]}:{class_name}"
    elif check_metamodel_2:
        return f"{ecore_parser.get_metamodel_uri(meta_2_path)[0]}:{class_name}"
    
def expand_star_attribute(full_class_name: str) -> list:
    metamodel_name, class_name = full_class_name.rsplit(":", 1)
    ecore_parser = EcoreParser()
    return ecore_parser.get_all_class_properties(metamodel_name, class_name)

def matched_filters(root_run: Run, example: Example) -> dict:

    def parse_filters(json_data, meta_1_path, meta_2_path):
        data = json.loads(json_data) if isinstance(json_data, str) else json_data
        filters_to_return = {}
        for _ , filters in data['filters'].items():
            for cls_name, attributes in filters.items():
                # find the metamodel of the given class and get the full name f"{metamodel_uri}:{class_name}"
                full_class_name  = get_metamodel_plus_class_name(cls_name, find(meta_1_path), find(meta_2_path))
                if full_class_name not in filters_to_return:
                    filters_to_return[full_class_name] = []
                for attr in attributes:
                    # if attribute is *, it should expand to all attributes of the class
                    if attr == "*":
                        filters_to_return[full_class_name] += [prop for prop in expand_star_attribute(full_class_name) if prop not in filters_to_return[full_class_name]]
                    else:
                        filters_to_return[full_class_name] += [attr] if attr not in filters_to_return[full_class_name] else []
        return filters_to_return

    def compare_class_attributes(predicted_filters, reference_filters):
        matched_filters = 0 # true positives
        non_matched_filters = 0 # false positives (Predicted but not actually present in the example)
        reference_number = 0

        for class_name, filters in reference_filters.items():
            reference_number += len(filters)
            if class_name in predicted_filters:
                for filter in filters:
                    if filter not in predicted_filters[class_name]:
                        non_matched_filters += 1
            else:
                non_matched_filters += len(filters)

        for class_name, filters in predicted_filters.items():
            if class_name in reference_filters:
                for filter in filters:
                    if filter in reference_filters[class_name]:
                        matched_filters += 1        

        return matched_filters, reference_number, non_matched_filters

    main_run = root_run.child_runs[0]

    if main_run.outputs is None:
        return {"results": [{"key": "Reference number (attr)", "score": 0},
                            {"key": "Matched Filters", "score": 0}, 
                            {"key": "Precision (attr)", "score": 0},
                            {"key": "Recall (attr)", "score": 0},
                            {"key": "Non-matched Filters", "score": 0}]}
    
    main_run_filters = parse_filters(main_run.outputs.get('select'), main_run.inputs.get('meta_1_path'), main_run.inputs.get('meta_2_path'))
    example_filters_ground_truth = parse_filters(example.outputs.get('select'), example.inputs.get('meta_1_path'), example.inputs.get('meta_2_path'))

    matched_filters, reference_number, non_matched_relations = compare_class_attributes(main_run_filters, example_filters_ground_truth)

    precision = matched_filters / (matched_filters + non_matched_relations) if (matched_filters + non_matched_relations) > 0 else 0
    recall = matched_filters / reference_number if reference_number > 0 else 0
    
    return {"results": [{"key": "Reference number (attr)", "score": reference_number},
                        {"key": "Matched Filters", "score": matched_filters}, 
                        {"key": "Precision (attr)", "score": precision},
                        {"key": "Recall (attr)", "score": recall},
                        {"key": "Non-matched Filters", "score": non_matched_relations}]}

def matched_relations(root_run: Run, example: Example) -> dict:

    def parse_relations(json_data, meta_1_path, meta_2_path):
        data = json.loads(json_data) if isinstance(json_data, str) else json_data
        relations = {}
        for relation in data.get("relations", []):
            # each relation contains exact one class per metamodel
            # get the metamodel uri and use it combined with the class name to create a unique key
            metamodel_1_uri = get_metamodel_uri(find(meta_1_path))[0]
            class_name_1 = relation["classes"][0]
            key_1 = f"{metamodel_1_uri}:{class_name_1}"

            metamodel_2_uri = get_metamodel_uri(find(meta_2_path))[0]
            class_name_2 = relation["classes"][1]
            key_2 = f"{metamodel_2_uri}:{class_name_2}"

            classes = tuple(sorted((key_1, key_2)))
            if classes not in relations:
                relations[classes] = 0
            relations[classes] += 1
        return relations

    main_run = root_run.child_runs[0]

    if main_run.outputs is None:
        return {"results": [{"key": "Reference number (cls)", "score": 0},
                            {"key": "Matched Classes", "score": 0}, 
                            {"key": "Precision (cls)", "score": 0},
                            {"key": "Recall (cls)", "score": 0},
                            {"key": "Non-matched Classes", "score": 0}]}
    
    
    main_run_relations = parse_relations(main_run.outputs.get('join'), main_run.inputs.get('meta_1_path'), main_run.inputs.get('meta_2_path'))
    reference_relations = parse_relations(example.outputs.get('join'), example.inputs.get('meta_1_path'), example.inputs.get('meta_2_path'))

    matched_relations = 0 # true positives
    non_matched_relations = 0 # false positives (Predicted but not actually present in the example)
    reference_number = 0

    precision   = 0 
    recall      = 0

    for value, count in reference_relations.items():
        reference_number += count
        if value in main_run_relations:
            matched_relations += min(count, main_run_relations[value])

    for value, count in main_run_relations.items():
        if value not in reference_relations:
            non_matched_relations += count
        else:
            non_matched_relations += max(0, count - reference_relations[value])

    precision = matched_relations / (matched_relations + non_matched_relations) if (matched_relations + non_matched_relations) > 0 else 0
    recall = matched_relations / reference_number if reference_number > 0 else 0
    

    return {"results": [{"key": "Reference number (cls)", "score": reference_number},
                        {"key": "Matched Classes", "score": matched_relations}, 
                        {"key": "Precision (cls)", "score": precision},
                        {"key": "Recall (cls)", "score": recall},
                        {"key": "Non-matched Classes", "score": non_matched_relations}]}