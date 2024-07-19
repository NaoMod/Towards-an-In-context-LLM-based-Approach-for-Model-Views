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

class ClassAttributes(BaseModel):
    __root__: List[str] = Field(..., description="List of class attributes")

class MetamodelClasses(BaseModel):
    __root__: Dict[str, ClassAttributes] = Field(..., description="Dictionary of classes with their attributes. The class name is the key.")

class Filters(BaseModel):
    filters: Dict[str, MetamodelClasses] = Field(..., description="Dictionary of filters with the metamodel name as the key.")

class EcoreAttributesParser(BaseCumulativeTransformOutputParser[Any]):
    """	
    EcoreAttributesParser class for managing the ecore attributes parser.z
    """
    meta_1: str = None
    meta_2: str = None
    pydantic_object: BaseModel = Filters

    def _diff(self, prev: Optional[Any], next: Any) -> Any:
        """"
        Return the difference between the previous and the next output.
        """
        return jsonpatch.make_patch(prev, next).patch
    
    def _get_metamodel_containing_class_name(self, class_name: str, meta_1_path: str, meta_2_path: str) -> str:
        ecore_parser = EcoreParser()
        check_metamodel_1 = ecore_parser.check_ecore_class(meta_1_path, class_name)
        check_metamodel_2 = ecore_parser.check_ecore_class(meta_2_path, class_name)

        if check_metamodel_1:
            return meta_1_path
        elif check_metamodel_2:
            return meta_2_path
    
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
                    
        for _ , filters in filters_to_check['filters'].items():
            for cls_name, attributes in filters.items():
                # find the metamodel of the given class and get the full name f"{metamodel_uri}:{class_name}"
                metamodel_to_test  = self._get_metamodel_containing_class_name(cls_name, self.meta_1, self.meta_2)
                for attr in attributes:
                    # if attribute is *, it's not necessary to check existence
                    if attr != "*":
                        # check if attribute exist in the given metamodel and throw exception when it's not
                        attr_checked = ecore_parser.check_ecore_attribute(metamodel_to_test, cls_name, attr)
                        if not attr_checked:
                            raise OutputParserException(
                                f"The output contains an invalid attribute: {attr}"
                            )

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