# Towards an In-context LLM-based Approach for Automating the Definition of Model Views

This repository contains artifacts for the paper *"Towards an In-context LLM-based Approach for Automating the Definition of Model Views,"* accepted at the 17th International Conference on Software Language Engineering (SLE '24).

It includes all necessary tools to replicate the experiments described in the paper, including scripts for dataset generation. Additionally, the artifact contains all prompt data used in the experiments and baseline model views in VPDL (EMF Views DSL) and ATL. This artifact enables the reproduction of the results discussed in the paper.

- Access the paper at [HAL](https://hal.science/hal-04698209v1/).
- The slide deck for the presentation is available [here](https://zenodo.org/records/14446887).

**IMPORTANT NOTE**: The code may have changed since the paper's publication. The `paper_artifact` branch and the [Zenodo permalink](https://zenodo.org/records/13827683) (DOI: 10.5281/zenodo.13827683) contain the exact code supporting the paper's results. The `main` branch may include updates.

## Table of Contents

- [Environment Preparation ⚙️](#environment-preparation-⚙️)
  - [Requirements](#requirements)
  - [Project Preparation](#project-preparation)
- [Using the Tool 🚀](#using-the-tool-🚀)
  - [Using the API](#using-the-api)
  - [Using the CLI](#using-the-cli)
- [Reproducing the Paper Results ✍️](#reproducing-the-paper-results-✍️)
- [Building the Tool](#building-the-tool)
- [Troubleshooting](#troubleshooting)
- [Other Artifacts](#other-artifacts)

## Environment Preparation ⚙️

### Requirements

#### Tools
- **Docker**: Version 27.3.1 or higher

#### Services (optional)
- **OpenAI API Key**: While the project allows flexibility in LLM selection, the main results were obtained using OpenAI models. Get a key from [OpenAI API](https://platform.openai.com/docs/api-reference/introduction). This is a paid service, and pricing varies based on the selected model.
- **LangSmith API Key**: Obtain a key from [LangSmith API](https://docs.smith.langchain.com/how_to_guides/setup/create_account_api_key). LangSmith offers a free quota sufficient for the tests described in the paper.
   - <small>Both OpenAI and LangSmith are independent services. Please review their Terms and Conditions regarding personal data.</small>
   - <small>We do not provide pre-paid API keys to protect user data, as these services may log metadata that could expose sensitive information.</small>

### Project Preparation

#### Pulling the Docker Image

```bash
   docker pull atlanmod/llm-based-model-views:v1
```

#### Adding New Views and Transformations (Optional)

All accessible model views (VPDL) and model transformations (ATL) are located in the `llm-app` directory under `Views_Baseline` and `ATL_Baseline`, respectively. To add new ones, create new folders following the existing structure.

- **Views**: Place exactly two Ecore files in the `metamodels` folder and include a `view_description.txt` file containing the user prompt.
- **Transformations**: Place exactly two Ecore files in the `metamodels` folder and include a `transformation_description.txt` file containing the user prompt.

These text files are used only with the CLI tool. For the API, descriptions are passed as arguments. See an example in [input_api.json](input_api.json).

## Using the Tool 🚀

### Setting Environment Variables

1. Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```
2. Fill in all required environment variables, including API keys (e.g., OpenAI, LangSmith). Variable names are self-explanatory.

### Using the API

Start the API with Docker:

```bash
    docker run --env-file .env -p 5000:5000 atlanmod/llm-based-model-views:v1
```

This launches the API, accessible at `http://127.0.0.1:5000`.

#### Example Usage with `curl`

```bash
    curl -X POST -H "Content-Type: application/json" -d '@input_api.json' http://127.0.0.1:5000/vpdl
```

This uses [input_api.json](input_api.json) as input. Parameters can also be passed as `curl` arguments. API documentation is available in [llm-app/README.md](llm-app/README.md).

### Using the CLI

1. **Start the container**:
   ```bash
   docker start atlanmod/llm-based-model-views:v1
   ```
2. **Get the container ID**:
   ```bash
   docker ps
   ```
3. **Execute the CLI tool**:
   ```bash
   docker exec -it [container ID] python -m cli.vpdl view_name prompt_type
   docker exec -it [container ID] python -m cli.atl transformation_name prompt_type
   ```

### Prompt Types

Available options: `baseline`, `alternative`, `few-shot-cot`, `few-shot-only`, `simplified`.

## Reproducing the Paper Results ✍️

**A LangSmith key is required.**

1. **Create datasets**:
   ```bash
   python -m datasets.vpdl_dataset_creator
   python -m datasets.atl_dataset_creator
   ```
2. **Run evaluation**:
   ```bash
   python -m cli.un_evaluation vpdl
   python -m cli.un_evaluation atl
   ```
3. **Check results**:
   - Results appear in LangSmith.
   - Due to the probabilistic nature of LLMs, slight variations from the paper's results are expected.

## Building the Tool

### Using a Virtual Environment (Recommended)

1. Create and activate a virtual environment:
   ```bash
   python -m venv ENV
   source ENV/bin/activate  # (Linux/macOS)
   .\ENV\Scripts\activate.ps1  # (Windows PowerShell)
   ```
2. Upgrade `pip` and install dependencies:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

### Running Locally

To run the CLI:
```bash
python -m cli.vpdl Safety baseline
```
To run the API locally:
```bash
python -m api.app
```
Access it at `http://127.0.0.1:5000`.

## Troubleshooting

- **OpenAI API error 404**: The model is unavailable.
  - Solution: Modify `src/utils/config.py` (line 83) to use another available model.
- **OpenAI API error 429**: Token limit reached.
  - Solution: Wait 1-2 minutes before retrying.
- **Dependency installation issues**:
  - Solution: Manually install essential packages:
    ```bash
    pip install langchain langchain_community langchain_core openai pydantic pyecore langsmith
    ```

## Other Artifacts

- **ChatGPT Prompts**: `paper_data/chatgpt_experiment`
- **Experiment Prompts**: `paper_data/prompts`
- **EMF Views Projects**: `llm-app/Views_Baseline`
- **ATL Projects**: `llm-app/Views_ATL_Baseline`
