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
   
    def _get_metamodel_containing_class_name(self, class_name: str, meta_1_path: str, meta_2_path: str) -> str:
        ecore_parser = EcoreParser()
        check_metamodel_1 = ecore_parser.check_ecore_class(meta_1_path, class_name)
        check_metamodel_2 = ecore_parser.check_ecore_class(meta_2_path, class_name)

        if check_metamodel_1:
            return meta_1_path
        elif check_metamodel_2:
            return meta_2_path 

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

        return output
    
    @property
    def _type(self) -> str:
        """"
        Return the type of the parser.
        """
        return "ecore_attributes_parser"