from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from .prompt_templates.select import prompts as select_templates
from .runnable_interface import RunnableInterface

from output_parsers.ecore_attributes_parser import EcoreAttributesParser

class Select(RunnableInterface):
    """
    Select class for managing the select prompt templates.
    """

    def __init__(self):
        """
        Initialize the Select class.
        """
        self.tags = select_templates["items"][0]["tags"]
        self.prompt = PromptTemplate.from_template(select_templates["items"][0]["template"])

    def set_model(self, llm):
        self.model = llm        

    def set_parser(self, meta_1 = None, meta_2 = None):        
        # raise error if some of the parameters are missing
        if meta_1 is None or meta_2 is None:
            raise ValueError("Metamodels are required to parse the output using Ecore checkers.")
        self.parser = EcoreAttributesParser(meta_1=meta_1, meta_2=meta_2)

    def get_runnable(self):
        """
        Get the runnable object.

        Parameters:
            parser (Parser): The parser object.

        Returns:
            Runnable: The runnable object.
        """
        return self.prompt | self.model | self.parser

    def get_tags(self):
        """
        Get the tags.

        Returns:
            list[str]: The tags.
        """
        return self.tags
