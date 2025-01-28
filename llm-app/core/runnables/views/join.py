from typing import List

from langchain.prompts import PromptTemplate, FewShotPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableParallel
from pydantic.v1 import BaseModel, Field
from langchain.output_parsers import RetryOutputParser

from .prompt_templates.join import prompts as join_templates
from .prompt_templates.examples.for_join import examples as join_examples
from core.interfaces.runnable_interface import RunnableInterface

from core.output_parsers.ecore_classes_parser import EcoreClassesParser

class Relation(BaseModel):
    name: str = Field(..., description="Name of the relation")
    classes: List[str] = Field(..., description="List of two classes. The first coming from the first metamodel and the second from the second metamodel")

class RelationsGroup(BaseModel):
    relations: List[Relation] = Field(..., description="List of relations")

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

    def set_parser(self, meta_1 = None, meta_2 = None):        
        # raise error if some of the parameters are missing
        if meta_1 is None or meta_2 is None:
            raise ValueError("Metamodels are required to parse the output using Ecore checkers.")
        self.parser = EcoreClassesParser(meta_1=meta_1, meta_2=meta_2, pydantic_object=RelationsGroup)
        

    def set_prompt(self, template = None):
        if template is None:
            # check if it should be created with exmaples
            if self.prompt_label == "few-shot-cot" or self.prompt_label == "few-shot-only":
                example_prompt_template = PromptTemplate(
                    input_variables=["view_desc", "ex_meta_1", "ex_meta_2", "relations"],
                    template="View description:{view_desc}\nMetamodel 1: {ex_meta_1}\nMetamodel 2: {ex_meta_2}\nRelations:{relations}"
                )
                self.prompt = FewShotPromptTemplate(
                    # These are the examples we want to insert into the prompt.
                    examples=join_examples[:self.examples_no],
                    # The prompt to format the examples
                    example_prompt= example_prompt_template,
                    # The instructions prompt
                    prefix=join_templates["items"][self.prompt_label]["template"],
                    # The input from the user
                    suffix="#INPUT\nView description:{view_description}\nMetamodel 1: {meta_1}\nMetamodel 2: {meta_2}\nRelations:",
                    # The original variables for any prompt
                    input_variables=["view_description", "meta_1", "meta_2"],
                    # The example_separator is the string we will use to join the prefix, examples, and suffix together with.
                    example_separator="\n\n",
                    partial_variables={"format_instructions":  self.parser.get_format_instructions()},
                )
            else:
                self.prompt = PromptTemplate(
                    template=join_templates["items"][self.prompt_label]["template"],
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
