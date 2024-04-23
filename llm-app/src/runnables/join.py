from langchain.output_parsers import PydanticOutputParser
from langchain import hub
from langchain_core.pydantic_v1 import BaseModel, Field

from .prompt_templates.join import prompts as join_templates

class Join():
    """
    Join class for managing the Join prompt templates.
    """

    def __init__(self,):
        """
        Initialize the Join class.
        """
        self.tags = join_templates["items"][0]["tags"]
        self.template = hub.pull("james-mir/join-for-vpdl")

    def get_template(self):
        """
        Get the prompt template.

        Returns:
            PromptTemplate: The prompt template.
        """
        return  self.template

    def get_runnable(self, llm, parser=None):
        """
        Get the runnable object.

        Parameters:
            parser (Parser): The parser object.

        Returns:
            Runnable: The runnable object.
        """
        if parser is None:
            parser = PydanticOutputParser(pydantic_object=Relations)

        return self.get_template() | llm| parser
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
