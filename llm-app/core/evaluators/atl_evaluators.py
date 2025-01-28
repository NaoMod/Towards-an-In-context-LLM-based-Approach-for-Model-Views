from langsmith.schemas import Example, Run

import json
from collections import defaultdict


def matched_relations(root_run: Run, example: Example) -> dict:

    def parse_relations(json_data):
        data = json.loads(json_data) if isinstance(json_data, str) else json_data
        relations = {}

        for relation in data.get("relations", []):
            from_dict = relation.get("from", {})
            from_key = next(iter(from_dict)) # Get the first entry in the from dictionary assuming there is only one
            from_entry = from_dict[from_key]

            to_entry = relation.get("to", {})

            # Extract (metamodel, class) from the from entry
            from_class = (from_entry.get("metamodel", ""), from_entry.get("class", ""))

            # Extract (metamodel, class) from the to entry and add to the list under from_class key
            to_classes = [(to_value.get("metamodel", ""), to_value.get("class", "")) for _, to_value in to_entry.items()]
            if from_class not in relations:
                relations[from_class] = to_classes
            else:
                relations[from_class].extend(to_classes)

        return relations
  
    main_run_relations = parse_relations(root_run.outputs.get('join'))
    example_relations = parse_relations(example.outputs.get('relations'))

    matched_classes = 0  # true positives
    false_positives = 0  # Predicted but not actually present in the example
    false_negatives = 0  # Actually present in the example but not predicted
    total_relations_ground_truth = 0  # Total number of relations in the example

    # Calculate matched classes (true positives)
    for from_entry, to_entries in main_run_relations.items():
        if from_entry in example_relations:
            for to_entry in to_entries:
                if to_entry in example_relations[from_entry]:
                    matched_classes += 1
                else:
                    false_positives += 1
        else:
            false_positives += len(to_entries) 

    # Calculate false negatives
    for from_entry, to_entries in example_relations.items():
        if from_entry not in main_run_relations:
            false_negatives += len(to_entries)
        else:
            for to_entry in to_entries:
                if to_entry not in main_run_relations[from_entry]:
                    false_negatives += 1

        total_relations_ground_truth += len(to_entries)

    match_percentage = (matched_classes / total_relations_ground_truth) * 100 if total_relations_ground_truth > 0 else 0

    # how many of the actually present relations (matched_classes + false_negatives) were correctly identified (matched_classes).
    recall = matched_classes / (matched_classes + false_negatives) if matched_classes + false_negatives > 0 else 0

    return {"results": [{"key": "Reference number (cls)", "score": total_relations_ground_truth},
                        {"key": "Matched Classes", "score": matched_classes}, 
                        {"key": "False Positives (cls)", "score": false_positives}, 
                        {"key": "False Negatives (cls)", "score": false_negatives},
                        {"key": "Recall (cls)", "score": recall},
                        {"key": "Non-matched Classes", "score": false_positives + false_negatives},
                        {"key": "Match Percentage (cls)", "score": match_percentage}]}