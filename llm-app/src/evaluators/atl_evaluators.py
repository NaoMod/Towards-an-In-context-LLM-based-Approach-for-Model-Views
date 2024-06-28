from langsmith.schemas import Example, Run

import json
from collections import defaultdict


def matched_relations(root_run: Run, example: Example) -> dict:

    def parse_relations(json_data):
        data = json.loads(json_data) if isinstance(json_data, str) else json_data
        relations = []

        for relation in data.get("relations", []):
            from_entry = relation.get("from", {})
            to_entry = relation.get("to", {})

            # Extract (metamodel, class) from the from entry
            from_class = (from_entry.get("metamodel", ""), from_entry.get("class", ""))

            # Extract (metamodel, class) from the to entry and add to the list under from_class key
            to_classes = [(to_value.get("metamodel", ""), to_value.get("class", "")) for _, to_value in to_entry.items()]
            relations[from_class].extend(to_classes)

        return relations
  
    main_run_relations = parse_relations(root_run.outputs.get('join'))
    example_relations = parse_relations(example.outputs.get('relations'))

    matched_classes = 0  # true positives
    false_positives = 0  # Predicted but not actually present in the example
    false_negatives = 0  # Actually present in the example but not predicted

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

    return {"results": [{"key": "Reference number (cls)", "score": total_relations_ground_truth},
                        {"key": "Matched Classes", "score": matched_classes}, 
                        {"key": "False Positives (cls)", "score": false_positives}, 
                        {"key": "False Negatives (cls)", "score": false_negatives},
                        {"key": "Recall (cls)", "score": recall},
                        {"key": "Non-matched Classes", "score": false_positives + false_negatives},
                        {"key": "Match Percentage (cls)", "score": match_percentage}]}