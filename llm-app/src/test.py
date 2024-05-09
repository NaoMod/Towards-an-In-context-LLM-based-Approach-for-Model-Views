from langchain_core.exceptions import OutputParserException  
from langchain_core.output_parsers import BaseOutputParser 
from pydantic import Field
  
class BooleanOutputParser(BaseOutputParser[bool]):  
 
    true_val: str = Field("YES", description="Value representing True")
    false_val: str = Field("NO", description="Value representing False")
  
    # def __init__(self, true_val: str = "YES", false_val: str = "NO"):
    #     super().__init__()
    #     self.true_val = true_val
    #     self.false_val = false_val
    
    def parse(self, text: str) -> bool:  
        cleaned_text = text.strip().upper()  
        if cleaned_text not in (self.true_val.upper(), self.false_val.upper()):  
            raise OutputParserException(  
                f"BooleanOutputParser expected output value to either be "  
                f"{{self.true_val}} or {{self.false_val}} (case-insensitive). "  
                f"Received {{cleaned_text}}."  
            )  
        return cleaned_text == self.true_val.upper()  
    
    @property  
    def _type(self) -> str:  
        return "boolean_output_parser"
    
parser = BooleanOutputParser()
parser.invoke("YES")