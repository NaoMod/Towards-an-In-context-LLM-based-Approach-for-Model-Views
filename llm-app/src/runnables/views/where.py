from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from .prompt_templates.where import prompts as where_templates
from interfaces.runnable_interface import RunnableInterface

from typing import List

from langchain_core.pydantic_v1 import BaseModel, Field, validator

class RuleElement(BaseModel):
    metaclass_1: str = Field(..., description="Name of the metaclass from metamodel 1")
    combination_rule: str = Field(..., description="Combination rule string explaining how the classes can be logically connected according to the domain's semantics")
    metaclass_2: str = Field(..., description="Name of the metaclass from metamodel 2")

# class Rule(BaseModel):
#     rule_elements: RuleElement = Field(..., description="List of rules")

#     # @validator('rule_elements')
#     # def check_length(cls, v):
#     #     if len(v) != 3:
#     #         raise ValueError('List must contain exactly 3 elements')
#     #     return v

class Rules(BaseModel):
    name: str = Field(..., description="Name of the relation")
    rules: List[RuleElement] = Field(..., description="List of rules")

class RulesList(BaseModel):
    rules: List[Rules] = Field(..., description="List of rules for each relation")

class Where(RunnableInterface):
    """
    Where class for managing the Where prompt templates.
    """

    def __init__(self):
        """
        Initialize the Where class.
        """
        self.tags = where_templates["items"][0]["tags"]

    def set_model(self, llm):
        self.model = llm        

    def set_parser(self):        
        self.parser = JsonOutputParser(pydantic_object=RulesList)

    def set_prompt(self, template = None):
        if template is None:
            self.prompt = PromptTemplate(
                template=where_templates["items"][0]["template"],
                input_variables=["view_description", "meta_1", "meta_2", "join"],
                partial_variables={"format_instructions":  self.parser.get_format_instructions()}
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
