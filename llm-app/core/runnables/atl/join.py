from langchain.prompts import PromptTemplate, FewShotPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser


from .prompt_templates.join import prompts as join_templates
from .prompt_templates.examples.for_join import examples as join_examples
from core.interfaces.runnable_interface import RunnableInterface

from pydantic.v1 import BaseModel, Field

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

    def __init__(self, prompt_label = "baseline", examples_no = 1):
        """
        Initialize the Join class.
        """
        self.tags = join_templates["items"][prompt_label]["tags"]
        self.prompt_label = prompt_label
        self.examples_no = examples_no
        

    def set_model(self, llm):
        self.model = llm        

    def set_parser(self):        
        basic_parser = JsonOutputParser(pydantic_object=RulesList)
        self.parser = OutputFixingParser.from_llm(parser=basic_parser, llm=self.model)

    def set_prompt(self, template = None):
        if template is None:
            # check if it should be created with exmaples
            if self.prompt_label == "few-shot-cot" or self.prompt_label == "few-shot-only":
                example_prompt_template = PromptTemplate(
                    input_variables=["meta_1", "ex_meta_1", "ex_meta_2", "relations"],
                    template="Transformation description:{trans_desc}\nMetamodel 1: {ex_meta_1}\nMetamodel 2: {ex_meta_2}\nRelations:{relations}"
                )
                self.prompt = FewShotPromptTemplate(
                    # These are the examples we want to insert into the prompt.
                    examples=join_examples[:self.examples_no],
                    # The prompt to format the examples
                    example_prompt= example_prompt_template,
                    # The instructions prompt
                    prefix=join_templates["items"][self.prompt_label]["template"],
                    # The input from the user
                    suffix="#INPUT\nTransformation description:{transformation_description}\nMetamodel 1: {meta_1}\nMetamodel 2: {meta_2}\nRelations:",
                    # The original variables for any prompt
                    input_variables=["transformation_description", "meta_1", "meta_2"],
                    # The example_separator is the string we will use to join the prefix, examples, and suffix together with.
                    example_separator="\n\n",
                    partial_variables={"format_instructions":  self.parser.get_format_instructions()},
                )
            else:
                self.prompt = PromptTemplate(
                    template=join_templates["items"][self.prompt_label]["template"],
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
