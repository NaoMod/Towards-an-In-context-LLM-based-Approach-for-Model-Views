import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_evaluation.py <experiment>. Assuming default value: vpdl")
        print("experiment: vpdl, atl")
        experiment = "vpdl"
    else:
        experiment = sys.argv[1].strip()

    if experiment == "vpdl":
        from evaluate_vpdl import execute_evaluation
        
        prompt_types = ["baseline", "improved", "few-shot-cot", "few-shot-only", "simplified"]
        few_shot_examples = [1, 2, 4]
        temperatures = [0, 0.01, 0.5, 1, 2]
        repetitions = 1

        dataset_name = "VPDL_FINAL_1"
        
        for prompt_type in prompt_types:
            if prompt_type == "few-shot-cot" or prompt_type == "few-shot":
                for examples_no in few_shot_examples:
                    execute_evaluation(dataset_name, prompt_type, examples_no, repetitions)
            else:
                execute_evaluation(dataset_name=dataset_name, prompt_type=prompt_type, repetitions=repetitions)


