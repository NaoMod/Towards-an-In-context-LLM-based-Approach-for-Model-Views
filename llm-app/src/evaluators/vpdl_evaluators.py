from langsmith.schemas import Example, Run
import json


    
def similarity_check(root_run: Run, example: Example) -> dict:

    # get the first child run
    main_run = root_run.child_runs[0]   
    
    score = main_run.outputs.get('vpdl_draft').strip() == example.outputs.get("vpdl_draft").strip()
    
    return {"score": int(score), "key": "similarity_check"}

def matched_relations(root_run: Run, example: Example) -> dict:

    def parse_relations(json_str):
        data = json.loads(json_str)
        relations = {}
        for relation in data.get("relations", []):
            classes = tuple(sorted(relation["classes"]))
            relations[classes] = relation["name"]
        return relations

    main_run = root_run.child_runs[0]
    
    main_run_relations = parse_relations(main_run.outputs.get('join'))
    example_relations = parse_relations(example.outputs.get('join'))
    
    matched_classes = sum(1 for cls in main_run_relations if cls in example_relations)
    
    return {"score": matched_classes, "key": "matched_relations"}


    