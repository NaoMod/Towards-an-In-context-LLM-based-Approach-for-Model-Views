from langchain.prompts import PromptTemplate
from langchain.output_parsers import OutputFixingParser
from langchain.output_parsers import RetryOutputParser
from langchain_core.runnables import RunnableLambda, RunnableParallel

from .prompt_templates.join import prompts as join_templates
from interfaces.runnable_interface import RunnableInterface

from output_parsers.ecore_classes_parser import EcoreClassesParser, RelationsGroup, Relation

class Join(RunnableInterface):
    """
    Join class for managing the Join prompt templates.
    """

    def __init__(self, pe_type = "zsCoT"):
        """
        Initialize the Join class.
        """
        self.tags = join_templates["items"][pe_type]["tags"]
        self.pe_type = pe_type
        

    def set_model(self, llm):
        self.model = llm        

    def set_parser(self, meta_1 = None, meta_2 = None):        
        # raise error if some of the parameters are missing
        if meta_1 is None or meta_2 is None:
            raise ValueError("Metamodels are required to parse the output using Ecore checkers.")
        basic_parser = EcoreClassesParser(meta_1=meta_1, meta_2=meta_2)
        # self.parser = OutputFixingParser.from_llm(parser=basic_parser, llm=self.model)
        self.parser = RetryOutputParser.from_llm(parser=basic_parser, llm=self.model.with_structured_output(RelationsGroup), max_retries=3)
        

    def set_prompt(self, template = None):
        if template is None:
            self.prompt = PromptTemplate(
                template=join_templates["items"][self.pe_type]["template"],
                input_variables=["view_description", "meta_1", "meta_2"],
                partial_variables={"format_instructions":  self.parser.get_format_instructions()},
            )

    def get_runnable(self):
        """
        Get the runnable object.

        Parameters:
            parser (Parser): The parser object.

        Returns:
            Runnable: The runnable object.
        """
        def parse_with_prompt(args):
            completion = args['completion']
            if (type(completion) is RelationsGroup):
                args = args.copy()
                del args['completion']
                completion = completion.json(ensure_ascii=False)
                args['completion'] = completion

            return self.parser.parse_with_prompt(**args)

        chain = self.prompt | self.model.with_structured_output(RelationsGroup, include_raw=False)
        return RunnableParallel(
            completion=chain, prompt_value=self.prompt
        ) | RunnableLambda(parse_with_prompt)
    
    def get_tags(self):
        """
        Get the tags.

        Returns:
            list[str]: The tags.
        """
        return self.tags
