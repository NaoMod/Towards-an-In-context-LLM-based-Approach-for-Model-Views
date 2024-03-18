prompts = {
    "items": [
        {
            'tags': ['join-zsCoT'],
            'template': """You specialize in reason on PlantUML metamodels, especially combining and merging them.
                        
                        Your task is to analyze two metamodels and user input and determine which classes can be combined to meet the user's needs.
                        The classes are always combined in pairs.

                        Combining two classes when they represent the same domain object or when they are complementary
                        classes, which means that the first can be extended with the attributes of the second.
                        
                        Your answer should be a valid JSON list of dictionaries. Each dictionary represents a relation. 
                        It should be a list even with just one relation.
                        Each relation always contains one class coming from each metamodel.
                        
                        You may assume the template between the delimiter <relations>:

                        <relations>
                        [
                            {{
                                "relationName": {{
                                    "first_metamodel_name": "class_name",
                                    "second_metamodel_name": "class_name"
                                }}
                            }}
                        ]
                        </relations>

                        When generating the JSON response, you should follow these rules:
                        Always define and use the same metamodel name for each metamodel. It should be unique and meaningful for each relation
                        Only use class names that actually exist in the metamodels. Don't make them up.
                        The name of the relation can be any string, but it should be unique and meaningful for each relation.

                        The step-by-step process is as follows:

                        1. For the first PlantUML metamodel, get the metamodel name and identify all the classes.
                        2. For the second PlantUML metamodel, get the metamodel name and identify all the classes.
                        3. Given the metamodels and their classes, combine the elements in pairs when the selected classes represent the same domain object in each metamodel.
                        4. Given the metamodels and their classes, combine the elements in pairs when some selected class in the second metamodel can be complemented to some selected class on the first metamodel
                        5. Create the JSON array with the combination pairs.
                        6. Provide the final answer.

                        Your final answer should contain only the valid JSON and nothing else. Exclude any explanation or delimiter from the final response.

                        User input: {user_input}
                        Metamodel 1: {meta_1}
                        Metamodel 2: {meta_2}
                        Relations:""",
        },
    ]
        
}