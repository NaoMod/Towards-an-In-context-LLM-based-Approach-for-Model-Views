import os

from langchain_openai import AzureChatOpenAI
# alternative models
from langchain_mistralai import ChatMistralAI 
from langchain_ollama import ChatOllama

class Config:
    """
    Configuration class for managing settings for API use. 

    Methods
    -------
    load_keys()
        Load the keys
    get_llm()
        Get the LLM instance to be used during the execution.
    get_open_ai_key()
        Get the Open AI Key to be used during the execution.
    test_llm()
        Test the LLM functionality by sending messages to the LLM instance.
    """

    def __init__(self):
        self.llm_name = os.getenv("LLM_NAME", "AzureChatOpenAI")
        self.llm = None
        self.temperature = os.getenv("LLM_TEMPERATURE", 0)

    def load_keys(self):
        """
        Load the keys

        Returns
        -------
        None

        """
        self.open_ai_key = os.getenv("LLM_SECRET", 0)

        if self.llm_name == "AzureChatOpenAI":
            self.llm = AzureChatOpenAI(
                azure_endpoint="https://models.inference.ai.azure.com",
                temperature=self.temperature,
                api_key=self.open_ai_key,
                openai_api_version="2024-09-01-preview", 
                model_name="gpt-4o")
        elif self.llm_name == "ChatMistralAI":
            self.llm = ChatMistralAI(
                model="mistral-large-latest",
                temperature=self.temperature,
                mistral_api_key=self.open_ai_key)
        elif self.llm_name == "ChatOllama":
            self.llm = ChatOllama(
                temperature=self.temperature,
                base_url=os.getenv("LLM_API_URL", "http://localhost:8000"),
                model_name="llama3")

    def get_llm(self):
        """
        Get the LLM instance to be used during the execution.

        Returns
        -------
        LLM
            The LLM instance.
        """
        return self.llm
    # TODO: erase?
    def get_open_ai_key(self):
        """
        Get the Open AI Key to be used during the execution.

        Returns
        -------
        str
            The Open AI Key.
        """
        return self.open_ai_key
