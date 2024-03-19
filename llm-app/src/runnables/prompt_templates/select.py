prompts = {
    "items": [
        {
            'tags': ['select-zsCot'], 
            'template': """You specialize in reason on PlantUML metamodels, especially selecting and filtering each classes attributes.
                    
                    Given two metamodels, a list of relations that contains classes from each one and a user input, your task is to select a set of attributes for each class in the list to meet the user's needs.
                    
                    An attrribute should be selected if it is unique among the two metamodels or if it is a collection that contains the classes in the initial given class list.

                    For the input relations list, you may assume the following template between the delimiter <relations>:

                    <relations>
                        [
                            {{
                                "relationName": ["class_name_of_first_metamodel", "class_name_of_second_metamodel"]
                            }}
                        ]
                    </relations>

                    Your final answer will be a JSON array representing the a list of attributes for each metamodel per relation following the template between the delimiter <filters>.
                    For the output, you should provide a JSON array with the selected attributes for each metamodel following the template:

                    <filters>
                        [
                            {{
                                "relationName": {{
                                    "first_metamodel_name": {{ "class1": ["attribute1", "attribute2", ...], class2: ["attribute1", "attribute2", ...], ...}},
                                    "second_metamodel_name": {{ "class1": ["attribute1", "attribute2", ...], class2: ["attribute1", "attribute2", ...], ...}}
                                }}
                            }}
                        ]
                    </filters>

                    When generating the JSON text:
                    Only use class and attribute names that actually exist in the metamodels. Don't make them up.

                    The step-by-step process is as follows:

                    1. For each relation, select the classes to be analyzed. The classes are always combined in pairs. They are always in order and always contain one class from each metamodel.
                    2. For each class, select the attributes that should appear in the final response to meet the user's needs. 
                    3. Create the JSON array with the selected attributes for each metamodel per relation.
                    4. Provide the final answer.

                    Your final answer should contain only the valid JSON and nothing else. Exclude any explanation or delimiter from the final response.

                    User input: {user_input}
                    Metamodel 1: {meta_1}
                    Metamodel 2: {meta_2}
                    List of relations: {relations}
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
    
