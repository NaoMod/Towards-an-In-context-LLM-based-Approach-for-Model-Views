prompts = {
    "items": [
        {
            'tags': ['CoT'],
            'template': """You are a computer program specialized in reason on PlantUML metamodels, especially combining and merging them.\
                        Given the following two related metamodels, your task is to analyze them and determine which elements can be combined.
                        The elements are always combined in pairs.
                        Combining two elements means that they represent the same domain object but combine attributes coming from each metamodel, or they are complementary 
                        elements that can be combined to extend the meaning of the first with the attributes of the second.
                        Your answer should be a valid JSON list of dictionaries. Each dictionary represents a relation.\
                        Each relation always contain one class coming from each metamodel.\
                        
                        You may assume the following template for the JSON list of dictionaries representing the combinations of elements from the metamodels:

                        [
                            {{
                                "relationName": {{
                                    "first_metamodel_indentifier": "class_name",
                                    "second_metamodel_indentifier": "class_name"
                                }}
                            }}
                        ]

                        When generating the JSON text:
                        * Always define and use the same metamodel_identifier for each metamodel
                        * Only use class names that actually exist in the metamodels. Don't make them up.

                        The step-by-step process is as follows:

                        1. To get the first PlantUML metamodel, identify the metamodel identifier and all the classes.
                        2. To get the second PlantUML metamodel, identify the metamodel identifier and all the classes.
                        3. Given the metamodels and their classes, combine the elements in pairs when the selected classes represent the same domain object in each metamodel.
                        4. Given the classes, combine the elements in pairs when some selected class in the second metamodel can be a complement to some selected class on the first metamodel
                        5. Create the JSON array with the combination pairs.
                        6. Provide the final answer.

                        Your final answer should contain only the valid JSON and nothing else.

                        Metamodel 1: {meta_1}\
                        Metamodel 2: {meta_2}\
                        Relations:""",
        },
    ]
        
}