prompts = {
    "items": {
        "baseline": {
            'tags': ['CoT'], 
            'template': """You specialize in reasoning about PlantUML metamodels, particularly in selecting and filtering each class's attributes.

                # TASK
                Given two metamodels, a view description, and a list of relations containing class pairs, your task is to select a set of attributes for the metamodels' classes.

                An attribute should be selected in the following situations:
                - The attribute is unique among two classes in a relation.
                - The attribute is a container of one of the classes in a relation.
                - The attribute was explicitly mentioned in the view description.
                - The attribute helps the user to understand the relation between the classes.

                You may assume the following template for the input relations list:
                
                {{
                    "relations": [
                        {{
                            "name": "relationName",
                            "classes": ["class_name_from_first_metamodel", "class_name_from_second_metamodel"]
                        }}
                    ]
                }}
                

                # OUTPUT DATA FORMAT
                {format_instructions}

                # RULES
                When generating the response, follow these rules:
                - Only use class and attribute names that actually exist in the metamodels. Don't make them up.
                - The symbol "*" indicates that all attributes of a given class should be selected. Use it only once per class per metamodel, and it replaces all other selected attributes.

                # STEP-BY-STEP PROCESS
                1. For each relation, select the classes to be analyzed. The classes are always combined in pairs, in order, and contain one class from each metamodel.
                2. For each class, select the attributes that should appear in the final response.
                3. If the class is contained in another class, include the container class and the attribute that references the contained class.
                4. If an attribute is explicitly mentioned in the view description, include it in the list.
                5. Include other relevant attributes that help the user understand the relation between the classes.
                6. If all attributes are selected, use the "*" symbol to indicate this, replacing all other selected attributes for that class.
                7. Create a JSON array with the selected attributes for each metamodel.
                8. Provide the final answer as valid JSON only. Exclude any explanations or delimiters.

                # INPUT
                View description: {view_description}
                Metamodel 1: {meta_1}
                Metamodel 2: {meta_2}
                List of relations: {join}
                Select elements:""",
        },
        "alternative": {
            'tags': ['CoT'],
            "template": """
                You specialize in reasoning about PlantUML metamodels, focusing on selecting and filtering attributes for each class.

                # TASK
                Given two metamodels, a view description, and a list of relations containing class pairs, your task is to determine the appropriate set of attributes for the classes in the metamodels.

                Select an attribute under the following conditions:
                - It is unique among the two classes in a relation.
                - It serves as a container for one of the classes in a relation.
                - It is explicitly mentioned in the view description.
                - It helps to elucidate the relation between the classes.

                Assume the input relations list follows this template:

                {{
                    "relations": [
                        {{
                            "name": "relationName",
                            "classes": ["class_name_from_first_metamodel", "class_name_from_second_metamodel"]
                        }}
                    ]
                }}

                # OUTPUT DATA FORMAT
                {format_instructions}

                # RULES
                When generating the response, adhere to these rules:
                - Use only class and attribute names that exist in the metamodels. Do not invent any names.
                - The symbol "*" denotes that all attributes of a given class should be selected. Use it only once per class per metamodel, and it supersedes all other selected attributes.

                # STEP-BY-STEP PROCESS
                1. For each relation, identify the classes to be analyzed. The classes are paired, with one class from each metamodel.
                2. For each class, determine the attributes to be included in the final response.
                3. If a class is contained within another class, include the container class and the attribute that references the contained class.
                4. Include any attribute explicitly mentioned in the view description.
                5. Add any additional attributes that help clarify the relationship between the classes.
                6. If all attributes are to be selected, use the "*" symbol, which replaces all other selected attributes for that class.
                7. Construct a JSON array with the selected attributes for each metamodel.
                8. Provide the final answer as valid JSON only. Do not include any explanations or delimiters.

                # INPUT
                View description: {view_description}
                Metamodel 1: {meta_1}
                Metamodel 2: {meta_2}
                List of relations: {join}
                Select elements:"""
        },
        "few-shot-cot":{
            'tags': ['few-shot', 'CoT'],
            'template': """You specialize in reasoning about PlantUML metamodels, particularly in selecting and filtering each class's attributes.

                # TASK
                Given two metamodels, a view description, and a list of relations containing class pairs, your task is to select a set of attributes for the metamodels' classes.

                An attribute should be selected in the following situations:
                - The attribute is unique among two classes in a relation.
                - The attribute is a container of one of the classes in a relation.
                - The attribute was explicitly mentioned in the view description.
                - The attribute helps the user to understand the relation between the classes.

                You may assume the following template for the input relations list:
                
                {{
                    "relations": [
                        {{
                            "name": "relationName",
                            "classes": ["class_name_from_first_metamodel", "class_name_from_second_metamodel"]
                        }}
                    ]
                }}
                

                # OUTPUT DATA FORMAT
                {format_instructions}

                # RULES
                When generating the response, follow these rules:
                - Only use class and attribute names that actually exist in the metamodels. Don't make them up.
                - The symbol "*" indicates that all attributes of a given class should be selected. Use it only once per class per metamodel, and it replaces all other selected attributes.

                # STEP-BY-STEP PROCESS
                1. For each relation, select the classes to be analyzed. The classes are always combined in pairs, in order, and contain one class from each metamodel.
                2. For each class, select the attributes that should appear in the final response.
                3. If the class is contained in another class, include the container class and the attribute that references the contained class.
                4. If an attribute is explicitly mentioned in the view description, include it in the list.
                5. Include other relevant attributes that help the user understand the relation between the classes.
                6. If all attributes are selected, use the "*" symbol to indicate this, replacing all other selected attributes for that class.
                7. Create a JSON array with the selected attributes for each metamodel.
                8. Provide the final answer as valid JSON only. Exclude any explanations or delimiters.

                You can think step-by-step, but your final answer should contain only the valid JSON and nothing else. Exclude any explanation or delimiter from the final response.

                # EXAMPLES""",
        },
        "few-shot-only": {
            "tags": ['few-shot'],
            'template': """You specialize in reasoning about PlantUML metamodels, particularly in selecting and filtering each class's attributes.

                # TASK
                Given two metamodels, a view description, and a list of relations containing class pairs, your task is to select a set of attributes for the metamodels' classes.

                An attribute should be selected in the following situations:
                - The attribute is unique among two classes in a relation.
                - The attribute is a container of one of the classes in a relation.
                - The attribute was explicitly mentioned in the view description.
                - The attribute helps the user to understand the relation between the classes.

                You may assume the following template for the input relations list:
                
                {{
                    "relations": [
                        {{
                            "name": "relationName",
                            "classes": ["class_name_from_first_metamodel", "class_name_from_second_metamodel"]
                        }}
                    ]
                }}
                

                # OUTPUT DATA FORMAT
                {format_instructions}

                # RULES
                When generating the response, follow these rules:
                - Only use class and attribute names that actually exist in the metamodels. Don't make them up.
                - The symbol "*" indicates that all attributes of a given class should be selected. Use it only once per class per metamodel, and it replaces all other selected attributes.

                Your final answer should contain only the valid JSON and nothing else. Exclude any explanation or delimiter from the final response.

                # EXAMPLES"""
        },
        'simplified': {
            'tags': ['no-techniques'],
            'template': """
                Given two metamodels, a view description, and a list of class relations, your task is to select attributes for the metamodels' classes.

                Select an attribute if:
                - It is unique among two classes in a relation.
                - It is a container of one of the classes in a relation.
                - It is explicitly mentioned in the view description.
                - It helps the user understand the relation between the classes.

                Assume the following template for the input relations list:

                {{
                    "relations": [
                        {{
                            "name": "relationName",
                            "classes": ["class_name_from_first_metamodel", "class_name_from_second_metamodel"]
                        }}
                    ]
                }}
                
                Your final answer should contain only the valid JSON and nothing else. Exclude any explanation or delimiter from the final response.

                """,
        }
    }
        
}
    
