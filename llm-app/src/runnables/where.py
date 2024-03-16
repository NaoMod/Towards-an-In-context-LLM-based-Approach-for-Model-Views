from langchain.prompts import PromptTemplate

from .prompt_templates.join import prompts as where_templates

class Where():
    """
    Where class for managing the Where prompt templates.
    """

    def __init__(self,):
        """
        Initialize the Where class.
        """
        self.tags = where_templates["items"][0]["tags"]
        self.template = where_templates["items"][0]["template"]

    def get_template(self):
        """
        Get the prompt template.

        Returns:
            PromptTemplate: The prompt template.
        """
        return PromptTemplate.from_template(self.template)

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
