import sys
import os

from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableParallel

from .prompt_templates.select import prompts as select_templates
from interfaces.runnable_interface import RunnableInterface

from output_parsers.ecore_attributes_parser import EcoreAttributesParser, Filters, MetamodelClasses, ClassAttributes

# Add the directory containing utils to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.alt_retry import RetryOutputParser

class Select(RunnableInterface):
    """
    Select class for managing the select prompt templates.
    """

    def __init__(self, pe_type = "zsCoT"):
        """
        Initialize the Select class.
        """
        self.tags = select_templates["items"][pe_type]["tags"]
        self.pe_type = pe_type

    def set_model(self, llm):
        self.model = llm        

    def set_parser(self, meta_1 = None, meta_2 = None):        
        # raise error if some of the parameters are missing
        if meta_1 is None or meta_2 is None:
            raise ValueError("Metamodels are required to parse the output using Ecore checkers.")
        basic_parser = EcoreAttributesParser(meta_1=meta_1, meta_2=meta_2)
        self.parser = RetryOutputParser.from_llm(parser=basic_parser, llm=self.model.with_structured_output(Filters), max_retries=2)

    def set_prompt(self, template = None):
        if template is None:
            self.prompt = PromptTemplate(
                template=select_templates["items"][self.pe_type]["template"],
                input_variables=["view_description", "meta_1", "meta_2", "join"],
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
        def parse_with_prompt(args):
            completion = args['completion']
            if (type(completion) is Filters):
                args = args.copy()
                del args['completion']
                completion = completion.json(ensure_ascii=False)
                args['completion'] = completion

            return self.parser.parse_with_prompt(**args)

        chain = self.prompt | self.model.with_structured_output(Filters, include_raw=False)
        
        return RunnableParallel(
            completion=chain, prompt_value=self.prompt
        ) | RunnableLambda(parse_with_prompt)

    def get_tags(self):
        """
        Get the tags.

        Returns:
            list[str]: The tags.
        """
        return self.tags
