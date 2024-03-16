from utils.config import Config
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser

from langchain_community.document_loaders import TextLoader

# Configure everything
config = Config()
config.load_keys()
llm = config.get_llm()
open_ai_key = config.get_open_ai_key()

simple_parser = llm | StrOutputParser()

meta_book_loader = TextLoader("../temp/Book.txt")
meta_book = meta_book_loader.load()

meta_publ_loader = TextLoader("../temp/Publication.txt")
meta_publ = meta_publ_loader.load()

join_template = """You are a computer program specialized in reason on PlantUML metamodels, especially combining and merging them into objects called Views.\
Given the following two metamodels and assuming the same domain semantically relates them,\
your task is to define which elements can be combined in the final View. In a View, the elements are combined in pairs.\
Combining two elements means that the View will include a single element representing the same domain object but combining attributes from each metamodel.
Your answer should be a list of elements.\
Each element of the list is a dictionary containing the name of this virtual relation and a tuple with the combined elements in the following format: {{Relation_name: (Metamodel_Identifier.Class_name, Metamodel_Identifier.Class_name)}}\
Only use class names that actually exist in the metamodels; don't try to invent new class names. The relation's name should combine these class names, always in camelCase.\

Metamodel 1: {meta_1}\
Metamodel 2: {meta_2}\
Relations:"""

join_prompt = PromptTemplate.from_template(join_template)

join_chain = (join_prompt | simple_parser)

join_result = join_chain.invoke({"meta_1": meta_book, "meta_2": meta_publ}).split("\n")

print(join_result)

select_template = """You are a computer program specialized in reason on PlantUML metamodels, especially combining and merging them into objects called Views.\
Given the following two metamodels, your task is to define which elements should be selected to be present in the final View.\
Your answer should be a list of elements.\
Each element is in the following format: Metamodel_Identifier.Class_name.Attributte.\
Only use class and attribute names that actually exist in the metamodels; don't try to invent new names.\
Note that frequently, the metamodels can represent the same domain, so it's possible to get some overlap between them.\
This should be taken into account to avoid repeating information. \

Metamodel 1: {meta_1}\
Metamodel 2: {meta_2}\
Select elements:"""

select_prompt = PromptTemplate.from_template(select_template)

select_chain =(select_prompt | simple_parser)

select_result = select_chain.invoke({"meta_1": meta_book, "meta_2": meta_publ}).split("\n")

print(select_result)

where_template = """You are a computer program specialized in reason on PlantUML metamodels, especially combining and merging them into objects called Views.\
Given the following two metamodels, your task is to define how to combine them.\
It means you need to define the conditions to combine elements from both metamodels.\
Your answer should be a list of conditions.\
Each condition is in the following format: Metamodel_Identifier.Class_name.Attributte {{combination_rule}} Metamodel_Identifier.Class_name.Attributte\
Only use class and attribute names that actually exist in the metamodels; don't try to invent new names.\
The combination_rule can be one of the following: equal, different, greater, less, greaterOrEqual, lessOrEqual.\
The combination_rule should be chosen according to the semantics of the domain. \

Metamodel 1: {meta_1}\
Metamodel 2: {meta_2}\

Conditions:"""

where_prompt = PromptTemplate.from_template(where_template)

where_chain = (where_prompt | simple_parser)

where_result = where_chain.invoke({"meta_1": meta_book, "meta_2": meta_publ}).split("\n")

print(where_result)

