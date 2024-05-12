from langchain_core.exceptions import OutputParserException
from langchain_core.outputs import Generation
from langchain_core.output_parsers import BaseCumulativeTransformOutputParser
from langchain_core.output_parsers.json import parse_json_markdown
from typing import Any, List, Optional

import os
import pathlib
from json import JSONDecodeError
import jsonpatch  # type: ignore[import]

from utils.ecore.parser import EcoreParser

class EcoreClassesParser(BaseCumulativeTransformOutputParser[Any]):

    meta_1: str = None
    meta_2: str = None

    def _diff(self, prev: Optional[Any], next: Any) -> Any:
        return jsonpatch.make_patch(prev, next).patch
    
    def parse_result(self, result: List[Generation], *, partial: bool = False) -> Any:
        text = result[0].text
        text = text.strip()
        if partial:
            try:
                return parse_json_markdown(text)
            except JSONDecodeError:
                return None
        else:
            try:
                return parse_json_markdown(text)
            except JSONDecodeError as e:
                msg = f"Invalid json output: {text}"
                raise OutputParserException(msg, llm_output=text) from e
        

    def parse(self, output: str) -> dict:
        ecore_parser = EcoreParser()
        try:
            relations_to_check = self.parse_result([Generation(text=output)])
            if relations_to_check is None:
                raise OutputParserException(
                    f"Error parsing JSON output: {e}"
                )
        except Exception as e:
           raise e
        for relation in relations_to_check:
            classes = list(relation.values())[0]        
            class_name_1 = classes[0]
            meta_1_checked = ecore_parser.check_ecore_class(self.meta_1, class_name_1)
            
            class_name_2 = classes[1]
            meta_2_checked = ecore_parser.check_ecore_class(self.meta_2, class_name_2)
            if not meta_1_checked or not meta_2_checked:
                raise OutputParserException(
                    f"The output contains an invalid class: {class_name_1 if not meta_1_checked else class_name_2}"
                )
        return relations_to_check
    
    def get_format_instructions(self) -> str:
        #TODO: Not using this method. Needs change if used
        return "Return a JSON object."
    
    @property
    def _type(self) -> str:
        return "ecore_classes_parser"