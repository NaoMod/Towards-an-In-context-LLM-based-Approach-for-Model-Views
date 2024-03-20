from operator import itemgetter
import json
import os
import pathlib

from langchain.schema import StrOutputParser
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

from utils.config import Config
from runnables.select import Select
from runnables.join import Join
from runnables.where import Where
from utils.ecore.parser import EcoreParser

from langchain_community.document_loaders import TextLoader

# Configure everything
config = Config()
config.load_keys()
llm = config.get_llm()
open_ai_key = config.get_open_ai_key()

text_parser = llm | StrOutputParser()
json_parser = llm | JsonOutputParser()

meta_book_loader = TextLoader(os.path.join(pathlib.Path(__file__).parent.absolute(),"..", "temp", "Book.txt"))
meta_book = meta_book_loader.load()

meta_publ_loader = TextLoader(os.path.join(pathlib.Path(__file__).parent.absolute(),"..", "temp", "Publication.txt"))
meta_publ = meta_publ_loader.load()

join_runnable = Join()
join_chain = join_runnable.get_runnable(json_parser)
cfg = {"tags": join_runnable.get_tags()}

select_runnable = Select()
select_chain = select_runnable.get_runnable(json_parser)
cfg['tags'] += select_runnable.get_tags()


where_runnable = Where()
where_chain = where_runnable.get_runnable(text_parser)
cfg['tags'] += where_runnable.get_tags()

def check_if_classes_exists(relations):
    r = json.dumps(relations)
    relations_to_check = json.loads(r)
    parser = EcoreParser()
    for relation in relations_to_check:
        classes = list(relation.values())[0]
        metamodel_name_1 = meta_book[0].metadata["source"].replace(".txt", ".ecore")
        class_name_1 = classes[0]
        meta_1_checked = parser.check_ecore_class(metamodel_name_1, class_name_1)

        metamodel_name_2 = meta_publ[0].metadata["source"].replace(".txt", ".ecore")
        class_name_2 = classes[1]
        meta_2_checked = parser.check_ecore_class(metamodel_name_2, class_name_2)
        if not meta_1_checked or not meta_2_checked:
            return False
    return True

full_chain = RunnablePassthrough.assign(relations=join_chain) | {
        "meta_1": itemgetter("meta_1"),
        "meta_2": itemgetter("meta_2"),
        "user_input": itemgetter("user_input"),
        "relations": itemgetter("relations"),
        "select": RunnablePassthrough.assign(select=select_chain) } | RunnablePassthrough.assign(combinations=where_chain)

full_result = full_chain.invoke(
    {
        "user_input": "I want to combine the the two metamodels to have a overview of the domain.",
        "meta_1": meta_book, 
        "meta_2": meta_publ
    },
    config=cfg)

if check_if_classes_exists(full_result['relations']):
    print("Classes exists")
    print(full_result['relations'])
    print(full_result['select']['select'])
    print(full_result['combinations'])
else:  
    print("Classes do not exist")


