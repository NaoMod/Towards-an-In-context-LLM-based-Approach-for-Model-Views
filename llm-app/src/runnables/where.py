from langchain.prompts import PromptTemplate
from langchain import hub

from .prompt_templates.where import prompts as where_templates

class Where():
    """
    Where class for managing the Where prompt templates.
    """

    def __init__(self,):
        """
        Initialize the Where class.
        """
        self.tags = where_templates["items"][0]["tags"]
        self.template = hub.pull("james-mir/where-for-vpdl")

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
