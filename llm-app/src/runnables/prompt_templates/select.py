prompts = {
    "items": [
        {
            'tags': ['Cot'], 
            'template': """You are a computer program specialized in reasoning on metamodels and its classes and attributes.
                    Your main task is to help a user to select the attributes of a pair of metamodels that are related to a given set of classes.

                    You receive two particular metamodel and a list containing the metamodels identifiers and a list of classes from each metamodel.
                    Your task is to iterate over the list of classes and for each metamodel, select which attributes should be selected.
                    An attrribute should be selected if it is unique among all metamodels or if it is a collection that contains the classes in the initial given list.

                    Your final answer will be a JSON array representing the a list of attributes for each metamodel.

                    For the input list, you may assume the following template for the JSON list of dictionaries representing the combinations of elements from the metamodels:

                    [
                        {{
                        "first_metamodel_indentifier": ["class1", "class2", ...],
                        "second_metamodel_indentifier": ["class1", "class2", ...],
                        }}
                    ]

                    For the output, you should provide a JSON array with the selected attributes for each metamodel following the template:

                    [
                        {{
                        "first_metamodel_indentifier": {{ "class1": ["attribute1", "attribute2", ...], class2: ["attribute1", "attribute2", ...], ...}},
                        "second_metamodel_indentifier": {{ "class1": ["attribute1", "attribute2", ...], class2: ["attribute1", "attribute2", ...], ...}},
                        }}
                    ]

                    When generating the JSON text:
                    * Always define and use the same metamodel_identifier for each metamodel
                    * Only use class and attributes names that actually exist in the metamodels. Don't make them up.

                    Metamodel 1: {meta_1}\
                    Metamodel 2: {meta_2}\
                    List of metamodels classes: {classes_input}
                    Select elements:""",
        },
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
    
