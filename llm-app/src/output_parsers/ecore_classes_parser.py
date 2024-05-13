from langchain_core.exceptions import OutputParserException
from langchain_core.outputs import Generation
from langchain_core.output_parsers import BaseCumulativeTransformOutputParser
from langchain_core.output_parsers.json import parse_json_markdown
from langchain_core.output_parsers.pydantic import _PYDANTIC_FORMAT_INSTRUCTIONS

from typing import Any, List, Optional

from langchain_core.pydantic_v1 import BaseModel, Field

from json import JSONDecodeError, dumps

import jsonpatch  # type: ignore[import]

from utils.ecore.parser import EcoreParser

class Relation(BaseModel):
    name: str = Field(..., description="Name of the relation")
    classes: List[str] = Field(..., description="Strings representing two classes coming from two different metamodels")

class RelationsGroup(BaseModel):
    relations: List[Relation] = Field(..., description="List of relations")

class EcoreClassesParser(BaseCumulativeTransformOutputParser[Any]):

    meta_1: str = None
    meta_2: str = None
    pydantic_object: BaseModel = RelationsGroup

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
        for relation in relations_to_check['relations']:                           
                       
            class_name_1 = relation['classes'][0]
            meta_1_checked = ecore_parser.check_ecore_class(self.meta_1, class_name_1)
            
            class_name_2 = relation['classes'][1]
            meta_2_checked = ecore_parser.check_ecore_class(self.meta_2, class_name_2)
            if not meta_1_checked or not meta_2_checked:
                raise OutputParserException(
                    f"The output contains an invalid class: {class_name_1 if not meta_1_checked else class_name_2}"
                )
        return relations_to_check
    
    def get_format_instructions(self) -> str:
        #TODO: Not using this method. Needs change if used
        # return f"Format the output as a {self.pydantic_object.__name__} instance."
        # Copy schema to avoid altering original Pydantic schema.
        schema = {k: v for k, v in self.pydantic_object.schema().items()}

        # Remove extraneous fields.
        reduced_schema = schema
        if "title" in reduced_schema:
            del reduced_schema["title"]
        if "type" in reduced_schema:
            del reduced_schema["type"]
        # Ensure json in context is well-formed with double quotes.
        schema_str = dumps(reduced_schema)

        return _PYDANTIC_FORMAT_INSTRUCTIONS.format(schema=schema_str)
    
    @property
    def _type(self) -> str:
        return "ecore_classes_parser"