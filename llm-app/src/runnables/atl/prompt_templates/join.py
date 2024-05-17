prompts = {
    "items": [
        {
            'tags': ['ATLjoin-zsCoT'],
            'template': """You specialize in reasoning on PlantUML metamodels, finding mapping relations between two different metamodels to help in a ATL transformation development.

                    Given two metamodels, your task is to analyze them and the transformation description to determine the mappings between the metaclasses. It means specifying how elements from the input metamodel 1 are mapped to elements in the output metamodel 2.

                    When generating the response, follow these rules:
                    - Each mapping relation contains precisely one class from each metamodel.
                    - Only use class names existing in the provided PlantUML metamodels. Don't make them up.
                    - The relation's name can be any string, but it must be unique and meaningful for each relation.
                    - The classes in the relation should be given in order: the first string is a class from the first metamodel, and the second string is always a class from the second metamodel.

                    The step-by-step process is as follows:
                    1. Identify the classes in the input metamodel 1 that need to be transformed into elements in the output metamodel 2.
                    2. Determine the necessary transformations based on the transformation description and input metamodel structure.
                    3. Define the logic for transforming elements from the input metamodel into elements in the output metamodel, considering attributes and relationships.
                    4. Choose appropriate mapping strategies, such as direct mappings or more complex transformations.
                    5. Address any ambiguities or uncertainties in the transformation process.
                    6. Create a list of relations between classes in the input and output metamodels, specifying how elements from the input metamodel are mapped to elements in the output metamodel.

                    Provide the answer following the format below:

                    {format_instructions}

                    Exclude any explanation or delimiter from the final response.

                    Transformation description: {transformation_description}
                    Metamodel 1 (input metamodel): {meta_1}
                    Metamodel 2 (output metamodel): {meta_2}
                    Relations:
                    """,
        },
    ]
        
}