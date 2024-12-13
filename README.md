# Towards an In-context LLM-based Approach for Automating the Definition of Model Views

This repository contains artifacts for the paper "Towards an In-context LLM-based Approach for Automating the Definition of Model Views," accepted at the 17th International Conference on Software Language Engineering (SLE '24).

You can access the paper at [HAL](https://hal.science/hal-04698209v1/).
The slides deck for the presentation is available at this [link](https://zenodo.org/records/14446887)

The code may have changed since the paper publication. This `paper_artifact` branch and the [Zenodo permalink](https://zenodo.org/records/13827683) for these artifacts (DOI: 10.5281/zenodo.13827683) contain the exact code that supports the paper results.

This artifact provided files contain all the necessary tools to replicate the experiments described in the paper, including scripts for generating the datasets.
Additionally, the artifact contains all prompt data used in the experiments and baseline model views in VPDL (EMF Views DSL) and ATL.
This artifact enables the reproduction of the results discussed in the paper.

## Table of Contents

- [Environment Preparation ⚙️](#environment-preparation-⚙️)
  - [Requirements](#requirements)
  - [Project Preparation](#project-preparation)
- [Use the Tool 🚀](#use-the-tool-🚀)
- [Running the Evaluation to Reproduce the Paper Results ✍️](#running-the-evaluation-to-reproduce-the-paper-results-✍️)
- [Troubleshooting](#troubleshooting)
- [Other Artifacts](#other-artifacts)

## Environment Preparation ⚙️

### Requirements

- **Python**: Version 3.8 or higher
- **OpenAI API Key**: Obtain from [OpenAI API](https://platform.openai.com/docs/api-reference/introduction). Note that this is a paid service. The price may vary depending on the selected model.
- **LangSmith API Key**: Obtain from [LangSmith API](https://docs.smith.langchain.com/how_to_guides/setup/create_account_api_key). Note that this is also a paid service, but they offer a free quota sufficient for the tests described in the paper.
   - <small>Both OpenAI and LangSmith are independent companies. Please review their Terms and Conditions regarding personal data.</small>
   - <small>We didn't provide any pre-paid API keys to preserve the users' data since they can leak user information into the metadata that we would have access to</small>

### Project Preparation

All instructions below should consider that the project's root folder is the `llm-app`, except when explicitly mentioned.

#### Using a Virtual Environment

It is possible to ignore these commands, but global package installation can lead your environment to unstable states. Tested on Ubuntu/Linux and Windows 11.

1. Create a virtual environment:
   ```bash
   python -m venv ENV
   ```
2. Activate the virtual environment:
   - **Windows (PowerShell)**:
     ```bash
     .\ENV\Scripts\activate.ps1
     ```
   - **Linux (Bash)**:
     ```bash
     source ENV/bin/activate
     ```
3. Upgrade pip:
   ```bash
   (ENV) python -m pip install --upgrade pip
   ```

For MacOS users, it can be necessary to create the environment using the environment marker for pywin32.

#### Install Dependencies

Install required packages:
```bash
pip install -r requirements.txt
```

## Use the Tool 🚀

1. **Prepare API Keys**:
   - Copy the content from `token_ex.txt` to a new file named `token.txt`:
     ```bash
     copy token_ex.txt token.txt
     ```
   - Replace placeholders ("test") with your API keys (`token` for OpenAI, `langsmith` for LangSmith).

2. **Run Experiments**:
   - For View experiments:
     ```bash
     (ENV) python src/vpdl.py
     ```
   - For ATL experiments:
     ```bash
     (ENV) python src/atl.py
     ```
   - If a LangSmith key is provided, traces will be created in the LangSmith UI under the project name `FULL-CHAIN`.

3. **Results**:
   - Results will be printed in the console. Copy and paste them into the respective tools (EMF Views or ATL editor) for further adjustment and execution.

## Running the Evaluation to Reproduce the Paper Results ✍️

**LangSmith key is required for this process.**

1. **Create Datasets**:
   ```bash
   (ENV) python src/datasets/vpdl_dataset_creator.py
   (ENV) python src/datasets/atl_dataset_creator.py
   ```

2. **Execute Evaluation**:
   - For View experiments:
     ```bash
     (ENV) python src/run_evaluation.py vpdl
     ```
   - For ATL experiments:
     ```bash
     (ENV) python src/run_evaluation.py atl
     ```
   - Refer to comments in `src/run_evaluation.py` for alternative configurations.

3. **Check Results**:
   - Results will be accessible in your LangSmith workspace. Note that due to the probabilistic nature of LLMs, results may vary slightly from those in the paper but should be consistent on average.

## Troubleshooting

Below are listed some potential problems executing the tool and what to do in these cases:

- Problem: The OpenAI API sent error code 404. This means that the model is not working correctly.
   - Solution: The file `\src\utils\config.py` line 83 can be edited changing the parameter model_name from "gpt-4o-2024-08-06" to any available model at [OpenAI gpt-4o](https://platform.openai.com/docs/models/gpt-4o) page using the string identifier. Note that we cannot ensure that other models will not change the expected results.
- Problem: The OpenAI API sent error code 429. This means you have reached the token limit per minute on their API.
   - Solution: Wait from 1 to 2 minutes before trying again.
- Problems during dependencies installation: Errors with pip management tool could occur depending on the OS
   - Solution: The essential packages can be installed manually in your environment using your preferred package management. Below is an example of using pip to install the essential packages in this project without using requirements.txt.
    `pip install langchain langchain_community langchain_core langchain_mistralai langchain_openai openai pydantic pyecore langsmith`


## Other Artifacts

Navigate through these files from the `repository_root`

- **ChatGPT Prompts**: Found in `(repository_root)/paper_data/chatgpt_experiment`. Includes prompts and completions used as a baseline.
- **Experiment Prompts**: Located in `(repository_root)/paper_data/prompts`. Contains all exact prompts used in our experiments.
- **EMF Views Projects**: In `(repository_root)/Views_Baseline`. Each project contains a README with more details. Requires an Eclipse instance with the [EMF Views plugin](https://www.atlanmod.org/emfviews/manual/user.html).
- **ATL Projects**: In `(repository_root)/Views_ATL_Baseline`. Requires an Eclipse instance with [ATL](https://eclipse.dev/atl/) installed.