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

VIEWS_DIRECTORY = os.path.join(pathlib.Path(__file__).parent.absolute(), "..", "..", "Views_Baseline")

class EcoreAttributesParser(BaseCumulativeTransformOutputParser[Any]):

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
            filters_to_check = self.parse_result([Generation(text=output)])
            if filters_to_check is None:
                raise OutputParserException(
                    f"Error parsing JSON output: {e}"
                )
        except Exception as e:
            raise e
        filters_for_meta_1 = filters_to_check[0]
        filters_for_meta_2 = filters_to_check[1]
        for _, filters_1 in filters_for_meta_1.items():
            for class_to_test, attributes in filters_1.items():
                for attr in attributes:
                    attr_checked = ecore_parser.check_ecore_attribute(self.meta_1, class_to_test, attr)
                    if not attr_checked:
                        raise OutputParserException(
                            f"The output contains an invalid attribute: {attr}"
                        )

        for _, filters_2 in filters_for_meta_2.items():
            for class_to_test, attributes in filters_2.items():
                for attr in attributes:
                    attr_checked = ecore_parser.check_ecore_attribute(self.meta_2, class_to_test, attr)
                    if not attr_checked:
                        raise OutputParserException(
                            f"The output contains an invalid attribute: {attr}"
                        )            
        return filters_to_check
    
    def get_format_instructions(self) -> str:
        #TODO: Not using this method. Needs change if used
        return "Return a JSON object."
    
    @property
    def _type(self) -> str:
        return "ecore_attributes_parser"