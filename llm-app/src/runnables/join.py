from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser

from .prompt_templates.join import prompts as join_templates

class Join():
    """
    Join class for managing the Join prompt templates.
    """

    def __init__(self, llm, parser = None):
        """
        Initialize the Join class.
        """
        self.tags = join_templates["items"][0]["tags"]
        self.prompt = PromptTemplate.from_template(join_templates["items"][0]["template"])
        self.model = llm
        if parser is None:
            basic_parser = JsonOutputParser()
            self.parser = OutputFixingParser.from_llm(parser=basic_parser, llm=llm)

    def get_promtp(self):
        """
        Get the prompt template.

        Returns:
            PromptTemplate: The prompt template.
        """
        return  self.prompt

    def get_runnable(self,):
        """
        Get the runnable object.

        Parameters:
            parser (Parser): The parser object.

        Returns:
            Runnable: The runnable object.
        """
        return self.get_promtp() | self.model | self.parser
    
    def get_tags(self):
        """
        Get the tags.

        Returns:
            list[str]: The tags.
        """
        return self.tags
    

class Relation(BaseModel):
    class_name_of_first_metamodel: str = Field(..., description="The class name selected from the first metamodel.")
    class_name_of_second_metamodel: str = Field(..., description="The class name selected from the second metamodel.")

class Relations(BaseModel):
    relations: list[Relation] = Field(..., description="The list of relations.")
