from langchain_core.exceptions import OutputParserException
from langchain_core.outputs import Generation

from typing import List, Type

from utils.ecore.parser import EcoreParser
from .main_parser import MainParser, TBaseModel

class EcoreAttributesParser(MainParser):
    """	
    EcoreAttributesParser class for managing the ecore attributes parser
    """
    meta_1: str = None
    meta_2: str = None
    pydantic_object: Type[TBaseModel]  # type: ignore
    """The pydantic model to parse."""

    def parse_result(
        self, result: List[Generation], *, partial: bool = False
    ) -> TBaseModel:
        """Parse the result of an LLM call to a pydantic object.

        Args:
            result: The result of the LLM call.
            partial: Whether to parse partial JSON objects.
                If True, the output will be a JSON object containing
                all the keys that have been returned so far.
                Defaults to False.

        Returns:
            The parsed pydantic object.
        """
        json_object = super().parse_result(result)
        self._parse_obj(json_object)
        return self._parse_attributes(json_object)        

    def _parse_attributes(self, output: str) -> dict:
        """
        Parse the output.
        """
        ecore_parser = EcoreParser()
                  
        for _ , filters in output['filters'].items():
            for cls_name, attributes in filters.items():
                # find the metamodel of the given class
                check_metamodel_1 = ecore_parser.check_ecore_class(self.meta_1, cls_name)
                check_metamodel_2 = ecore_parser.check_ecore_class(self.meta_2, cls_name)
                if check_metamodel_1:
                    meta_path = self.meta_1
                elif check_metamodel_2:
                    meta_path = self.meta_2
                for attr in attributes:
                    # if attribute is *, it's not necessary to check existence
                    if attr != "*":
                        # check if attribute exist in the given metamodel and throw exception when it's not
                        attr_checked = ecore_parser.check_ecore_attribute(meta_path, cls_name, attr)
                        if not attr_checked:
                            raise OutputParserException(
                                f"The output contains an invalid attribute {attr} for class: {cls_name} in metamodel: {meta_path}"
                            )

        return output
    
    @property
    def OutputType(self) -> Type[TBaseModel]:
        """Return the pydantic model."""
        return self.pydantic_object
    
    @property
    def _type(self) -> str:
        """"
        Return the type of the parser.
        """
        return "ecore_attributes_parser"