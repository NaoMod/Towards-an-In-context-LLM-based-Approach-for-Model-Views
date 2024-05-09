from langchain_core.exceptions import OutputParserException
from langchain_core.output_parsers import BaseOutputParser
from typing import Any

import os
import pathlib
import json

from utils.ecore.parser import EcoreParser

VIEWS_DIRECTORY = os.path.join(pathlib.Path(__file__).parent.absolute(), "..", "..", "Views_Baseline")

class EcoreClassesParser(BaseOutputParser):

    meta_1: str = None
    meta_2: str = None

    # def __init__(self, meta_1, meta_2):
    #     self._meta_1 = meta_1
    #     self._meta_2 = meta_2
    #     self._ecore_parser = EcoreParser()
        

    def parse(self, output: str) -> dict:
        ecore_parser = EcoreParser()
        try:
            r = json.dumps(output)
            relations_to_check = json.loads(r)
        except json.JSONDecodeError as e:
            raise OutputParserException(
                    f"Error parsing JSON output: {e}"
                )
        for relation in relations_to_check:
            classes = list(relation.values())[0]        
            class_name_1 = classes[0]
            meta_1_checked = ecore_parser.check_ecore_class(self._meta_1, class_name_1)
            
            class_name_2 = classes[1]
            meta_2_checked = ecore_parser.check_ecore_class(self._meta_2, class_name_2)
            if not meta_1_checked or not meta_2_checked:
                return False
        return True
    
    @property
    def _type(self) -> str:
        return "ecore_classes_parser"