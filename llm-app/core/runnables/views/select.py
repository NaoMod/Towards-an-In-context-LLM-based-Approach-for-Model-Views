from typing import List, Dict

from langchain.prompts import PromptTemplate, FewShotPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableParallel
from pydantic.v1 import BaseModel, Field
from langchain.output_parsers import RetryOutputParser

from .prompt_templates.select import prompts as select_templates
from .prompt_templates.examples.for_select import examples as select_examples
from core.interfaces.runnable_interface import RunnableInterface

from core.output_parsers.ecore_attributes_parser import EcoreAttributesParser

class ClassAttributes(BaseModel):
    __root__: List[str] = Field(..., description="List of class attributes")

class MetamodelClasses(BaseModel):
    __root__: Dict[str, ClassAttributes] = Field(..., description="Dictionary of classes with their attributes. The class name is the key.")

class Filters(BaseModel):
    filters: Dict[str, MetamodelClasses] = Field(..., description="Dictionary of filters with the metamodel name as the key.")

class Select(RunnableInterface):
    """
    Select class for managing the select prompt templates.
    """

    def __init__(self, prompt_label = "baseline", examples_no = 1):
        """
        Initialize the Select class.
        """
        self.tags = select_templates["items"][prompt_label]["tags"]
        self.prompt_label = prompt_label
        self.examples_no = examples_no

    def set_model(self, llm):
        self.model = llm        

    def set_parser(self, meta_1 = None, meta_2 = None):        
        # raise error if some of the parameters are missing
        if meta_1 is None or meta_2 is None:
            raise ValueError("Metamodels are required to parse the output using Ecore checkers.")
        self.parser = EcoreAttributesParser(meta_1=meta_1, meta_2=meta_2, pydantic_object=Filters)

    def set_prompt(self, template = None):
        if template is None:
            if self.prompt_label == "few-shot-cot" or self.prompt_label == "few-shot-only":
                example_prompt_template = PromptTemplate(
                    input_variables=["view_desc", "ex_meta_1", "ex_meta_2", "relations"],
                    template="View description:{view_desc}\nMetamodel 1: {ex_meta_1}\nMetamodel 2: {ex_meta_2}\nRelations:{relations}\nSelect elements:{filters}"
                )
                self.prompt = FewShotPromptTemplate(                    
                    examples=select_examples[:self.examples_no],                    
                    example_prompt= example_prompt_template,                    
                    prefix=select_templates["items"][self.prompt_label]["template"],
                    suffix="#INPUT\nView description:{view_description}\nMetamodel 1: {meta_1}\nMetamodel 2: {meta_2}\nList of relations: {join}\nSelect elements:",
                    input_variables=["view_description", "meta_1", "meta_2", "join"],
                    example_separator="\n\n",
                    partial_variables={"format_instructions":  self.parser.get_format_instructions()},
                )
            else:
                self.prompt = PromptTemplate(
                    template=select_templates["items"][self.prompt_label]["template"],
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
        chain = self.prompt | self.model

        retry_parser = RetryOutputParser.from_llm(parser=self.parser, llm=self.model, max_retries=2)
        
        return RunnableParallel(
            completion=chain, prompt_value=self.prompt
        ) | RunnableLambda(lambda x: retry_parser.parse_with_prompt(**x))

    def get_tags(self):
        """
        Get the tags.

        Returns:
            list[str]: The tags.
        """
        return self.tags
