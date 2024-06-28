from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser


from .prompt_templates.join import prompts as join_templates
from interfaces.runnable_interface import RunnableInterface

from langchain_core.pydantic_v1 import BaseModel, Field

from typing import List, Dict

class MetamodelClassElement(BaseModel):
    metamodel: str = Field(..., description="Name of the metamodel")
    class_: str = Field(..., description="Name of the class coming from the metamodel", alias="class")

class Rule(BaseModel):
    rule: str = Field(..., description="Name of the relation")
    from_: Dict[str, MetamodelClassElement] = Field(..., alias="from", description="Source class of the relation identified by a string alias")
    to: Dict[str, MetamodelClassElement] = Field(..., description="Target classes of the relation identified by string aliases")

class RulesList(BaseModel):
    relations: List[Rule] = Field(..., description="List of relations between classes in the input and output metamodels.")

class Join(RunnableInterface):
    """
    Join class for managing the Join prompt templates.
    """

    def __init__(self, pe_type = "zsCoT"):
        """
        Initialize the Join class.
        """
        self.tags = join_templates["items"][pe_type]["tags"]
        self.pe_type = pe_type
        

    def set_model(self, llm):
        self.model = llm        

    def set_parser(self):        
        basic_parser = JsonOutputParser(pydantic_object=RulesList)
        self.parser = OutputFixingParser.from_llm(parser=basic_parser, llm=self.model)
        

    def set_prompt(self, template = None):
        if template is None:
            self.prompt = PromptTemplate(
                template=join_templates["items"][self.pe_type]["template"],
                input_variables=["transformation_description", "meta_1", "meta_2"],
                partial_variables={"format_instructions": self.parser.get_format_instructions()},
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
