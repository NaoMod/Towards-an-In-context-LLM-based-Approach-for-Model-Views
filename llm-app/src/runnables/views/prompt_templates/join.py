prompts = {
    "items": {
        "baseline": {
            'tags': ['CoT'],
            'template': """You are now a PlantUML analyst tasked with finding relationships between classes from two metamodels.

                    # TASK
                    Analyze the input metamodels and the view description to define a list of relations between the metamodels' classes. Each relation must combine one class from the first metamodel with one from the second metamodel. Classes can be paired when they represent the same domain object, are complementary, or when the view description specifies attributes from one metamodel to appear in the other.

                    # OUTPUT DATA FORMAT
                    {format_instructions}

                    # RULES
                    When generating the JSON response, follow these rules:
                    - Use only class names that exist in the metamodels. Do not include any classes that are not in the metamodels.
                    - Ensure each relation's name is unique and meaningful.

                    # STEP-BY-STEP PROCESS
                    1. Identify all classes from the first metamodel.
                    2. Identify all classes from the second metamodel.
                    3. Combine classes in pairs when they represent the same domain object in each metamodel.
                    4. Combine classes in pairs when one class in the second metamodel can be complemented by a class in the first metamodel and vice-versa.
                    5. Analyze the view description for other potential relations.
                    6. Ensure each pair includes one class from each metamodel.
                    7. Ensure each relation's name is unique and meaningful.
                    8. Verify all classes exist in the PlantUML metamodels.
                    9. Create a JSON array with the combination pairs.
                    10. Provide only the valid JSON response without any explanation or delimiters.

                    # INPUT
                    View description: {view_description}
                    Metamodel 1: {meta_1}
                    Metamodel 2: {meta_2}
                    Relations:""",
        },
        "improved": {
            'tags': ['CoT'],
            'template': """You are now a PlantUML analyst with the task of identifying relationships between classes from two metamodels.

                    # TASK
                    Your objective is to examine the provided metamodels and the view description to establish a list of relationships between their classes. Each relationship must involve one class from the first metamodel and one class from the second metamodel. Classes should be paired if they represent the same domain object, are complementary, or if the view description explicitly requires attributes from one metamodel to be included in the other.

                    # OUTPUT DATA FORMAT
                    {format_instructions}

                    # RULES
                    When creating the JSON response, adhere to the following guidelines:
                    - Only use class names present in the metamodels. Do not include any external classes.
                    - Each relationship must have a unique and descriptive name.

                    # STEP-BY-STEP PROCESS
                    1. List all classes from the first metamodel.
                    2. List all classes from the second metamodel.
                    3. Pair classes from both metamodels that represent the same domain object.
                    4. Pair classes that can complement each other with attributes.
                    5. Review the view description for additional possible relationships.
                    6. Ensure each pair contains one class from each metamodel.
                    7. Assign a unique and meaningful name to each relationship.
                    8. Confirm that all classes used exist in the PlantUML metamodels.
                    9. Generate a JSON array with the paired combinations.
                    10. Output only the JSON response without any additional text or explanations.

                    # INPUT
                    View description: {view_description}
                    Metamodel 1: {meta_1}
                    Metamodel 2: {meta_2}
                    Relations:"""
        },
        "few-shot-cot": {
            'tags': ['few-shot', 'CoT'],
            'template': """You are now a PlantUML analyst that find relations between classes from two metamodels.
                        
                    # TASK
                    Your task is to analyze the input metamodel and the view description and define a list of relations between the metamodels' classes.
                    The classes are always combined in pairs, being one coming from the first metamodel and the other coming from the second metamodel.
                    Classes can be combined when they represent the same domain object or when they are complementary classes, which means that one can be extended with the attributes of the other.

                    Other possible reason for combinations is when the view description includes explicit attribbutes from one metamodel that should appear in the other.
                                            
                    Your answer should be a valid JSON list of dictionaries where each dictionary entry represents a relation. 
                    It should be a list even when it contains just one relation.
                    Each relation always contains precisely one class coming from each metamodel.
                    In your response, the classes are always in order: the first class comes from the first metamodel, and the second class comes from the second metamodel.

                    # OUTPUT DATA FORMAT                        
                    {format_instructions}                       
                    
                    # RULES
                    When generating the JSON response, you should follow these rules:
                    - Only use class names that exist in the metamodels. Never include classes that are not in the metamodels
                    - The relation's name can be any string, but it should be unique and meaningful for each relation.

                    # STEP BY STEP PROCESS
                    1. Identify all the classes from the first metamodel.
                    2. Identify all the classes from the second metamodel.
                    3. Given the metamodels and their classes, combine the elements in pairs when the selected classes represent the same domain object in each metamodel.
                    4. Given the metamodels and their classes, combine the elements in pairs when some selected class in the second metamodel can be complemented by some chosen class on the first metamodel and vice-versa.
                    5. Analyse the view description to find out other potential relations.
                    6. Ensure that the classes are combined in pairs, one from each metamodel.
                    7. Ensure that the relation's name is unique and meaningful.
                    8. Ensure that all the classes exist in the PlantUML metamodels.
                    9. Create the JSON array with the combination pairs.
                    10. Provide the answer.

                    You can think step-by-step, but your final answer should contain only the valid JSON and nothing else. Exclude any explanation or delimiter from the final response.

                    # EXAMPLES
                    """,
        },
        "few-shot": {
            'tags': ['few-shot'],
            'template': """You are now a PlantUML analyst that find relations between classes from two metamodels.
                        
                    # TASK
                    Your task is to analyze the input metamodel and the view description and define a list of relations between the metamodels' classes.
                    The classes are always combined in pairs, being one coming from the first metamodel and the other coming from the second metamodel.
                    Classes can be combined when they represent the same domain object or when they are complementary classes, which means that one can be extended with the attributes of the other.

                    Other possible reason for combinations is when the view description includes explicit attribbutes from one metamodel that should appear in the other.
                                            
                    Your answer should be a valid JSON list of dictionaries where each dictionary entry represents a relation. 
                    It should be a list even when it contains just one relation.
                    Each relation always contains precisely one class coming from each metamodel.
                    In your response, the classes are always in order: the first class comes from the first metamodel, and the second class comes from the second metamodel.

                    # OUTPUT DATA FORMAT                        
                    {format_instructions}                       
                    
                    # RULES
                    When generating the JSON response, you should follow these rules:
                    - Only use class names that exist in the metamodels. Never include classes that are not in the metamodels
                    - The relation's name can be any string, but it should be unique and meaningful for each relation.

                    Your final answer should contain only the valid JSON and nothing else. Exclude any explanation or delimiter from the final response.

                    # EXAMPLES
                    """,
        },
        "simplified": {
            'tags': ['no-techniques'],
            'template': """                        
                    # TASK
                    Analyze the input metamodel and the view description to define relations between the metamodel classes.

                        - Each relation pairs a class from the first metamodel with a class from the second metamodel.
                        - Classes are paired if they represent the same domain object, are complementary (one can be extended with the attributes of the other), or if the view description explicitly includes attributes from one metamodel that should appear in the other.

                    Your response should be a JSON list of dictionaries, where each dictionary represents a relation. Even if there's only one relation, it should still be a list. Each dictionary must have one class from each metamodel, always in the order: first metamodel class, then second metamodel class.

                    # OUTPUT DATA FORMAT                        
                    {format_instructions}

                    Your final answer should contain only the valid JSON and nothing else. Exclude any explanation or delimiter from the final response.

                    # INPUT
                    View description: {view_description}
                    Metamodel 1: {meta_1}
                    Metamodel 2: {meta_2}
                    Relations:""",
        }
    }        
}