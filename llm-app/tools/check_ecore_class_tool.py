import json

from langchain.pydantic_v1 import BaseModel, Field
from langchain.agents import tool, Tool

from utils.ecore.parser import EcoreParser

class CheckInput(BaseModel):
    metamodel_name: str = Field(description="Name of the metamodel to be checked")
    class_to_test: str = Field(description="Class to be tested  and check if it exists in the metamodel")

class CheckEcoreClassTool():
    """
    CheckEcoreClassTool class.
    """

    @staticmethod
    @tool("check_ecore_class")
    def check_ecore_class(metamodel_check: str) -> bool:
        """
        Run the tool synchronously to verify if the class exists.

        Parameters
        ----------
        metamodel_name : str
            The path to the Ecore file.
        class_to_test : str
            The class to test.

        Returns
        -------
        bool
            True if the Ecore class is found, False otherwise.
        """
        parser = EcoreParser()
        metamodel_check_dict = json.loads(metamodel_check)
        return parser.check_ecore_class(metamodel_check_dict["metamodel_name"], metamodel_check_dict["class_to_test"])
    
    def get_tool(self) -> Tool:
        """
        Get the tool.

        Returns
        -------
        Tool
            The tool.
        """
        return Tool(
            func=CheckEcoreClassTool.check_ecore_class,
            name="check_ecore_class",
            description="Useful for when you need to verify if a given class exists in a specific Ecore metamodel",
        )