from langchain.pydantic_v1 import BaseModel, Field

from langchain.agents import tool

from utils.ecore.parser import EcoreParser

class CheckInput(BaseModel):
    metamodel_name: str = Field(description="Name of the metamodel to be checked")
    class_to_test: str = Field(description="Class to be tested  and check if it exists in the metamodel")

class CheckEcoreClassTool():
    """
    CheckEcoreClassTool class.
    """

    @staticmethod
    @tool("check_ecore_class", args_schema=CheckInput)
    def check_ecore_class(metamodel_name: str, class_to_test: str) -> bool:
        """
        Run the tool synchronously.

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
        return parser.check_ecore_class(metamodel_name, class_to_test)
    
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
            description="Useful for when you need to verify if a given class exists in a specific metamodel",
        )