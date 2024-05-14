from langchain.prompts import PromptTemplate
from langchain.output_parsers import OutputFixingParser

from .prompt_templates.join import prompts as join_templates
from interfaces.runnable_interface import RunnableInterface

from output_parsers.ecore_classes_parser import EcoreClassesParser

class Join(RunnableInterface):
    """
    Join class for managing the Join prompt templates.
    """

    def __init__(self):
        """
        Initialize the Join class.
        """
        self.tags = join_templates["items"][0]["tags"]
        

    def set_model(self, llm):
        self.model = llm        

    def set_parser(self, meta_1 = None, meta_2 = None):        
        # raise error if some of the parameters are missing
        if meta_1 is None or meta_2 is None:
            raise ValueError("Metamodels are required to parse the output using Ecore checkers.")
        basic_parser = EcoreClassesParser(meta_1=meta_1, meta_2=meta_2)
        self.parser = OutputFixingParser.from_llm(parser=basic_parser, llm=self.model)
        

    def set_prompt(self, template = None):
        if template is None:
            self.prompt = PromptTemplate(
                template=join_templates["items"][0]["template"],
                input_variables=["view_description", "meta_1", "meta_2"],
                partial_variables={"format_instructions":  self.parser.get_format_instructions()},
            )

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
