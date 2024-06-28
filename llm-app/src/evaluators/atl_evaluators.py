from langsmith.schemas import Example, Run

import json
from collections import defaultdict


def matched_relations(root_run: Run, example: Example) -> dict:

    def parse_relations(json_data):
        data = json.loads(json_data) if isinstance(json_data, str) else json_data
        relations = defaultdict(int)
        
        for relation in data.get("relations", []):
            from_classes = frozenset((key, v['metamodel'], v['class']) for key, v in relation['from'].items())
            to_classes = frozenset((key, v['metamodel'], v['class']) for key, v in relation['to'].items())
            relations[(from_classes, to_classes)] += 1
        
        return relations

    main_run = root_run.child_runs[0]
    
    main_run_relations = parse_relations(main_run.outputs.get('join'))
    example_relations = parse_relations(example.outputs.get('join'))

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