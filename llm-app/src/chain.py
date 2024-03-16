from utils.config import Config
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser

from runnables.select import Select
from runnables.join import Join
from runnables.where import Where

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

join_runnable = Join()
join_chain = join_runnable.get_runnable(simple_parser)
join_cfg = {"tags": join_runnable.get_tags()}

join_result = join_chain.invoke(
    {"meta_1": meta_book, "meta_2": meta_publ},
    config=join_cfg).split("\n")

print(join_result)

select_runnable = Select()
select_chain = select_runnable.get_runnable(simple_parser)
cfg = {"tags": select_runnable.get_tags()}

select_result = select_chain.invoke(
    {"meta_1": meta_book, "meta_2": meta_publ}, 
    config=cfg
).split("\n")

print(select_result)

where_runnable = Where()
where_chain = where_runnable.get_runnable(simple_parser)
where_cfg = {"tags": where_runnable.get_tags()}

where_result = where_chain.invoke(
    {"meta_1": meta_book, "meta_2": meta_publ},
    config=where_cfg).split("\n")

print(where_result)

