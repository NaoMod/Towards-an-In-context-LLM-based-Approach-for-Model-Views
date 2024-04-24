from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from .prompt_templates.select import prompts as select_templates

class Select():
    """
    Select class for managing the select prompt templates.
    """

    def __init__(self, llm, parser = None):
        """
        Initialize the Select class.
        """
        self.tags = select_templates["items"][0]["tags"]
        self.prompt = PromptTemplate.from_template(select_templates["items"][0]["template"])
        self.model = llm
        if parser is None:
            self.parser = JsonOutputParser()

    def get_prompt(self):
        """
        Get the prompt template.

        Returns:
            PromptTemplate: The prompt template.
        """
        return self.prompt

    def get_runnable(self):
        """
        Get the runnable object.

        Parameters:
            parser (Parser): The parser object.

        Returns:
            Runnable: The runnable object.
        """
        return self.get_prompt() | self.model | self.parser

    def get_tags(self):
        """
        Get the tags.

        Returns:
            list[str]: The tags.
        """
        return self.tags
