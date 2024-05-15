prompts = {
    "items": [
        {
            'tags': ['ATLjoin-zsCoT'],
            'template': """You specialize in reason on PlantUML metamodels, especially finding relations between different metamodels to help in the development of ATL transformations.
                        
                        Given two metamodels, your task is to analyze them and the transformation description and determine the relations between the metaclasses.
                        The classes are always combined in pairs.

                        Classes should be combined when their attributes and associations align between the source and target metamodels
                                                
                        Each relation always contains precisely one class coming from each metamodel. Each relation is also named.
                                                
                        The classes are always given in order: the first string is a class from the first metamodel, and the second string is always a class from the second metamodel.

                        When generating the response, you should follow these rules:
                        Only use class names that exist in the provided PlantUML metamodels.
                        The relation's name can be any string, but it should be unique and meaningful for each relation.

                        The step-by-step process is as follows:

                        1. Identify all the classes from the first metamodel.
                        2. Identify all the classes from the second metamodel.
                        3. Given the metamodels and their classes, combine the elements in pairs when their attributes and associations align between the source and target metamodels.
                        5. Provide the answer.

                        Exclude any explanation or delimiter from the final response.

                        {format_instructions}

                        Transformation description: {transformation_description}
                        Metamodel 1: {meta_1}
                        Metamodel 2: {meta_2}
                        Relations:""",
        },
    ]
        
}