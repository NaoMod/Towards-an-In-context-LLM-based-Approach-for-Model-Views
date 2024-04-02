from langchain.prompts import PromptTemplate
from langchain import hub

from .prompt_templates.join import prompts as join_templates

class Join():
    """
    Join class for managing the Join prompt templates.
    """

    def __init__(self,):
        """
        Initialize the Join class.
        """
        self.tags = join_templates["items"][0]["tags"]
        self.template = hub.pull("james-mir/join-for-vpdl")

    def get_template(self):
        """
        Get the prompt template.

        Returns:
            PromptTemplate: The prompt template.
        """
        return  self.template

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
