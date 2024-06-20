from langsmith.schemas import Example, Run
import json

def matched_filters(root_run: Run, example: Example) -> dict:

    def parse_relations(json_data):
        data = json.loads(json_data) if isinstance(json_data, str) else json_data
        relations = {}
        for relation in data.get("relations", []):
            classes = tuple(sorted(relation["classes"]))
            relations[classes] = relation["name"]
        return relations

    def parse_filters(json_data):
        data = json.loads(json_data) if isinstance(json_data, str) else json_data
        filters = {}
        for filter_item in data.get("filters", []):
            filters[filter_item["name"]] = filter_item["classAttributes"]
        return filters

    def compare_class_attributes(filters_1, filters_2):
        matched = 0
        total_filters = 0
        for class_name, filters in filters_1.items():
            if class_name in filters_2:
                total_filters += len(filters)
                if "*" in filters_2[class_name]:
                    matched += len(filters)
                else:
                    for filter in filters:
                        if filter in filters_2[class_name]:
                            matched += 1
        return matched, total_filters

    main_run = root_run.child_runs[0]
    
    main_run_relations = parse_relations(main_run.outputs.get('join'))
    example_relations = parse_relations(example.outputs.get('join'))
  
    main_run_filters = parse_filters(main_run.outputs.get('select'))
    example_filters_ground_truth = parse_filters(example.outputs.get('select'))

    matched_filters_count = 0
    total_filters_count = 0
    for cls, name in main_run_relations.items():
        if cls in example_relations and name in main_run_filters and example_relations[cls] in example_filters_ground_truth:
            main_filters_for_relation = main_run_filters[name]
            example_filters_for_relation = example_filters_ground_truth[example_relations[cls]]
            matched, total = compare_class_attributes(main_filters_for_relation, example_filters_for_relation)
            matched_filters_count += matched
            total_filters_count += total

    filter_match_percentage = (matched_filters_count / total_filters_count) * 100 if total_filters_count > 0 else 0

    return {"score": filter_match_percentage, "key": "matched_filters"}

def matched_relations(root_run: Run, example: Example) -> dict:

    def parse_relations(json_data):
        data = json.loads(json_data) if isinstance(json_data, str) else json_data
        relations = {}
        for relation in data.get("relations", []):
            classes = tuple(sorted(relation["classes"]))
            relations[classes] = relation["name"]
        return relations

    main_run = root_run.child_runs[0]
    
    main_run_relations = parse_relations(main_run.outputs.get('join'))
    example_relations = parse_relations(example.outputs.get('join'))
  
    matched_classes = sum(1 for cls in main_run_relations if cls in example_relations)
    total_relations_ground_truth = len(example_relations)
    match_percentage = (matched_classes / total_relations_ground_truth) * 100 if total_relations_ground_truth > 0 else 0

    return {"score": match_percentage, "key": "matched_relations"}


    