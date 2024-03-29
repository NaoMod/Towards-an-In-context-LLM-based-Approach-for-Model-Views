from langchain.prompts import PromptTemplate
from langchain import hub

from .prompt_templates.select import prompts as select_templates

class Select():
    """
    Select class for managing the select prompt templates.
    """

    def __init__(self,):
        """
        Initialize the Select class.
        """
        self.tags = select_templates["items"][0]["tags"]
        self.template = hub.pull("james-mir/select-for-vpdl")

    def get_template(self):
        """
        Get the prompt template.

        Returns:
            PromptTemplate: The prompt template.
        """
        return self.template

    def get_runnable(self, parser):
        """
        Get the runnable object.

        Parameters:
            parser (Parser): The parser object.

        Returns:
            Runnable: The runnable object.
        """
        return self.get_template() | parser

    def get_tags(self):
        """
        Get the tags.

        Returns:
            list[str]: The tags.
        """
        return self.tags
