from langsmith.schemas import Example, Run

class VpdlEvaluator():

    # def __init__(self, vpdl_code =: str):
    #     self.vpdl_code = vpdl_code
    
    def __call__(self, run: Run, example: Example | None = None) -> dict:
        vpdl_output = run.outputs["output"]
        reference_output = example.outputs["vpdl_skeleton"]        
        # Perform comparison logic here
        # For example, you can check if the program output matches the reference output
        
        # Assuming the comparison logic is to check if the program output exactly matches the reference output
        # You might need to adjust this logic based on your specific requirements
        score = vpdl_output.strip() == reference_output.strip()
        
        return {"key": "vpdl_comparison", "score": score}