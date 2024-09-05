import sys
import time

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_evaluation.py <experiment>. Assuming default value: vpdl")
        print("experiment: vpdl, atl")
        experiment = "vpdl"
    else:
        experiment = sys.argv[1].strip()

    if experiment == "vpdl":
        from evaluate_vpdl import execute_evaluation
        
        # THE FOLLOWING LINES EXECUTE THE EVALUATION THAT WAS PRESENTED IN THE PAPER. USE THEM TO REPRODUCE THE RESULTS
        prompt_types = ["few-shot-cot"]
        few_shot_examples = [1]
        temperatures = [0]

        # THE FOLLOWING LINES EXECUTE THE EVALUATION USING VARIATIONS OF THE CONFIGURATION PRESENTED IN THE PAPER. UNCOMMENT TO OVERRIDE THE PREVIOUS CONFIGURATION
        #prompt_types = ["baseline", "alternative", "few-shot-cot", "few-shot-only", "simplified"]
        #few_shot_examples = [1, 2, 4]
        #temperatures = [0, 0.01, 0.5, 1, 2]
        repetitions = 3

        dataset_name = "VPDL_FINAL_EVALUATION"
        
        for prompt_type in prompt_types:
            for temperature in temperatures:
                time.sleep(60) # To avoid error 429 regarding token rate limit per minute
                if prompt_type == "few-shot-cot" or prompt_type == "few-shot-only":
                    for examples_no in few_shot_examples:
                        time.sleep(130)
                        execute_evaluation(
                            dataset_name=dataset_name,
                            prompt_type=prompt_type,
                            examples_no=examples_no,
                            temperature=temperature,
                            repetitions=repetitions
                        )
                else:
                    execute_evaluation(
                        dataset_name=dataset_name,
                        prompt_type=prompt_type,
                        temperature=temperature,
                        repetitions=repetitions
                    )

    elif experiment == "atl":
        from evaluate_atl import execute_evaluation
        
        # THE FOLLOWING LINES EXECUTE THE EVALUATION THAT WAS PRESENTED IN THE PAPER. USE THEM TO REPRODUCE THE RESULTS
        prompt_types = ["few-shot-cot"]
        few_shot_examples = [1]
        temperatures = [0]

        # THE FOLLOWING LINES EXECUTE THE EVALUATION USING VARIATIONS OF THE CONFIGURATION PRESENTED IN THE PAPER. UNCOMMENT TO OVERRIDE THE PREVIOUS CONFIGURATION
        #prompt_types = ["baseline", "few-shot-cot", "few-shot-only"]
        #few_shot_examples = [1, 2, 4]
        #temperatures = [0, 0.01, 0.5, 1, 2]
        repetitions = 1

        dataset_name = "ATL_FINAL_EVALUATION"
        
        for prompt_type in prompt_types:
            for temperature in temperatures:
                time.sleep(60) # To avoid error 429 regarding token rate limit per minute
                if prompt_type == "few-shot-cot" or prompt_type == "few-shot-only":
                    for examples_no in few_shot_examples:
                        time.sleep(130)
                        execute_evaluation(
                            dataset_name=dataset_name,
                            prompt_type=prompt_type,
                            examples_no=examples_no,
                            temperature=temperature,
                            repetitions=repetitions
                        )
                else:
                    execute_evaluation(
                        dataset_name=dataset_name,
                        prompt_type=prompt_type,
                        temperature=temperature,
                        repetitions=repetitions
                    )


