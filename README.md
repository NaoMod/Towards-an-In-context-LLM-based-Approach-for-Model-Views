## Towards an In-context LLM-based Approach for Automating the Definition of Model Views

This repository contains all the artifacts for the paper "Towards an In-context LLM-based Approach for Automating the Definition of Model Views," accepted at the 17th International Conference on Software Language Engineering (SLE '24).

### Environment Preparation ⚙️

How to prepare the environment to execute the tool.

#### Requirements

- Python >= 3.8 
- To execute the tool, it's necessary to have an [OpenAI API key](https://platform.openai.com/docs/api-reference/introduction). It is a paid service, and an OpenAI account is mandatory. The price may vary depending on the selected model.
- To execute and check the evaluation results in the LangSmith UI, it's necessary to have a [LangSmith API key](https://docs.smith.langchain.com/how_to_guides/setup/create_account_api_key). It is a paid service, and an LangSmith account is mandatory. They have a free quota that is enough for execute the tests provided on this paper. If not provided, the code still works.
    - <small>Both OpenAI and LangSmith are independent companies with no relations with the authors. Carefully read their Terms and Conditions to check how they treat personal data.</small>

#### Project Preparation

- The directory `llm-app` is the root folder containing all the necessary Python files to execute the tool. Unless explicitly mentioned otherwise, all references to execute a file should consider that the given path lives in the root folder.

##### Using a Virtual Environment to Avoid Global Installation

It is possible to ignore these commands, but global package installation can lead your environment to unstable states (the commands were tested on Ubuntu/Linux and Windows 11).

- `python -m venv ENV`
    - This command will create an `ENV` folder at the root level.
- Execute `ENV\Scripts\activate.ps1` (Windows-PowerShell) or `source ENV/bin/activate` (Bash-Linux).
- (ENV) `python -m pip install --upgrade pip`

##### Install Dependencies

- `pip install -r requirements.txt`

Now, your environment is ready to go with the provided code.

### Use the Tool 🚀

1. Copy the content from the file `token_ex.txt` to a `token.txt` file (`copy token_ex.txt token.txt`).
2. Fill the new file by replacing the word "test" with your API keys (`token` for OpenAI key and `langsmith` for LangSmith key).
3. Execute the experiments by running (ENV)`python src/vpdl.py` for the View experiments and/or (ENV)`python src/atl.py` for the ATL experiments.
    - Notes: If Langsmith key was provided, both executions will create traces under the project name `FULL-CHAIN` on the Langsmith UI.
4. The results will be printed in the console, and you can copy and paste them into the actual tool in use (EMF Views or ATL editor, respectvely) to be adjusted and executed.

### Running the Evaluation to Reproduce the Paper Results ✍️

(LangSmith use is mandatory for this process)
1. Create the datasets by running the scripts (ENV)`python src/datasets/vpdl_dataset_creator.py` and (ENV)`python src/datasets/atl_dataset_creator.py`.
    - These will create the datasets in your LangSmith environment.
2. Execute the script (ENV)`python src/run_evaluation.py vpdl` for the View experiments and/or (ENV)`python src/run_evaluation.py atl` for the ATL experiments.
    - Note: The file `src/run_evaluation.py` comments contain instructions to setup different configurations other than used in the paper.
3. The console will print the success/error status of the execution.
4. The results should be accessible in your LangSmith workspace.
    - Important note: Due to the probabilistic nature of the LLMs, the results may or may not match exactly those presented in the paper, but they should match on average.

### Other Artifacts

- The directory `(repository_root)/paper_data/chatgpt_experiment` contains the prompts used in the ChatGPT experiments (referenceed as baseline in the paper), including both the prompt and the completion, together with a public link to access them on ChatGPT platform.
- The directory `(repository_root)/paper_data/prompts` contains all exact prompts used in our experiments for reference.
- The directory `(repository_root)/Views_Baseline` contains all the EMF Views projects. Each one contains a specific README file with more information.
    - To run them, you need to have an Eclipse instance with the [EMF Views plugin](https://www.atlanmod.org/emfviews/manual/user.html) installed.
- The directory `(repository_root)/Views_ATL_Baseline` contains all the ATL projects.
    - To run them, you need to have an Eclipse instance with [ATL](https://eclipse.dev/atl/) installed.