import os

from typing import Optional, Type
from langchain.tools import BaseTool
from langchain.pydantic_v1 import BaseModel, Field

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)

from ecore_utils.plant_uml_translate import PlantUMLTranslate
from pyecore.resources import ResourceSet


class MetamodelInput(BaseModel):
    mm_path: str = Field(description="Path to get the ecore metamodel file")

class EcorePlantUMLTool(BaseTool):
    """
    Convert an Ecore file to PlantUML format and save it as a .txt file in the temp folder.
    """

    name = "ecore_plant_uml"
    description = "Useful for when you need to verify if a given class exists in a specific metamodel."
    args_schema: Type[BaseModel] = MetamodelInput

    def _run(
        self, mm_path: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """
        Convert an Ecore file to PlantUML format synchronously.

        Parameters
        ----------
        mm_path : str
            The path to the Ecore file.
        run_manager : Optional[CallbackManagerForToolRun], optional
            The run manager for the tool, by default None.

        Returns
        -------
        str
            The path to the generated PlantUML file.
        """
        # Check if PlantUML file already exists
        if os.path.exists(f"../temp/{mm_path.split('/')[-1].split('.')[0]}.txt"):
            return f"../temp/{mm_path.split('/')[-1].split('.')[0]}.txt"
        else:
            rset = ResourceSet()
            metamodel_resource = rset.get_resource(mm_path)
            root = metamodel_resource.contents[0]
            plantuml = '@startuml\n'
            translate = PlantUMLTranslate()
            translate.generate(root)
            plantuml += translate.uml_string
            plantuml += '@enduml'
            with open(f"../temp/{mm_path.split('/')[-1].split('.')[0]}.txt", "w") as file:
                file.write(plantuml)
            return f"../temp/{mm_path.split('/')[-1].split('.')[0]}.txt"

    async def _arun(
        self, mm_path: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """
        Convert an Ecore file to PlantUML format asynchronously.

        Parameters
        ----------
        mm_path : str
            The path to the Ecore file.
        run_manager : Optional[AsyncCallbackManagerForToolRun], optional
            The run manager for the tool, by default None.

        Returns
        -------
        str
            The path to the generated PlantUML file.

        Raises
        ------
        NotImplementedError
        """
        raise NotImplementedError("ecore_to_plant_uml does not support async")
