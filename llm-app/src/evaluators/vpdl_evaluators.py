from langsmith.schemas import Example, Run


    
def similarity_check(root_run: Run, example: Example) -> dict:

    # get the first child run
    main_run = root_run.child_runs[0]

    
    
    score = main_run.outputs.get('vpdl_draft').strip() == example.outputs.get("vpdl_draft").strip()
    score_2 = main_run.outputs.get("vpdl_draft").strip() == example.outputs.get("vpdl_draft").strip()
    
    return {"score": int(score), "key": "similarity_check"}

def mock_check(root_run: Run, example: Example) -> dict:

    # get the first child run
    main_run = root_run.child_runs[0]    
    
    
    score = 32
    
    return {"score": int(score), "key": "mock_check"}
    