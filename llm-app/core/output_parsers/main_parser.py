import pydantic  # pydantic: ignore

from langchain_core.exceptions import OutputParserException
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.output_parsers.pydantic import _PYDANTIC_FORMAT_INSTRUCTIONS
from langchain_core.utils.pydantic import PYDANTIC_MAJOR_VERSION

from typing import Generic, TypeVar, Union
from pydantic.v1 import BaseModel
from json import dumps

if PYDANTIC_MAJOR_VERSION < 2:
    PydanticBaseModel = pydantic.BaseModel

else:
    from pydantic.v1 import BaseModel  # pydantic: ignore

    # Union type needs to be last assignment to PydanticBaseModel to make mypy happy.
    PydanticBaseModel = Union[BaseModel, pydantic.BaseModel]  # type: ignore

TBaseModel = TypeVar("TBaseModel", bound=PydanticBaseModel)


class MainParser(JsonOutputParser, Generic[TBaseModel]):
    
    def _parse_obj(self, obj: dict) -> TBaseModel:
        """Parse the output of an LLM call to a pydantic object.

        Args:
            obj: The output of the LLM call.
            
        Returns:
            The parsed pydantic object.

        Raises:
            OutputParserException: If the output cannot be parsed.
        """
        if PYDANTIC_MAJOR_VERSION == 2:
            try:
                if issubclass(self.pydantic_object, pydantic.BaseModel):
                    return self.pydantic_object.model_validate(obj)
                elif issubclass(self.pydantic_object, pydantic.v1.BaseModel):
                    return self.pydantic_object.parse_obj(obj)
                else:
                    raise OutputParserException(
                        f"Unsupported model version for PydanticOutputParser: \
                            {self.pydantic_object.__class__}"
                    )
            except (pydantic.ValidationError, pydantic.v1.ValidationError) as e:
                raise self._parser_exception(e, obj)
        else:  # pydantic v1
            try:
                return self.pydantic_object.parse_obj(obj)
            except pydantic.ValidationError as e:
                raise self._parser_exception(e, obj)
            
    def _parser_exception(
        self, e: Exception, json_object: dict
    ) -> OutputParserException:
        json_string = dumps(json_object)
        name = self.pydantic_object.__name__
        msg = f"Failed to parse {name} from completion {json_string}. Got: {e}"
        return OutputParserException(msg, llm_output=json_string)
    
    def parse(self, output) -> TBaseModel:
        """Parse the output of an LLM call to a pydantic object.

        Args:
            text: The output of the LLM call.

        Returns:
            The parsed pydantic object.
        """                    
        completion = output.content       
        return super().parse(completion)
    
    def get_format_instructions(self) -> str:
        """ 
        Get the format instructions for the Pydantic object.
        
        Returns:
            str: The format instructions.
        """
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