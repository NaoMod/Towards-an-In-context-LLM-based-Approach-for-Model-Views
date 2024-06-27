from langsmith.schemas import Example, Run
import json
import csv

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
            if classes not in relations:
                relations[classes] = 0
            relations[classes] += 1
        return relations

    main_run = root_run.child_runs[0]
    
    main_run_relations = parse_relations(main_run.outputs.get('join'))
    example_relations = parse_relations(example.outputs.get('join'))

    matched_classes = 0 # true positives
    false_positives = 0 # Predicted but not actually present in the example
    false_negatives = 0 # Actually present in the example but not predicted

    # Calculate matched classes (true positives)
    for value, count in example_relations.items():
        if value in main_run_relations:
            matched_classes += min(count, main_run_relations[value])
        else:
            false_negatives += count

    # Calculate false positives (values in main_run_relations not in example_relations)
    for value, count in main_run_relations.items():
        if value not in example_relations:
            false_positives += count

    total_relations_ground_truth = sum(example_relations.values())
    match_percentage = (matched_classes / total_relations_ground_truth) * 100 if total_relations_ground_truth > 0 else 0

    # how many of the actually present relations (matched_classes + false_negatives) were correctly identified (matched_classes).
    recall = matched_classes / (matched_classes + false_negatives) if matched_classes + false_negatives > 0 else 0
    
    # Calculate true negatives - don't make sense, since we don't have the full set of relations
    # Calculate the union of all possible class pairs
    # all_classes = set(main_run_relations.keys()).union(set(example_relations.keys()))
    # total_possible_relations = len(all_classes)
    #true_negatives = total_possible_relations - (matched_classes + false_positives + false_negatives)
    
    # Save values to a CSV file
    output_csv_path = "relations_result.csv"
    with open(output_csv_path, mode='w', newline='') as csv_file:
        fieldnames = ['Reference number', 'Matched Classes', 'False Positives', 'False Negatives', 'Recall', 'Non-matched Classes', 'Match Percentage']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerow({
            'Reference number': total_relations_ground_truth,
            'Matched Classes': matched_classes,
            'False Positives': false_positives,
            'False Negatives': false_negatives,
            'Recall': recall,
            'Non-matched Classes': false_positives + false_negatives,
            'Match Percentage': match_percentage
        })

    return {"results": [{"key": "Matched Classes", "value": matched_classes}, 
                        {"key": "False Positives", "value": false_positives}, 
                        {"key": "False Negatives", "value": false_negatives},
                        {"key": "Recall", "value": recall},
                        {"key": "Non-matched Classes", "value": false_positives + false_negatives},
                        {"key": "Match Percentage", "value": match_percentage}]}


    