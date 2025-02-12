# Towards an In-context LLM-based Approach for Automating the Definition of Model Views

This repository contains artifacts for the paper "Towards an In-context LLM-based Approach for Automating the Definition of Model Views," accepted at the 17th International Conference on Software Language Engineering (SLE '24).

This repository includes all the necessary tools to replicate the experiments described in the paper, including scripts for generating the datasets.
Additionally, the artifact contains all prompt data used in the experiments and baseline model views in VPDL (EMF Views DSL) and ATL.
This artifact enables the reproduction of the results discussed in the paper.

- You can access the paper at [HAL](https://hal.science/hal-04698209v1/).
- The slides deck for the presentation is available at this [link](https://zenodo.org/records/14446887)

**IMPORTANT NOTE**: The code may have changed since the paper publication. The `paper_artifact` branch and the [Zenodo permalink](https://zenodo.org/records/13827683) for these artifacts (DOI: 10.5281/zenodo.13827683) contain the exact code that supports the paper results. The version in the `main` branch may contain some changes.

## Table of Contents

- [Environment Preparation ⚙️](#environment-preparation-⚙️)
  - [Requirements](#requirements)
  - [Project Preparation](#project-preparation)
- [Use the Tool 🚀](#use-the-tool-🚀)
  - [Use the API](#use-the-api)
  - [Use the CLI](#use-the-cli)
- [Reproduce the Paper Results ✍️](#running-the-evaluation-to-reproduce-the-paper-results-✍️)
- [Build the tool](#build)
- [Troubleshooting](#troubleshooting)
- [Other Artifacts](#other-artifacts)

## Environment Preparation ⚙️

### Requirements

#### Tools
- **Docker**: Version 27.3.1 or higher

#### Services (optional)
- **OpenAI API Key**: Altough the project allows flexibility regarding the LLM choice, the main results were obteined using OpenAI models. Get the key from [OpenAI API](https://platform.openai.com/docs/api-reference/introduction). Note that this is a paid service. The price may vary depending on the selected model.
- **LangSmith API Key**: Obtain from [LangSmith API](https://docs.smith.langchain.com/how_to_guides/setup/create_account_api_key). Note that this is also a paid service, but they offer a free quota sufficient for the tests described in the paper.
   - <small>Both OpenAI and LangSmith are independent companies. Please review their Terms and Conditions regarding personal data.</small>
   - <small>We didn't provide any pre-paid API keys to preserve the users' data since they can leak user information into the metadata that we would have access to</small>

### Project Preparation

#### Pulling docker image

```bash
   docker pull atlanmod/llm-for-emf-views:v1
```

#### Include new Views and Transformations (optional)

All current acessible model views (VPDL) and model transformations (ATL) are within the folders `Views_Baseline` and `ATL_Baseline` at the directory `llm-app`. To include new ones, it is necessary to include new folders following the same structure that the app is prepared to parse.

For Views: Ecore files into `metamodels` folder (exact 2 ecore files) and a file named "view_description.txt" containing the user prompt.
For Tranformations: Ecore files into `metamodels` folder (exact 2 ecore files) and a file named "transformation_description.txt" containing the user prompt.

The text files are used only with the CLI tool. For the API, the description is given by an argument. Check an example in the file [input_api](input_api.json).

## Use the Tool 🚀

1. **Set ENV Variables**:
   - Copy the content from `.env.example` file in this repository to a new file named `.env` and save it in your working folder:
     ```bash
     copy token_ex.txt token.txt
     ```
   - Fill it with all enviromental variables necessary to use the tool, including the API keys ( for OpenAI and LangSmith for example). The variable names are self-explanatory.

### Use the API

1. Start the API with the following Docker command:

```bash
    docker run --env-file .env -p 5000:5000 atlanmod/llm-for-emf-views:v1
```

This will start the API and give you access to it through the `localhost:5000`

#### Example of using it with `curl`:

```bash
    curl.exe -X POST -H "Content-Type: application/json" -d '@input_api.json' http://127.0.0.1:5000/vpdl
```
This example is using the example file [input_api](input_api.json) as input, put the parameters can also be passed as `curl` direct arguments.
The inner [README](llm-app/README.md) contains the API documentation.

### Use the CLI

1. **With the running container (`docker start atlanmod/llm-for-emf-views:v1`), get the container ID**:

```bash
   docker ps
```

2. **Execute the CLI tool**:
   1. `docker exec -it [container ID] python -m cli.vpdl view_name prompt_type` for VPDL examples (the view description should exist in the file mentioned before)
   2. `docker exec -it [container ID] python -m cli.atl transformation_name prompt_type` for ATL examples

3. **Results**:
   - Results will be printed in the console. Copy and paste them into the respective tools (EMF Views or ATL editor) for further adjustment and execution.

#### Prompt Types
The available prompt_types are: ["baseline", "alternative", "few-shot-cot", "few-shot-only", "simplified"], each one with its own particularity with different results.

#### Traces
   - If a LangSmith key is provided among the env variables, traces will be created in the LangSmith UI wth self-explanatory project names.

## Running the Evaluation to Reproduce the Paper Results ✍️

**LangSmith key is required for this process.**

1. **Create Datasets**:
   ```bash
   python -m datasets.vpdl_dataset_creator
   python -m datasets.atl_dataset_creator
   ```

2. **Execute Evaluation**:
   - For View experiments:
     ```bash
     python -m cli.un_evaluation vpdl
     ```
   - For ATL experiments:
     ```bash
     python -m cli.un_evaluation atl
     ```
   - Refer to comments in `src/run_evaluation.py` for alternative configurations.

3. **Check Results**:
   - Results will be accessible in your LangSmith workspace. Note that due to the probabilistic nature of LLMs, results may vary slightly from those in the paper but should be consistent on average.

### Build

All instructions below should consider that the project's root folder is the `llm-app`, except when explicitly mentioned.

After clone the repository.

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

#### Run locally

The same configurations and arguments of the examples in the section Use the Tool 🚀](#use-the-tool-🚀) should work locally.

##### Example of the VPDL generation (CLI):
`python -m cli.vpdl Safety baseline`

##### Running the API locally:
`python -m api.app`
It will be acessible at localhost:5000

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
- **EMF Views Projects**: In `(repository_root)/llm-app/Views_Baseline`. Each project contains a README with more details. Requires an Eclipse instance with the [EMF Views plugin](https://www.atlanmod.org/emfviews/manual/user.html).
- **ATL Projects**: In `(repository_root)/llm-app/Views_ATL_Baseline`. Requires an Eclipse instance with [ATL](https://eclipse.dev/atl/) installed.