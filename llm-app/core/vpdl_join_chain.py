from core.runnables.views.join import Join
from core.loaders.ecore_loader import EcoreLoader

from utils.ecore.parser import EcoreParser

ecore_parser = EcoreParser()

def execute_chain(llm, view_description, meta_1_path, meta_2_path, pe_type = "baseline", examples_no = 1):

    # LOADERS
    meta_1_loader = EcoreLoader(meta_1_path)    
    meta_1 = meta_1_loader.load()
    meta_1_content = meta_1[0].page_content

    meta_2_loader = EcoreLoader(meta_2_path)
    meta_2 = meta_2_loader.load()
    meta_2_content = meta_2[0].page_content

    join_runnable = Join(prompt_label=pe_type, examples_no=examples_no)
    join_runnable.set_model(llm)
    join_runnable.set_parser(meta_1=meta_1_path, meta_2=meta_2_path)
    join_runnable.set_prompt()
    join_chain = join_runnable.get_runnable()
    cfg = {"tags": join_runnable.get_tags()}

    full_result = join_chain.invoke(
        {
            "view_description": view_description,
            "meta_1": meta_1_content, 
            "meta_2": meta_2_content,
            "meta_1_path": meta_1_path,
            "meta_2_path": meta_2_path
        },
        config=cfg)
   
    print(full_result)

    return full_result