import os

from langchain_openai import ChatOpenAI
import numpy as np

class Config:

    def __init__(self):
        self.open_ai_key = None
        self.langsmith_key = None
    
    def load_keys(self):
        """
        Load the keys from the token file and configure the environment variables for LangSmith.

        Returns:
            None
        """
        
        # Read the file and load the keys
        script_dir = os.path.dirname(__file__)
        rel_path = '../token.txt'
        abs_file_path = os.path.join(script_dir, rel_path)
        token_file = open(abs_file_path, 'r')
        # Read the first line
        open_ai_token_line = token_file.readline()

        if open_ai_token_line:
            self.open_ai_key = open_ai_token_line.split('=')[1].strip()
            print(f'Open AI Key  is loaded')

        # Read the second line
        langsmith_token_line = token_file.readline()

        if langsmith_token_line:
            self.langsmith_key = langsmith_token_line.split('=')[1].strip()
            print(f'Langsmith Key is loaded')


        if self.langsmith_key is not None:
            # Configure LangSmith
            os.environ["LANGCHAIN_TRACING_V2"] = "true"
            os.environ["LANGCHAIN_PROJECT"] = "MULTI-AGENT"
            os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
            os.environ["LANGCHAIN_API_KEY"] = self.langsmith_key

       
    def get_llm(self):
        """
        Get the ChatOpenAI Language Model to be used during the execution.

        Returns:
            ChatOpenAI: The ChatOpenAI Language Model instance.
        """
        llm = ChatOpenAI(openai_api_key=self.open_ai_key)
        return llm
        

    
    def get_open_ai_key(self):
        """
        Get the Open AI Key to be used during the execution.

        Returns:
            str: The Open AI Key.
        """
        return self.open_ai_key