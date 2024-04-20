prompts = {
    "items": [
        {
            'tags': ['join-zsCoT'],
            'template': """You specialize in reason on PlantUML metamodels, especially combining and merging them into views.
                        
                        Your task is to analyze two metamodels and the view description and determine which classes should be combined in the view.
                        The classes are always combined in pairs.

                        Classes can be combined when they represent the same domain object or when they are complementary classes, which means that the first can be extended with the attributes of the second and vice-versa.
                                                
                        Your answer should be a valid JSON list of dictionaries. Each dictionary entry represents a relation. 
                        It should be a list even when it contains just one relation.
                        Each relation always contains exactly one class coming from each metamodel.
                                                
                        You may assume the template below for the JSON response:

                        [
                            {{
                                "relationName": ["class_name_of_first_metamodel", "class_name_of_second_metamodel"]
                            }}
                        ]

                        Each relation is in the following format: ["class_name_of_first_metamodel",  class_name_of_second_metamodel"], which is always a list with two strings. 
                        The strings are always in order: the first string is always a class from the first metamodel, and the second string is always a class from the second metamodel.

                        When generating the JSON response, you should follow these rules:
                        Only use class names that actually exist in the metamodels. Don't make them up.
                        The relation's name can be any string, but it should be unique and meaningful for each relation.

                        The step-by-step process is as follows:

                        1. Get the metamodel name for the first PlantUML metamodel and identify all the classes.
                        2. Get the metamodel name for the second PlantUML metamodel and identify all the classes.
                        3. Given the metamodels and their classes, combine the elements in pairs when the selected classes represent the same domain object in each metamodel.
                        4. Given the metamodels and their classes, combine the elements in pairs when some selected class in the second metamodel can be complemented to some selected class on the first metamodel
                        5. Create the JSON array with the combination pairs.
                        6. Provide the final answer.

                        Your final answer should contain only the valid JSON and nothing else. Exclude any explanation or delimiter from the final response.

                        View description: {view_description}
                        Metamodel 1: {meta_1}
                        Metamodel 2: {meta_2}
                        Relations:""",
        },
    ]
        
}