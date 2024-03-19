from operator import itemgetter

from langchain.schema import StrOutputParser
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnablePassthrough

from utils.config import Config
from runnables.select import Select
from runnables.join import Join
from runnables.where import Where

from langchain_community.document_loaders import TextLoader

# Configure everything
config = Config()
config.load_keys()
llm = config.get_llm()
open_ai_key = config.get_open_ai_key()

text_parser = llm | StrOutputParser()
json_parser = llm | JsonOutputParser()

meta_book_loader = TextLoader("../temp/Book.txt")
meta_book = meta_book_loader.load()

meta_publ_loader = TextLoader("../temp/Publication.txt")
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

# where_result = where_chain.invoke(
#     {"meta_1": meta_book, "meta_2": meta_publ},
#     config=where_cfg).split("\n")

# print(where_result)


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

print(full_result['relations'])
print(full_result['select']['select'])
print(full_result['combinations'])
