from langchain_core.exceptions import OutputParserException
from langchain_core.outputs import Generation
from langchain_core.output_parsers import BaseCumulativeTransformOutputParser
from langchain_core.output_parsers.json import parse_json_markdown
from langchain_core.output_parsers.pydantic import _PYDANTIC_FORMAT_INSTRUCTIONS

from typing import Any, List, Optional, Dict

from langchain_core.pydantic_v1 import BaseModel, Field

from json import JSONDecodeError, dumps
import jsonpatch  # type: ignore[import]

from utils.ecore.parser import EcoreParser

class RelationWithClassesAttributes(BaseModel):
    name: str = Field(..., description="Name of the relation")
    classAttributes: Dict[str, List[str]] = Field(..., description="Dictionary with the class name as key and a list of attributes as value")

class Filters(BaseModel):
    filters: List[RelationWithClassesAttributes] = Field(..., description="List of relations with their classes and respective attributes")

class EcoreAttributesParser(BaseCumulativeTransformOutputParser[Any]):
    """	
    EcoreAttributesParser class for managing the ecore attributes parser.
    """
    meta_1: str = None
    meta_2: str = None
    pydantic_object: BaseModel = Filters

    def _diff(self, prev: Optional[Any], next: Any) -> Any:
        """"
        Return the difference between the previous and the next output.
        """
        return jsonpatch.make_patch(prev, next).patch
    
    def parse_result(self, result: List[Generation], *, partial: bool = False) -> Any:
        """
        Parse the result of the output.
        """
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
        """
        Parse the output.
        """
        ecore_parser = EcoreParser()
        try:
            filters_to_check = self.parse_result([Generation(text=output)])
            if filters_to_check is None:
                raise OutputParserException(
                    f"Error parsing JSON output: {e}"
                )
        except Exception as e:
            raise e
        for filter_per_relation in filters_to_check['filters']:

            # relation_name = filter_per_relation['name'] # not used
            class_attributes = filter_per_relation['classAttributes']
            for class_to_test, attributes in class_attributes.items():
                for attr in attributes:
                    attr_checked = ecore_parser.check_ecore_attribute(self.meta_1, class_to_test, attr)
                    if not attr_checked:
                        raise OutputParserException(
                            f"The output contains an invalid attribute: {attr}"
                        )

        #     filters_for_meta_1 = filter_to_check[0]
        #     filters_for_meta_2 = filter_to_check[1]
        #     for _, filters_1 in filters_for_meta_1.items():
        #         for class_to_test, attributes in filters_1.items():
        #             for attr in attributes:
        #                 attr_checked = ecore_parser.check_ecore_attribute(self.meta_1, class_to_test, attr)
        #                 if not attr_checked:
        #                     raise OutputParserException(
        #                         f"The output contains an invalid attribute: {attr}"
        #                     )

        # for _, filters_2 in filters_for_meta_2.items():
        #     for class_to_test, attributes in filters_2.items():
        #         for attr in attributes:
        #             attr_checked = ecore_parser.check_ecore_attribute(self.meta_2, class_to_test, attr)
        #             if not attr_checked:
        #                 raise OutputParserException(
        #                     f"The output contains an invalid attribute: {attr}"
        #                 )            
        return filters_to_check
    
    def get_format_instructions(self) -> str:
        # The code below was adapted from the Pydantic output parser in LangChain library.
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
        """"
        Return the type of the parser.
        """
        return "ecore_attributes_parser"