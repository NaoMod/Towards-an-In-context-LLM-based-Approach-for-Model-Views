prompts = {
    "items": {
         "baseline": {
            'tags': ['CoT'],
            'template': """You specialize in reasoning on PlantUML metamodels, especially combining and merging them.

                # TASK
                Given two metamodels, a list of relations containing class pairs, and a view description, your task is to define how to combine the given classes.

                You must define the combination rules to merge classes from both metamodels.

                # INPUT TEMPLATE FOR RELATIONS
                The input relations list will be in the following format:
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
                When generating the response text, follow these rules:
                - Only use class and attribute names that actually exist in the metamodels. Do not invent new names.
                - The combination_rule should explain how the classes can be connected according to the domain's semantics, including the type of comparisons used to connect the classes in the relation.

                # STEP-BY-STEP PROCESS
                1. Select Metamodels: Identify the metamodels to be analyzed for each relation in the list of relations.
                2. Analyze Domain: For each pair of metamodel classes, analyze the domain considering the view description and propose a combination to relate both classes.
                3. Create Combination Rule: Create a JSON array with the combination rule for each relation. The combination rule should include the name of the first metaclass, the combination explanation, and the name of the second metaclass.
                4. Compile JSON Array: Compile a JSON array with one rule per relation.
                5. Provide Final Answer: Deliver the final JSON array as the response.

                # INPUT
                View description: {view_description}
                Metamodel 1: {meta_1}
                Metamodel 2: {meta_2}
                List of relations: {join}
                Combination rules:""",
         },
         "improved": {
             "tags": ['CoT'],
             "template": """You are an expert in reasoning with PlantUML metamodels, particularly in combining and merging them.

                # TASK
                Your task is to determine how to combine classes from two provided metamodels based on a given list of relations and a view description.

                You need to define the rules for combining classes from both metamodels.

                # INPUT TEMPLATE
                The input relations list will be formatted as follows:
                {{
                    "relations": [
                        {{
                            "name": "relationName",
                            "classes": ["class_name_from_first_metamodel", "class_name_from_second_metamodel"]
                        }}
                    ]
                }}

                # OUTPUT FORMAT
                {format_instructions}

                # GUIDELINES
                When creating the response, adhere to these guidelines:
                - Use only the class and attribute names that are present in the metamodels. Do not create new names.
                - Each combination_rule should describe how the classes can be linked based on the domain's semantics, specifying the types of comparisons that can be used to connect the classes in the relation.

                # STEP-BY-STEP PROCESS
                1. Identify Metamodels: Determine which metamodels to analyze for each relation in the relations list.
                2. Domain Analysis: For each class pair, analyze the domain using the view description to propose a method for combining the classes.
                3. Formulate Combination Rule: Construct a JSON array with the combination rule for each relation. Each rule should include the name of the first metaclass, an explanation of the combination, and the name of the second metaclass.
                4. Assemble JSON Array: Create a JSON array with one rule per relation.
                5. Submit Final Answer: Provide the final JSON array as the output.

                # INPUT
                View description: {view_description}
                Metamodel 1: {meta_1}
                Metamodel 2: {meta_2}
                List of relations: {join}
                Combination rules:"""
         },
         "few-shot-cot": {
            'tags': ['few-shot', 'CoT'], 
            'template': """You specialize in reasoning on PlantUML metamodels, especially combining and merging them.

                # TASK
                Given two metamodels, a list of relations containing class pairs, and a view description, your task is to define how to combine the given classes.

                You must define the combination rules to merge classes from both metamodels.

                # INPUT TEMPLATE FOR RELATIONS
                The input relations list will be in the following format:
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
                When generating the response text, follow these rules:
                - Only use class and attribute names that actually exist in the metamodels. Do not invent new names.
                - The combination_rule should explain how the classes can be connected according to the domain's semantics, including the type of comparisons used to connect the classes in the relation.

                # STEP-BY-STEP PROCESS
                1. Select Metamodels: Identify the metamodels to be analyzed for each relation in the list of relations.
                2. Analyze Domain: For each pair of metamodel classes, analyze the domain considering the view description and propose a combination to relate both classes.
                3. Create Combination Rule: Create a JSON array with the combination rule for each relation. The combination rule should include the name of the first metaclass, the combination explanation, and the name of the second metaclass.
                4. Compile JSON Array: Compile a JSON array with one rule per relation.
                5. Provide Final Answer: Deliver the final JSON array as the response.

                Exclude any explanation or delimiter from the final response.

                # EXAMPLES"""
        },
        "few-shot-only": {
            'tags': ['few-shot'], 
            'template': """You specialize in reasoning on PlantUML metamodels, especially combining and merging them.

                # TASK
                Given two metamodels, a list of relations containing class pairs, and a view description, your task is to define how to combine the given classes.

                You must define the combination rules to merge classes from both metamodels.

                # INPUT TEMPLATE FOR RELATIONS
                The input relations list will be in the following format:
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
                When generating the response text, follow these rules:
                - Only use class and attribute names that actually exist in the metamodels. Do not invent new names.
                - The combination_rule should explain how the classes can be connected according to the domain's semantics, including the type of comparisons used to connect the classes in the relation.
                Exclude any explanation or delimiter from the final response.

                # EXAMPLES"""
        },
        "simplified": {
            "tags": ['no-techniques'],
            "template":"""You specialize in reasoning on PlantUML metamodels, especially combining and merging them.

                # TASK
                Given two metamodels, a list of relations containing class pairs, and a view description, your task is to define how to combine the given classes.

                You must define the combination rules to merge classes from both metamodels.

                # INPUT TEMPLATE FOR RELATIONS
                The input relations list will be in the following format:
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
            """
        }        
    }
}
