from operator import itemgetter

from utils.config import Config
from langchain.schema import StrOutputParser
from langchain_core.output_parsers import JsonOutputParser

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
join_cfg = {"tags": join_runnable.get_tags()}

# join_result = join_chain.invoke(
#     {
#         "user_input": "I want to combine the the two metamodels to have a single overview of the domain.",
#         "meta_1": meta_book, 
#         "meta_2": meta_publ
#     },
#     config=join_cfg)

# print(join_result)

select_runnable = Select()
select_chain = select_runnable.get_runnable(json_parser)
cfg = {"tags": select_runnable.get_tags()}

# select_result = select_chain.invoke(
#     {"meta_1": meta_book, "meta_2": meta_publ}, 
#     config=cfg
# ).split("\n")

# print(select_result)

# where_runnable = Where()
# where_chain = where_runnable.get_runnable(text_parser)
# where_cfg = {"tags": where_runnable.get_tags()}

# where_result = where_chain.invoke(
#     {"meta_1": meta_book, "meta_2": meta_publ},
#     config=where_cfg).split("\n")

# print(where_result)

full_chain = {
        "relations": join_chain,
        "meta_1": itemgetter("meta_1"),
        "meta_2": itemgetter("meta_2"),
        "user_input": itemgetter("user_input"),
        } | select_chain

full_result = full_chain.invoke(
    {
        "user_input": "I want to combine the the two metamodels to have a single overview of the domain.",
        "meta_1": meta_book, 
        "meta_2": meta_publ
    },
    config=join_cfg)

print(full_result)
