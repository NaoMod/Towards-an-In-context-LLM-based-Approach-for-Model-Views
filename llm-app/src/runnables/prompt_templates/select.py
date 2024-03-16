prompts = {
    "items": [
        {
            'tags': ['zero-shot'], 
            'template': """You are a computer program specialized in reason on PlantUML metamodels, especially combining and merging them into objects called Views.\
                    Given the following two metamodels, your task is to define which elements should be selected to be present in the final View.\
                    Your answer should be a list of elements.\
                    Each element is in the following format: Metamodel_Identifier.Class_name.Attributte.\
                    Only use class and attribute names that actually exist in the metamodels; don't try to invent new names.\
                    Note that frequently, the metamodels can represent the same domain, so it's possible to get some overlap between them.\
                    This should be taken into account to avoid repeating information. \

                    Metamodel 1: {meta_1}\
                    Metamodel 2: {meta_2}\
                    Select elements:""",
        },
    ]
        
}
    
