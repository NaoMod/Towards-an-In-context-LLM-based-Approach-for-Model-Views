## Towards an In-context LLM-based Approach for Automating the Definition of Model Views

This repository contains all the artifacts for the paper "Towards an In-context LLM-based Approach for Automating the Definition of Model Views, " submitted to the 17th International Conference on Software Language Engineering (SLE 2024).

### PRIVATE REPOSITORY. ONLY ACCESSIBLE ANONYMOUSLY

### Environment preparation ⚙️

How to prepare the environment to execute the tool.

#### Requirements

- Python >= 3.8 
- To execute the tool it's necessary to have a [OpenAI API key](https://platform.openai.com/docs/api-reference/introduction). The service is paid.
- To execute and check the evaluation results in the LangSmith UI, it's necessary to have a [LangSmith API key](https://docs.smith.langchain.com/how_to_guides/setup/create_account_api_key). The service is paid, but it has a free quota.

#### Project preparation

- The directory `llm-app` contains all the necessary python files to execute the tool. All references to execute a file should consider it as the root folder. The following commands should be executed from the root folder.

##### Using Virtual Environment to avoid global installation

It is possible to ignore these commands, but the global package installation can lead your environment to unstable statuses (Tested at Ubuntu/Linux and Windows 11)

- `python -m venv ENV`
    - This command will creat a `ENV` folder in the root level
- Execute `ENV\Scripts\activate.ps1` (Windows-Powershell) or `source ENV/bin/activate` (Bash-Linux)
- (ENV) `python -m pip install --upgrade pip`

##### Install dependencies

- `pip install -r requirements.txt`

Now, your enviroment is ready to go with the provided solution

### Use the tool to reproduce the paper results 🚀

1. Copy the content from the file `token_ex.txt` to a `token.txt` file (`copy token_ex.txt token.txt`);
2. Fill the new file replacing the words "test" by your API keys (`token` for OpenAI key and `langsmith` for LangSmith key);
3. Execute the experiments running (ENV)`python src/vpdl.py` for the View experiments and/or (ENV)`python src/atl.py` for the ATL experiments;
4. The results will be printed in the console and you can copy and paste them to the actual tool in use (EMF Views or ATL editor).

### Running the evaluation ✍️

(LangSmith use is mandatory for this proccess)
1. Create the datasets ruuning the scripts (ENV)`python src/datasets/vpdl_dataset_creator.py` and (ENV)`python src/datasets/atl_dataset_creator.py`
    - These will create the datasets on your LansgSmith environment;
2. Execute the scripts (ENV)`python src/evaluate_vpdl.py` for the View experiments and/or (ENV)`python src/evaluate_atl.py` for the ATL experiments;
3. The console will print the success/error status of the execution;
4. The results should be acessible on your LangSmith workspace;
    - OBS: Due to the nature of the LLMs, the results may or may not match exactly those presented on the paper, but they should match it on average.

### Other artifacts

- The directory `artifacts_evaluation` contains the prompts used in the ChatGPT experiments, including both the prompt and the completion together with a public link to access them.
- The directory `Views_Baseline` contains all the EMF Views projects. Each one contains a specific README file with more information
    - To run them, you need to have an Eclipse instance with the [EMF Views plugin](https://www.atlanmod.org/emfviews/manual/user.html) installed
- The directory  `Views_ATL_Baseline` contains all the ATL projects.
    - To run them,  you need to have an Eclipse instance with the [ATL installed](https://eclipse.dev/atl/).
