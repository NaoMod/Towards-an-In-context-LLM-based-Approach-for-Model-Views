from typing import Optional, Type
from langchain.tools import BaseTool
from langchain.pydantic_v1 import BaseModel, Field

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)

from utils.ecore.ecore_parser import EcoreParser

class CheckInput(BaseModel):
    ecore_path: str = Field(description="Path to get the ecore metamodel file")
    class_to_test: str = Field(description="Class to test if it exists in the metamodel")

class CheckEcoreClassTool(BaseTool):
    """
    CheckEcoreClassTool class.
    """

    name = "check_ecore_class"
    description = "Useful for when you need."
    args_schema: Type[BaseModel] = CheckInput

    def _run(
        self, ecore_path: str, class_to_test: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> bool:
        """
        Run the tool synchronously.

        Parameters
        ----------
        ecore_path : str
            The path to the Ecore file.
        class_to_test : str
            The class to test.
        run_manager : Optional[CallbackManagerForToolRun], optional
            The run manager for the tool run, by default None.

        Returns
        -------
        bool
            True if the Ecore class is found, False otherwise.
        """
        parser = EcoreParser()
        return parser.check_ecore_class(ecore_path, class_to_test)
    
    async def _arun(
        self, ecore_path: str, class_to_test: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> bool:        
        """
        Run the tool asynchronously.

        Parameters
        ----------
        ecore_path : str
            The path to the Ecore file.
        class_to_test : str
            The class to test.
        run_manager : Optional[AsyncCallbackManagerForToolRun], optional
            The run manager for the tool run, by default None.

        Returns
        -------
        bool
            True if the Ecore class is found, False otherwise.

        Raises
        ------
        NotImplementedError
        """
        raise NotImplementedError("check_ecore_class does not support async")