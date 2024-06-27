prompts = {
    "items": [
        {
            'tags': ['select-zsCot'], 
            'template': """You specialize in reason on PlantUML metamodels, especially selecting and filtering each class's attributes.
                    
                        Given two metamodels, a view description and a list of relations containing classes' pairs, your task is to select a set of attributes for the metamodels' classes.
                                            
                        An attribute should be selected in the following situations:
                         - The attribute is unique it is unique among two classes in a relation 
                         - The attribute is a container of one of the classes in a relation.
                         - The attribute was explicitly mentioned in the view description.
                         - The attribute helps the user to understand the relation between the classes.

                        For the input relations list, you may assume the following template:

                        {{
                            "relations": [
                                {{
                                    "name": "relationName",
                                    "classes": ["class_name_from_first_metamodel", "class_name_from_second_metamodel"]
                                }}
                            ]
                        }}
                                                                
                        {format_instructions}

                        When generating the response, you should follow these rules:
                         - Only use class and attribute names that actually exist in the metamodels. Don't make them up.
                         - The symbol "*" should be used to indicate that all attributes of a given class should be selected. You can use it only once per class per metamodel.

                        The step-by-step process is as follows:

                        1. For each relation, select the classes to be analyzed. The classes are always combined in pairs, in order, and contain one class from each metamodel.
                        2. For each class, select the attributes that should appear in the final response.
                        3. If the class is contained in another class, the container class and the attribute that collected the class should also appear in the list.
                        4. If the attribute is explicitly mentioned in the view description, it should be included in the list.
                        5. Include other relevant attributes that help the user understand the relation between the classes.
                        6. Create the JSON array with the selected attributes for each metamodel.
                        7. Provide the final answer.

                        Your final answer should contain only the valid JSON and nothing else. Exclude any explanation or delimiter from the final response.

                        View description: {view_description}
                        Metamodel 1: {meta_1}
                        Metamodel 2: {meta_2}
                        List of relations: {join}
                        Select elements:""",
        },
        {
            'tags': ['zero-shot'], 
            'template': """You are a computer program specialized in reason on PlantUML metamodels, especially combining and merging them into objects called Views.
                    Given the following two metamodels, your task is to define which elements should be selected to be present in the final View.
                    Your answer should be a list of elements.
                    Each element is in the following format: Metamodel_Identifier.Class_name.Attributte.
                    Only use class and attribute names that actually exist in the metamodels; don't try to invent new names.
                    Note that frequently, the metamodels can represent the same domain, so it's possible to get some overlap between them.
                    This should be taken into account to avoid repeating information. 

                    Metamodel 1: {meta_1}
                    Metamodel 2: {meta_2}
                    Select elements:""",
        },
    ]
        
}
    
