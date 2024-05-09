from langchain_core.exceptions import OutputParserException
from langchain_core.output_parsers import BaseOutputParser

import os
import pathlib

from utils.ecore.parser import EcoreParser

VIEWS_DIRECTORY = os.path.join(pathlib.Path(__file__).parent.absolute(), "..", "..", "Views_Baseline")

class VPDLOutputParser(BaseOutputParser[str]]):

    def __init__(self, meta_1, meta_2):
        self.meta_1 = meta_1
        self.meta_2 = meta_2
        self.ecore_parser = EcoreParser()
        

    def parse(self, output: str) -> dict:
        cleaned_text = output.strip()

        metamodel_name_1 = self.meta_1[0].metadata["source"].replace(".txt", ".ecore").replace("PlantUML\\", "").replace("1_", "").replace("2_", "")
        metamodel_name_2 = self.meta_2[0].metadata["source"].replace(".txt", ".ecore").replace("PlantUML\\", "").replace("1_", "").replace("2_", "")

        self.meta_1_uri, meta_1_prefix = self.parser.get_metamodel_uri(metamodel_name_1)
        meta_2_uri, meta_2_prefix = self.parser.get_metamodel_uri(metamodel_name_2)

        vpdl_skeleton = "create view NAME as\n\nselect "