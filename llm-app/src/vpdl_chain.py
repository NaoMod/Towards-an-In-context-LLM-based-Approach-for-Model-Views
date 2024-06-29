from operator import itemgetter

from langchain_core.runnables import RunnablePassthrough

from runnables.views.select import Select
from runnables.views.join import Join
from runnables.views.where import Where

from utils.ecore.parser import EcoreParser

from loaders.ecore_loader import EcoreLoader

ecore_parser = EcoreParser()

def generate_vpdl_skeleton_wrapper(input_:dict):
    return generate_vpdl_skeleton(input_, input_['meta_1_path'], input_['meta_2_path'])

def generate_vpdl_skeleton(input_vpdl, meta_1, meta_2):

    meta_1_uri, meta_1_prefix = ecore_parser.get_metamodel_uri(meta_1)
    meta_2_uri, meta_2_prefix = ecore_parser.get_metamodel_uri(meta_2)

    vpdl_skeleton = "create view NAME as\n\nselect "
    
    # FILTERS (SELECT clause)
    for meta_name, filters in input_vpdl['select']['filters'].items():

        for cls_name, attributes in filters.items():
            for attr in attributes:
                vpdl_skeleton += f"{meta_name}.{cls_name}.{attr},\n"
    
    # JOIN
    for relation in input_vpdl['join']['relations']:
                   
        class_name_1 = relation['classes'][0]
        class_name_2 = relation['classes'][1]
    
        vpdl_skeleton += f"{meta_1_prefix}.{class_name_1} join {meta_2_prefix}.{class_name_2} as {relation['name']},\n"
    
    # including the metamodels and its identifiers
    vpdl_skeleton += f"\n\nfrom '{meta_1_uri}' as {meta_1_prefix},\n     {meta_2_uri}' as {meta_2_prefix},\n\nwhere "
    
    # Adding join conditions (WHERE clause)
    for combination in input_vpdl['where']['rules']:
        relation_name = combination['name']
        combination_rules_list = combination['rules']
        rules = ""        
        for rule in combination_rules_list:            
            rules += f"`{rule['combination_rule']}`\n      "
        vpdl_skeleton += f"{rules} for {relation_name}\n"
        
    return vpdl_skeleton

def execute_chain(llm, view_description , meta_1_path, meta_2_path, pe_type = "zsCoT"):

    # LOADERS
    meta_1_loader = EcoreLoader(meta_1_path)    
    meta_1 = meta_1_loader.load()
    meta_1_content = meta_1[0].page_content

    meta_2_loader = EcoreLoader(meta_2_path)
    meta_2 = meta_2_loader.load()
    meta_2_content = meta_2[0].page_content

    join_runnable = Join(pe_type)
    join_runnable.set_model(llm)
    join_runnable.set_parser(meta_1=meta_1_path, meta_2=meta_2_path)
    join_runnable.set_prompt()
    join_chain = join_runnable.get_runnable()
    cfg = {"tags": join_runnable.get_tags()}

    select_runnable = Select(pe_type)
    select_runnable.set_model(llm)
    select_runnable.set_parser(meta_1=meta_1_path, meta_2=meta_2_path)
    select_runnable.set_prompt()
    select_chain = select_runnable.get_runnable()
    cfg['tags'] += select_runnable.get_tags()

    where_runnable = Where(pe_type)
    where_runnable.set_model(llm)
    where_runnable.set_parser()
    where_runnable.set_prompt()
    where_chain = where_runnable.get_runnable()
    cfg['tags'] += where_runnable.get_tags()

    full_chain = RunnablePassthrough.assign(join=join_chain).with_config({"run_name": "JOIN"}) | {
            "meta_1": itemgetter("meta_1"),
            "meta_2": itemgetter("meta_2"),
            "meta_1_path": itemgetter("meta_1_path"),
            "meta_2_path": itemgetter("meta_2_path"),
            "view_description": itemgetter("view_description"),
            "join": itemgetter("join"),
            } | RunnablePassthrough.assign(select=select_chain).with_config({"run_name": "SELECT"}) | \
                RunnablePassthrough.assign(where=where_chain).with_config({"run_name": "WHERE"}) | \
                RunnablePassthrough.assign(vpdl_draft=generate_vpdl_skeleton_wrapper).with_config({"run_name": "VPDL_DRAFT"})
    

    full_result = full_chain.invoke(
        {
            "view_description": view_description ,
            "meta_1": meta_1_content, 
            "meta_2": meta_2_content,
            "meta_1_path": meta_1_path,
            "meta_2_path": meta_2_path
        },
        config=cfg)

    print(full_result['join'])
    print(full_result['select'])
    print(full_result['where'])
    print(full_result['vpdl_draft'])

    return full_result