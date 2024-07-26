from langchain_core.exceptions import OutputParserException
from langchain_core.outputs import Generation

from typing import List, Type

from utils.ecore.parser import EcoreParser
from .main_parser import MainParser, TBaseModel

class EcoreClassesParser(MainParser):
    """	
    EcoreClassesParser class for managing the ecore classes parser
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
        return self._parse_relations(json_object)
    
    def _parse_relations(self, output) -> dict:
        ecore_parser = EcoreParser()
        for relation in output['relations']:                           
                       
            class_name_1 = relation['classes'][0]
            meta_1_checked = ecore_parser.check_ecore_class(self.meta_1, class_name_1)
            
            class_name_2 = relation['classes'][1]
            meta_2_checked = ecore_parser.check_ecore_class(self.meta_2, class_name_2)
            if not meta_1_checked or not meta_2_checked:
                raise OutputParserException(
                    f"The output contains an invalid class: {class_name_1 if not meta_1_checked else class_name_2}"
                )
        return output
    
    @property
    def _type(self) -> str:
        return "ecore_classes_parser"